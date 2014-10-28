import collections
import logging
import os
import re

from cStringIO import StringIO

import jinja2.nodes

from jinja2.compiler import TemplateAssertionError
from jinja2.visitor import NodeVisitor
from jinja2.utils import escape

from jinja2js import nodes

log = logging.getLogger(__name__)

UNARYOP = {
    "not ": "!"
}

OPERATORS = {
    "eq":    "==",
    "ne":    "!=",
    "gt":    ">",
    "gteq":  ">=",
    "lt":    "<",
    "lteq":  "<=",
}

LIST_OPERATORS = ('in', 'notin')

BOOL_NODES = (jinja2.nodes.And, jinja2.nodes.Or, jinja2.nodes.Not,
              jinja2.nodes.Compare)

BOOL_BIN_NODES = (jinja2.nodes.And, jinja2.nodes.Or, jinja2.nodes.Compare)


def base_path(path):
    return os.path.splitext(path)[0]

class JSIdentifiers(jinja2.compiler.Identifiers):
    def __init__(self):
        super(JSIdentifiers, self).__init__()

        # The namespace of the current template.
        self.namespace = None

        # Local names to absolute namespaced names.
        self.imports = {}

        # Template paths to namespaces. Tracked separately from absolute
        # namespaced names to make it easy to print the necessary goog.require
        # calls in the CodeGenerator.
        self.import_namespaces = {}

        # Local names to absolute namespaced names.
        self.exports = {}

        self.imported_identifiers = {}
        self.exported_macros = {}
        self.macros = {}

    def __repr__(self):
        return 'JSIdentifiers(%r)' % self.__dict__

def dot_join(*args):
    return '.'.join(map(str, args))

class Macro(object):
    def __init__(self, namespace, name, args, defaults, dyn_args=False, dyn_kwargs=False):
        # The namespace where the function is defined
        self.namespace = namespace
        # The name of the function within the namespace
        self.name = name
        # The full namespaced name
        self.fullname = dot_join(namespace, name)
        # The names of all parameters declared in the signature
        self.args = args
        # Default arg values. Right aligned with args.
        self.defaults = defaults
        # Whether the function accepts additional positional params
        self.dyn_args = dyn_args
        # Whether the function accepts additional keyword params
        self.dyn_kwargs = dyn_kwargs

    def call_signature(self, gen, node, frame):
        gen.write('%s(' % self.fullname)

        data = collections.OrderedDict()
        dyn_args = []
        dyn_kwargs = collections.OrderedDict()

        for i, arg in enumerate(node.args):
            try:
                key = self.args[i]
            except IndexError:
                dyn_args.append(arg)
            else:
                data[key.name] = arg

        for arg in node.kwargs:
            if arg.key in data:
                raise TemplateAssertionError('Arg provided twice')
            if any(arg.key == n.name for n in self.args):
                data[arg.key] = arg.value
            else:
                dyn_kwargs[arg.key] = arg.value

        if data:
            gen.write("{")
            for i, (key, value) in enumerate(data.iteritems()):
                gen.write(key)
                gen.write(': ')
                gen.visit(value, frame)
                if i < len(data) - 1:
                    gen.write(', ')
            gen.write("}")

        gen.write(")")

class JSFunction(object):
    def __init__(self, js_name):
        self.js_name = js_name

    def call_signature(self, gen, node, frame):
        gen.write('%s(' % self.js_name)
        for i, arg in enumerate(node.args):
            if i > 0:
                gen.write(', ')
            gen.visit(arg, frame)
        gen.visit(')')

class Loop(object):
    def __init__(self, name):
        self.name = name
        self.list = '__%sList' % name
        self.length = '__%sListLength' % name
        self.index = '__%sIndex' % name

def import_and_parse_identifiers(env, options, name):
    source, filename, uptodate = env.loader.get_source(env, name)
    template_node = env._parse(source, name, filename)

    namespace = namespace_from_tmpl(template_node, name, filename)

    eval_ctx = jinja2.nodes.EvalContext(env, name)
    eval_ctx.encoding = "utf-8"

    frame = JSFrame(env, options, eval_ctx)
    frame.identifiers.namespace = namespace
    frame.inspect(template_node.body)
    frame.toplevel = frame.rootlevel = True

    return frame.identifiers

class JSFrameIdentifierVisitor(jinja2.compiler.FrameIdentifierVisitor):

    def __init__(self, identifiers, environment, options, ctx):
        self.identifiers = identifiers
        self.environment = environment
        self.options = options
        self.ctx = ctx

    def blockvisit(self, nodes):
        for node in nodes:
            self.visit(node)

    # def visit_Name

    def visit_If(self, node):
        self.visit(node.test)
        for body in node.body:
            self.visit(body)
        for else_ in node.else_:
            self.visit(else_)

    def visit_Macro(self, node):
        self.identifiers.exports[node.name] = dot_join(
            self.identifiers.namespace,
            node.name,
        )

        macro = Macro(
            self.identifiers.namespace,
            node.name,
            node.args,
            node.defaults,
        )
        self.identifiers.macros[macro.fullname] = macro
        self.identifiers.exported_macros[macro.fullname] = macro
        log.debug('Indexing %r %r', macro.fullname, macro)

    def visit_Import(self, node):
        self.generic_visit(node)

        name = node.template.value
        identifiers = import_and_parse_identifiers(self.environment, self.options, name)
        namespace = identifiers.namespace
        self.identifiers.import_namespaces[name] = namespace
        self.identifiers.imports[node.target] = namespace

        self.identifiers.macros.update(identifiers.macros)

        self.identifiers.declared_locally.add(node.target)

    def visit_FromImport(self, node):
        self.generic_visit(node)

        path = node.template.value
        identifiers = import_and_parse_identifiers(self.environment, self.options, path)
        namespace = identifiers.namespace
        self.identifiers.import_namespaces[path] = namespace

        for item in node.names:
            name = item[1] if isinstance(item, tuple) else item
            self.identifiers.imports[name] = dot_join(namespace, name)

            try:
                macro = identifiers.exported_macros[dot_join(namespace, name)]
            except KeyError:
                raise TemplateAssertionError(
                    'Template %r does not contain a macro named %r' %
                    (path, name), 0)

            self.identifiers.macros[macro.fullname] = macro
            log.debug('Indexing %r %r', macro.fullname, macro)

            self.identifiers.declared_locally.add(name)


    # def visit_Assign

    def visit_For(self, node):
        # declare the iteration variable
        self.visit(node.iter)
        # declare the target variable
        self.visit(node.target)
        # declare anything in the for loops body. that might need to be
        # managed, like caller functions.
        self.blockvisit(node.body)

    # def visit_Callblock

    # def visit_FilterBlock

    # def visit_Block


class JSFrame(jinja2.compiler.Frame):

    def __init__(self, environment, options, eval_ctx, parent=None):
        super(JSFrame, self).__init__(eval_ctx, parent)

        self.identifiers = JSIdentifiers()
        self.environment = environment
        self.options = options

        # mapping of visit_Name callback to reassign variable names for use
        # in 'for' loops
        self.reassigned_names = {}

        self.current_loop = None
        self.declared_loops = {}

        # Track if we are escaping some output
        self.escaped = False

        if parent is not None:
            self.identifiers.imports = parent.identifiers.imports
            self.identifiers.macros = parent.identifiers.macros

    def inspect(self, nodes):
        """Walk the node and check for identifiers.  If the scope is hard (eg:
        enforce on a python level) overrides from outer scopes are tracked
        differently.
        """
        visitor = JSFrameIdentifierVisitor(
            self.identifiers, self.environment, self.options, self.eval_ctx)
        for node in nodes:
            visitor.visit(node)

    def inner(self):
        return JSFrame(self.environment, self.options, self.eval_ctx, self)

    def new_loop(self, node):
        basename = name = node.target.name
        i = 0
        while name in self.declared_loops:
            i += 1
            name = basename + i
        return Loop(name)


class BaseCodeGenerator(NodeVisitor):

    def __init__(self, environment, options, name, filename):
        super(BaseCodeGenerator, self).__init__()

        self.environment = environment
        self.options = options
        self.name = name
        self.filename = filename

        self.stream = StringIO()

        # the current line number
        self.code_lineno = 1

        # the debug information
        self.debug_info = []
        self._write_debug_info = None

        # the number of new lines before the next write()
        self._new_lines = 0

        # the line number of the last written statement
        self._last_line = 0

        # true if nothing was written so far.
        self._first_write = True

        # the current indentation multiplier
        self._indentation = 0

        # the character(s) to display as a single indent
        self._indentation_text = options['js_indentation']

    def indent(self):
        """Indent by one."""
        self._indentation += 1

    def outdent(self, step=1):
        """Outdent by step."""
        self._indentation -= step

    def write(self, x, node=None):
        """Write a string into the output stream."""
        self.mark(node)
        if self._new_lines:
            if not self._first_write:
                self.stream.write('\n' * self._new_lines)
                self.code_lineno += self._new_lines
                if self._write_debug_info is not None:
                    self.debug_info.append((self._write_debug_info,
                                            self.code_lineno))
                    self._write_debug_info = None
            self._first_write = False
            self.stream.write(self._indentation_text * self._indentation)
            self._new_lines = 0
        self.stream.write(x)

    def writeline(self, x, node=None, extra=0):
        """Combination of newline and write."""
        self.newline(node, extra)
        self.write(x)

    def write_string_const(self, x):
        xrepr = repr(x)
        if isinstance(xrepr, unicode):
            self.write(xrepr[1:])
        else:
            self.write(xrepr)

    def mark(self, node):
        # Mark the current output to correspond to the node.
        if node is not None and node.lineno != self._last_line:
            self._write_debug_info = node.lineno
            self._last_line = node.lineno

    def newline(self, node=None, extra=0):
        """Add one or more newlines before the next write."""
        self._new_lines = max(self._new_lines, 1 + extra)
        self.mark(node)

    def writeline_startoutput(self, node, frame):
        self.writeline("var __output = '';", node)

    def writeline_endoutput(self, node, frame):
        self.writeline("return __output;", node)

    def writeline_outputappend(self, node, frame):
        self.writeline("__output += ", node)

    def write_outputappend_add(self, node, frame):
        self.write(" + ")

    def write_outputappend_end(self, node, frame):
        self.write(";")

    def write_htmlescape(self, node, frame):
        self.write('_.escape(')

    def write_htmlescape_end(self, node, frame):
        self.write(')')

    def blockvisit(self, nodes, frame):
        """
        Visit a list of noes ad block in a frame. Some times we want to
        pass lists to the the visit method. Get around this here.
        """
        # if frame.buffer
        for node in nodes:
            self.visit(node, frame)


def namespace_from_tmpl(node, name=None, filename=None):
    ns_nodes = list(node.find_all(nodes.NamespaceNode))
    # TODO: Require exactly one namespace
    if len(ns_nodes) > 1:
        raise jinja2.compiler.TemplateAssertionError(
            'You must provide exactly one {% namespace %} node',
            0, name, filename)
    return ns_nodes[0].namespace if ns_nodes else 'jinja2js'

def namespace_from_import(env, name):
    source, filename, uptodate = env.loader.get_source(env, name)
    imported_node = env._parse(source, name, filename)
    return namespace_from_tmpl(imported_node, name, filename)


class CodeGenerator(BaseCodeGenerator):

    def __init__(self, environment, options, name, filename):
        super(CodeGenerator, self).__init__(environment, options, name, filename)
        self.namespace = None

    def visit_Template(self, node):
        """
        Setup the template output.

        Includes imports, macro definitions, etc.
        """
        self.namespace = namespace_from_tmpl(node, self.name, self.filename)

        have_extends = node.find(jinja2.nodes.Extends) is not None
        if have_extends:
            raise ValueError("JSCompiler doesn't support extends")

        have_blocks = node.find(jinja2.nodes.Block) is not None
        if have_blocks:
            raise ValueError("JSCompiler doesn't support blocks")

        eval_ctx = jinja2.nodes.EvalContext(self.environment, self.name)
        eval_ctx.encoding = "utf-8"

        # process the root
        frame = JSFrame(self.environment, self.options, eval_ctx)
        frame.identifiers.namespace = self.namespace
        frame.inspect(node.body)
        frame.toplevel = frame.rootlevel = True

        self.writeline("goog.provide('%s');\n" % self.namespace)
        self.blockvisit(node.body, frame)

    def visit_Import(self, node, frame):
        self.mark(node)
        path = node.template.value
        namespace = frame.identifiers.import_namespaces[path]
        self.writeline("goog.require('%s');\n" % namespace)

    def visit_FromImport(self, node, frame):
        self.visit_Import(node, frame)

    def visit_Macro(self, node, frame):
        generator = MacroCodeGenerator(
            self.environment,
            self.options,
            self.stream,
            self.namespace,
            self.name,
            self.filename,
        )
        generator.visit(node, frame)

    def visit_Const(self, node, frame):
        val = node.value
        if val is None:
            self.write("null")
        elif val is True:
            self.write("true")
        elif val is False:
            self.write("false")
        else:
            self.write(repr(val))

        return False

    def visit_TemplateData(self, node, frame):
        self.mark(node)
        self.write(node.data)


class MacroCodeGenerator(BaseCodeGenerator):
    # split out the macro code generator. This generate the guts of the
    # JavaScript we need to render the templates. Note that we do this
    # here seperate from the template generator above as we want to restrict
    # the Jinja2 template syntax for the JS implementation and we want to
    # format the generate code a bit like the templates. Gaps between
    # templates, comments should be displayed in the JS file. We need them for
    # any closure compiler hints we may want to put in.

    def __init__(self, environment, options, stream, namespace, name, filename):
        super(MacroCodeGenerator, self).__init__(environment, options, name, filename)

        self.stream = stream
        self.namespace = namespace

    def visit_Output(self, node, frame):
        # JS is only interested in macros etc, as all of JavaScript
        # is rendered into the global namespace so we need to ignore data in
        # the templates that is out side the macros.
        if frame.toplevel:
            return

        finalize = unicode

        # try to evaluate as many chunks as possible into a static
        # string at compile time.
        body = []
        for child in node.nodes:
            try:
                const = child.as_const(frame.eval_ctx)
            except jinja2.nodes.Impossible:
                body.append(child)
                continue

            # the frame can't be volatile here, becaus otherwise the
            # as_const() function would raise an Impossible exception
            # at that point.
            try:
                if frame.eval_ctx.autoescape:
                    if hasattr(const, '__html__'):
                        const = const.__html__()
                    else:
                        const = escape(const)
                const = finalize(const)
            except:
                # if something goes wrong here we evaluate the node
                # at runtime for easier debugging
                body.append(child)
                continue

            if body and isinstance(body[-1], list):
                body[-1].append(const)
            else:
                body.append([const])

        start = True
        for item in body:
            if isinstance(item, list):
                if start:
                    self.writeline_outputappend(node, frame)
                    start = False
                else:
                    self.write_outputappend_add(node, frame)
                if self.options['strip_html_whitespace']:
                    item = [strip_html_whitespace(itemhtml)
                            for itemhtml in item]
                self.write(repr("".join(item))[1:])
            else:
                if start:
                    self.writeline_outputappend(item, frame)
                    start = False
                else:
                    self.write_outputappend_add(item, frame)

                # autoescape, safe, and escape
                if isinstance(item, jinja2.nodes.Filter):
                    if item.name == "safe":
                        self.visit(item.node, frame)
                        continue

                if isinstance(item, jinja2.nodes.Call):
                    self.visit(item, frame)

                elif frame.eval_ctx.autoescape:
                    self.write_htmlescape(node, frame)
                    escaped_frame = frame.soft()
                    escaped_frame.escaped = True

                    self.visit(item, escaped_frame)

                    self.write_htmlescape_end(node, frame)
                else:
                    self.visit(item, frame)

        if not start:
            self.write_outputappend_end(node, frame)

    def visit_Filter(self, node, frame):
        # safe attribute with autoesacape is handled in visit_Output
        if node.name == "escape":
            if node.kwargs:
                raise Exception("No kwargs")

            if not frame.escaped:
                self.write_htmlescape(node, frame)
                frame = frame.soft()
                frame.escaped = True
                self.visit(node.node, frame)
                self.write_htmlescape_end(node, frame)
            else:
                self.visit(node.node, frame)
        else:
            self.write('jinja2filters.')
            self.write(node.name)
            self.write('(')
            self.visit(node.node, frame)
            for arg in node.args:
                self.write(', ')
                self.visit(arg, frame)
            if node.kwargs:
                self.write(", {'__jinja2_kwargs__': true")
                for kwarg in node.kwargs:
                    self.write(", '" + kwarg.key + "': ")
                    self.visit(kwarg.value, frame)
                self.write('}')
            self.write(')')

    def visit_Const(self, node, frame, dotted_name=None):
        # XXX - need to know the JavaScript ins and out here.
        val = node.value
        if val is None:
            output = "null"
        elif val is True:
            output = "true"
        elif val is False:
            output = "false"
        else:
            output = repr(val)

        if dotted_name is None:
            self.write(output)
        else:
            dotted_name.append(output)

        return False

    def visit_List(self, node, frame):
        self.write("[")
        for idx, item in enumerate(node.items):
            if idx:
                self.write(", ")
            self.visit(item, frame)
        self.write("]")

    def visit_Dict(self, node, frame):
        self.write("{")
        for idx, item in enumerate(node.items):
            if idx:
                self.write(", ")

            # item.key should be a constant string. Otherwise how do you
            # get to output a dictionary with a variable key string?
            # So it is either a `Const` or `Name` node.
            if isinstance(item.key, jinja2.nodes.Const):
                self.write_string_const(item.key.value)
            elif isinstance(item.key, jinja2.nodes.Name):
                self.write(item.key.name)
            else:
                msg = "Dictionary keys must be constant."
                raise TemplateAssertionError(msg, item.key.lineno, self.name,
                                             self.filename)

            self.write(": ")
            self.visit(item.value, frame)

        self.write("}")

    def visit_Name(self, node, frame, dotted_name=None):
        # declared_parameter
        # declared
        # outer_undeclared
        # declared_locally
        # undeclared
        # exported
        name = node.name
        isparam = False

        ids = frame.identifiers
        topframe = frame
        while not topframe.toplevel:
            topframe = topframe.parent

        parent_ids = frame.parent.identifiers if frame.parent else None

        if name in ids.declared_parameter or name in ids.outer_undeclared:
            output = name
            isparam = True
        elif parent_ids and name in parent_ids.declared_parameter:
            output = name

        elif name in frame.reassigned_names:
            output = frame.reassigned_names[name]

            isparam = True

        elif name in topframe.identifiers.exports:
            output = topframe.identifiers.exports[name]
        elif name in topframe.identifiers.imports:
            output = topframe.identifiers.imports[name]
        elif name in name in frame.identifiers.declared_locally:
            output = name

        elif name in ids.imports:
            # This is an import.
            output = ids.imports[name]

            frame.assigned_names.add(ids.imports[name])
        else:
            if dotted_name is None:
                msg = "Variable '%s' not defined" % name
                raise TemplateAssertionError(msg, node.lineno, self.name,
                                             self.filename)

            output = name

        if dotted_name is None:
            self.write(output)
        else:
            dotted_name.append(output)

        return isparam

    def visit_Slice(self, node, frame, dotted_name=None):
        if node.step is not None:
            raise NotImplementedError("jinja2js does not currently support "
                                      "steps in slices")

        if node.start:
            self.visit(node.start, frame, dotted_name)
            start = dotted_name.pop()
        else:
            start = '0'

        if node.stop:
            self.visit(node.stop, frame, dotted_name)
            stop = ', %s' % dotted_name.pop()
        else:
            stop = ''

        dotted_name.append('slice(%s%s)' % (start, stop))

    def visit_Getitem(self, node, frame, dotted_name=None):

        write_variable = False
        if dotted_name is None:
            dotted_name = []
            write_variable = True

        self.visit(node.node, frame, dotted_name)

        arg_name = []
        self.visit(node.arg, frame, arg_name)

        if isinstance(node.arg, jinja2.nodes.Slice):
            dotted_name.extend(arg_name)
        else:
            node = dotted_name.pop()
            dotted_name.append("%s[%s]" % (node, '.'.join(arg_name)))

        if write_variable:
            self.write(".".join(dotted_name))

    def visit_Getattr(self, node, frame, dotted_name=None):
        if dotted_name is None \
        and frame.current_loop \
        and isinstance(node.node, jinja2.nodes.Name):
            rhs_name = node.node.name
            if rhs_name == 'loop':
                loop = frame.current_loop
            elif rhs_name in frame.declared_loops:
                loop = frame.declared_loops[rhs_name]
            else:
                loop = None
            if loop:
                if node.attr == 'index':
                    self.write('%s + 1' % loop.index)
                elif node.attr == 'index0':
                    self.write('%s' % loop.index)
                elif node.attr == 'revindex0':
                    self.write('%s - %s' % (loop.length, loop.index))
                elif node.attr == 'revindex':
                    self.write('%s - %s - 1' % (loop.length, loop.index))
                elif node.attr == 'first':
                    self.write('!%s' % loop.index)
                elif node.attr == 'last':
                    self.write('%s == (%s - 1)' % (loop.index, loop.length))
                elif node.attr == 'length':
                    self.write(loop.length)
                elif node.attr == 'cycle':
                    raise NotImplementedError()
                return

        # write_variable is going to be true if dotted_name is None which
        # implies that we are gathering the variable name together. So
        # don't write it out yet.
        write_variable = False
        if dotted_name is None:
            dotted_name = []
            write_variable = True

        # collect variable name
        self.visit(node.node, frame, dotted_name)
        dotted_name.append(node.attr)

        if write_variable:
            self.write(".".join(dotted_name))

    def binop(operator):
        def visitor(self, node, frame):
            self.write("(")
            self.visit(node.left, frame)
            self.write(" %s " % operator)
            self.visit(node.right, frame)
            self.write(")")
        return visitor

    # Math operators
    visit_Add = binop("+")
    visit_Sub = binop("-")
    visit_Mul = binop("*")
    visit_Div = binop("/")
    visit_Mod = binop("%")

    def visit_FloorDiv(self, node, frame):
        self.write("Math.floor(")
        self.visit(node.left, frame)
        self.write(" / ")
        self.visit(node.right, frame)
        self.write(")")

    def visit_Pow(self, node, frame):
        self.write("Math.pow(")
        self.visit(node.left, frame)
        self.write(", ")
        self.visit(node.right, frame)
        self.write(")")

    def bool_binop(operator):

        def visitor(self, node, frame):
            left_bool = type(node.left) in BOOL_NODES
            left_bool_bin = type(node.left) in BOOL_BIN_NODES

            if left_bool_bin:
                self.write("(")

            if not left_bool:
                self.write("_.truth(")

            self.visit(node.left, frame)

            if not left_bool:
                self.write(")")

            if left_bool_bin:
                self.write(")")

            self.write(" %s " % operator)

            right_bool = type(node.right) in BOOL_NODES
            right_bool_bin = type(node.right) in BOOL_BIN_NODES

            if right_bool_bin:
                self.write("(")

            if not right_bool:
                self.write("_.truth(")

            self.visit(node.right, frame)

            if not right_bool:
                self.write(")")

            if right_bool_bin:
                self.write(")")

        return visitor

    visit_And = bool_binop('&&')
    visit_Or = bool_binop('||')

    def visit_Not(self, node, frame):
        start = "!(" if type(node.node) in BOOL_NODES else "_.not("
        self.write(start)
        self.visit(node.node, frame)
        self.write(")")

    def uaop(operator):
        def visitor(self, node, frame):
            self.write(UNARYOP.get(operator, operator) + "(")
            self.visit(node.node, frame)
            self.write(")")
        return visitor

    visit_Pos = uaop("+")
    visit_Neg = uaop("-")

    del binop, bool_binop, uaop

    def visit_Concat(self, node, frame):
        self.write("''")
        for n in node.nodes:
            self.write(' + ')
            self.visit(n, frame)

    def visit_Compare(self, node, frame):
        op = node.ops[0]
        if len(node.ops) == 1 and op.op in LIST_OPERATORS:
            if op.op == 'notin':
                self.write('!')
            self.write('_.in_(')
            self.visit(node.expr, frame)
            self.write(', ')
            self.visit(op.expr, frame)
            self.write(')')
        else:
            self.visit(node.expr, frame)
            # XXX - ops is a list. Can we have a list of comparisons
            for op in node.ops:
                self.visit(op, frame)

    def visit_Operand(self, node, frame):
        self.write(" %s " % OPERATORS[node.op])
        self.visit(node.expr, frame)

    def visit_If(self, node, frame):
        if_frame = frame.soft()

        test_bool = type(node.test) in BOOL_NODES

        start = "if (" if test_bool else "if (_.truth("
        end = ") {" if test_bool else ")) {"

        self.writeline(start, node)
        self.visit(node.test, if_frame)
        self.write(end)

        self.indent()
        self.blockvisit(node.body, if_frame)
        self.outdent()

        if node.else_:
            self.writeline("} else {")
            self.indent()
            self.blockvisit(node.else_, if_frame)
            self.outdent()

        self.writeline("}")

    def visit_For(self, node, frame):
        node.iter_child_nodes(exclude=("iter",))

        if node.recursive:
            raise NotImplementedError(
                "JSCompiler doesn't support recursive loops")

        # try to figure out if we have an extended loop.  An extended loop
        # is necessary if the loop is in recursive mode or if the special loop
        # variable is accessed in the body.
        extended_loop = jinja2.compiler.find_undeclared(node.body, ('loop',))

        # JavaScript for loops don't change namespace
        loop_frame = frame.soft()

        loop = loop_frame.current_loop = loop_frame.new_loop(node)

        self.writeline('var %s = ' % loop.list)
        self.visit(node.iter, loop_frame)
        self.write(';')

        self.writeline('var %s = %s.length;' % (loop.length, loop.list))

        self.writeline('for (var %(idx)s = 0; %(idx)s < %(len)s; ++%(idx)s) {' % {
            'idx': loop.index,
            'len': loop.length,
        })
        self.indent()
        self.writeline('var %s = %s[%s];' % (loop.name, loop.list, loop.index))

        if extended_loop:
            loop_frame.identifiers.add_special("loop")

        for name in node.find_all(jinja2.nodes.Name):
            if name.ctx == "store" and name.name == "loop":
                msg = ("Can't assign to special loop variable in for-loop "
                       "target")
                raise TemplateAssertionError(msg, name.lineno, self.name,
                                             self.filename)

        self.blockvisit(node.body, loop_frame)
        self.outdent()
        self.writeline("}")

        if node.else_:
            self.writeline("if (!%s) {" % loop.length)
            self.indent()
            self.blockvisit(node.else_, frame)
            self.outdent()
            self.writeline("}")

    def function_scoping(self, node, frame, children=None):
        if children is None:
            children = node.iter_child_nodes()

        func_frame = frame.inner()
        func_frame.inspect(children)

        # variables that are undeclared (accessed before declaration) and
        # declared locally *and* part of an outside scope raise a template
        # assertion error. Reason: we can't generate reasonable code from
        # it without aliasing all the variables.
        # this could be fixed in Python 3 where we have the nonlocal
        # keyword or if we switch to bytecode generation
        overriden_closure_vars = (
            func_frame.identifiers.undeclared &
            func_frame.identifiers.declared &
            (func_frame.identifiers.declared_locally |
             func_frame.identifiers.declared_parameter)
        )
        if overriden_closure_vars:
            tmpl = ("It's not possible to set and access variables "
                    "derived from an outer scope! (affects: %s)")
            msg = tmpl % (", ".join(sorted(overriden_closure_vars)),
                          node.lineno)
            raise TemplateAssertionError(msg, node.lineno, self.name,
                                         self.filename)

        # remove variables from a closure from the frame's undeclared
        # identifiers.
        func_frame.identifiers.undeclared -= (
            func_frame.identifiers.undeclared &
            func_frame.identifiers.declared
        )

        # Handle special variables.
        if "caller" in func_frame.identifiers.undeclared:
            func_frame.identifiers.undeclared.discard("caller")
            func_frame.reassigned_names["caller"] = "__data.__caller"

        return func_frame

    def macro_body(self, name, node, frame, children=None):
        frame = self.function_scoping(node, frame, children=children)

        self.writeline("%s.%s = function(__data) {" % (self.namespace, name))
        self.indent()

        num_defaults = len(node.defaults)
        num_required = len(node.args) - num_defaults

        # Assign local variables for each required parameter.
        for arg in node.args[:num_required]:
            frame.assigned_names.add(arg.name)
            self.writeline('var %s = __data.%s;' % (arg.name, arg.name))
            self.writeline('goog.asserts.assert(goog.isDef(%s), "Required parameter not provided: %s");' % (arg.name, arg.name))

        # Assign local variables for each optional parameter, specifying its default.
        for arg, default in zip(node.args[num_required:], node.defaults):
            frame.assigned_names.add(arg.name)
            self.writeline('var %s = goog.isDef(__data.%s) ? __data.%s : ' % (arg.name, arg.name, arg.name))
            self.visit(default, frame)
            self.write(';')

        self.writeline_startoutput(node, frame)
        self.blockvisit(node.body, frame)
        self.writeline_endoutput(node, frame)
        self.outdent()
        self.writeline("};")

    def caller_body(self, name, node, frame, children):
        """Caller is a local function and doesn't belong is the general NS"""
        self.writeline("%s = function() {" % name)
        self.indent()
        self.writeline_startoutput(node, frame)
        self.blockvisit(node.body, frame)
        self.writeline_endoutput(node, frame)
        self.outdent()
        self.writeline("};")

    def visit_Macro(self, node, frame):
        name = node.name
        self.macro_body(name, node, frame)
        frame.assigned_names.add("%s" % (name))

    def visit_CallBlock(self, node, frame):
        # node.call
        # node.body
        # Add the caller function to the macro.
        # XXX - Make sure we don't have a namespace cnoflict here.
        children = node.iter_child_nodes(exclude=("call",))
        self.caller_body("func_caller", node, frame, children=children)

        # call the macro passing in the caller method
        self.writeline_outputappend(node, frame)

        self.visit(node.call, frame, forward_caller="func_caller")
        self.write(";")

    def visit_Call(self, node, frame, forward_caller=None):
        # function symbol to call
        dotted_name = []
        call_frame = frame.soft()
        call_frame.escaped = True
        self.visit(node.node, call_frame, dotted_name=dotted_name)
        func_name = ".".join(dotted_name)

        macro = frame.identifiers.macros.get(func_name)
        if macro:
            macro.call_signature(self, node, frame)
            return

        if func_name in self.options['js_functions']:
            func = self.options['js_functions'][func_name]
            func.call_signature(self, node, frame)
            return

        log.debug('Undefined function %r' % func_name)

    def visit_Assign(self, node, frame):
        if isinstance(node.node, jinja2.nodes.Name) \
        and node.node.name == 'loop' \
        and 'loop' in frame.identifiers.declared:
            frame.declared_loops[node.target.name] = frame.current_loop
            return

        # XXX - test that we don't override any variable names doing this
        self.newline(node)

        local_ids = frame.identifiers.declared_locally
        name = node.target.name

        if name in local_ids and name not in frame.assigned_names:
            frame.assigned_names.add(name)
            self.write("var ")

        self.visit(node.target, frame)
        self.write(" = ")
        self.visit(node.node, frame)
        self.write(";")

    def visit_CondExpr(self, node, frame):
        self.visit(node.test, frame)
        self.write(' ? ')
        self.visit(node.expr1, frame)
        self.write(' : ')
        # XXX - should this allow undefined else clauses? it's tough to
        #       really judge what the correct behaviour should be, but
        #       I have chosen an empty string since it is falsy and won't
        #       be printed if that's what the value is ultimately used for.
        if node.expr2:
            self.visit(node.expr2, frame)
        else:
            self.write("''")

_pre_tag_whitespace = re.compile(r'\s*<')
_post_tag_whitespace = re.compile(r'>\s*')
_excess_whitespace = re.compile(r'\s\s+')

def strip_html_whitespace(value):
    value = _pre_tag_whitespace.sub('<', value)
    value = _post_tag_whitespace.sub('>', value)
    return _excess_whitespace.sub(' ', value)


def default_options():
    return {
        'js_functions': [],
        'js_indentation': '    ',
        'strip_html_whitespace': False,
    }

def generate(environment, name, filename, options=None):
    """Generate the javascript source for jinja template."""
    src, path, uptodate = environment.loader.get_source(environment, filename)
    node = environment.parse(src)

    return _generate(node, environment, name, filename, options=None)


def generate_from_string(environment, src, options=None):
    node = environment.parse(src)

    return _generate(node, environment, "", "")


def _generate(node, environment, name, filename, options=None):
    if options is None:
        options = {}
    for key, value in default_options().items():
        options.setdefault(key, value)

    generator = CodeGenerator(environment, options, name, filename)
    generator.visit(node)
    return generator.stream.getvalue()
