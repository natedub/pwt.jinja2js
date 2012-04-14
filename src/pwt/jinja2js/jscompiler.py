import re

from cStringIO import StringIO

from jinja2.visitor import NodeVisitor
import jinja2.nodes
import jinja2.compiler
from jinja2.utils import escape


BINOPERATORS = {
    "and": "&&",
    "or":  "||",
    }

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
    ## "in":    "in",
    ## "notin": "not in"
    }


class JSFrameIdentifierVisitor(jinja2.compiler.FrameIdentifierVisitor):

    def __init__(self, identifiers, environment, ctx):
        # Manually setup the identifiers as older version of Jinja2 required
        # a hard_scope argument. So to work with older version just set the
        # hard_scope argument manually here compensate. It is not used
        # within the JS compiler.
        self.identifiers = identifiers
        self.hard_scope = False

        self.environment = environment
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
        self.identifiers.declared_locally.add(
            ("%s" % (node.name)).encode("utf-8"))

    def visit_Import(self, node):
        # register import target as declare_locally
        super(JSFrameIdentifierVisitor, self).visit_Import(node)

    # def visit_FromImport(self, node):

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

    def __init__(self, environment, eval_ctx, parent=None):
        super(JSFrame, self).__init__(eval_ctx, parent)

        # map local variables to imported code
        self.identifiers.imports = {}

        self.environment = environment

        # mapping of visit_Name callback to reassign variable names for use
        # in 'for' loops
        self.reassigned_names = {}

        # name -> method mapping for handling special variables in the
        # for loop
        self.forloop_buffer = None

        # Track if we are escaping some output
        self.escaped = False

    def inspect(self, nodes):
        """Walk the node and check for identifiers.  If the scope is hard (eg:
        enforce on a python level) overrides from outer scopes are tracked
        differently.
        """
        visitor = JSFrameIdentifierVisitor(
            self.identifiers, self.environment, self.eval_ctx)
        for node in nodes:
            visitor.visit(node)

    def inner(self):
        frame = JSFrame(self.environment, self.eval_ctx, self)
        frame.identifiers.imports = self.identifiers.imports
        return frame


class Concat(object):

    def __init__(self, environment=None):
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
        self._indentation_text = getattr(environment, 'js_indentation', '    ')

    # Copied
    def indent(self):
        """Indent by one."""
        self._indentation += 1

    # Copied
    def outdent(self, step=1):
        """Outdent by step."""
        self._indentation -= step

    # Modified
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

    # Copied
    def writeline(self, x, node=None, extra=0):
        """Combination of newline and write."""
        self.newline(node, extra)
        self.write(x)

    def mark(self, node):
        # Mark the current output to correspond to the node.
        if node is not None and node.lineno != self._last_line:
            self._write_debug_info = node.lineno
            self._last_line = node.lineno

    # Modified
    def newline(self, node=None, extra=0):
        """Add one or more newlines before the next write."""
        self._new_lines = max(self._new_lines, 1 + extra)
        self.mark(node)

    def writeline_startoutput(self, node, frame):
        self.writeline("var output = '';", node)

    def writeline_endoutput(self, node, frame):
        self.writeline("return output;", node)

    def writeline_outputappend(self, node, frame):
        self.writeline("output += ", node)

    def write_outputappend_add(self, node, frame):
        self.write(" + ")

    def write_outputappend_end(self, node, frame):
        self.write(";")

    def write_htmlescape(self, node, frame):
        self.write("soy.$$escapeHtml(")

    def write_htmlescape_end(self, node, frame):
        self.write(")")


class BaseCodeGenerator(NodeVisitor):

    def __init__(self, environment, name, filename):
        super(BaseCodeGenerator, self).__init__()

        self.environment = environment
        self.name = name
        self.filename = filename

    def blockvisit(self, nodes, frame):
        """
        Visit a list of noes ad block in a frame. Some times we want to
        pass lists to the the visit method. Get around this here.
        """
        # if frame.buffer
        for node in nodes:
            self.visit(node, frame)


class CodeGenerator(BaseCodeGenerator):

    def __init__(self, environment, name, filename):
        super(CodeGenerator, self).__init__(environment, name, filename)
        self.writer = Concat()

    def visit_Template(self, node):
        """
        Setup the template output.

        Includes imports, macro definitions, etc.
        """

        have_extends = node.find(jinja2.nodes.Extends) is not None
        if have_extends:
            raise ValueError("JSCompiler doesn't support extends")

        have_blocks = node.find(jinja2.nodes.Block) is not None
        if have_blocks:
            raise ValueError("JSCompiler doesn't support blocks")

        eval_ctx = jinja2.nodes.EvalContext(self.environment, self.name)
        eval_ctx.encoding = "utf-8"

        # process the root
        frame = JSFrame(self.environment, eval_ctx)
        frame.inspect(node.body)
        frame.toplevel = frame.rootlevel = True

        self.blockvisit(node.body, frame)

    def visit_Import(self, node, frame):
        self.writer.mark(node)

    def visit_Macro(self, node, frame):
        generator = MacroCodeGenerator(
            self.environment,
            self.writer.__class__(self.environment),
            self.name,
            self.filename)
        generator.visit(node, frame)

        self.writer.write(generator.writer.stream.getvalue())

    def visit_TemplateData(self, node, frame):
        self.writer.mark(node)
        self.writer.write(node.data)


class ConcatCodeGenerator(CodeGenerator):

    def __init__(self, environment, name, filename):
        super(ConcatCodeGenerator, self).__init__(environment, name, filename)


STRINGBUILDER = "StringBuilder"
CONCAT = "Concat"


class MacroCodeGenerator(BaseCodeGenerator):
    # split out the macro code generator. This generate the guts of the
    # JavaScript we need to render the templates. Note that we do this
    # here seperate from the template generator above as we want to restrict
    # the Jinja2 template syntax for the JS implementation and we want to
    # format the generate code a bit like the templates. Gaps between
    # templates, comments should be displayed in the JS file. We need them for
    # any closure compiler hints we may want to put in.

    def __init__(self, environment, writer, name, filename):
        super(MacroCodeGenerator, self).__init__(environment, name, filename)

        self.writer = writer

    def visit_Output(self, node, frame):
        # JS is only interested in macros etc, as all of JavaScript
        # is rendered into the global namespace so we need to ignore data in
        # the templates that is out side the macros.
        if frame.toplevel:
            return

        finalize = str  # unicode

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
                    self.writer.writeline_outputappend(node, frame)
                    start = False
                else:
                    self.writer.write_outputappend_add(node, frame)
                if getattr(self.environment, "strip_html_whitespace", False):
                    item = [strip_html_whitespace(itemhtml)
                            for itemhtml in item]
                self.writer.write(repr("".join(item)))
            else:
                # This is a non-data node.
                # If we are using the string builder then we generate slightly
                # different code then concat.
                if self.writer.__class__.__name__ == STRINGBUILDER:
                    if isinstance(item, jinja2.nodes.Call):
                        # XXX - If we are a macro then we must end the
                        # appending of the output.
                        if not item.args:
                            if not start:
                                self.writer.write_outputappend_end(item, frame)
                                start = True
                            self.writer.newline(item)
                            self.visit(item, frame)
                            self.writer.write(";")
                            continue

                if start:
                    self.writer.writeline_outputappend(item, frame)
                    start = False
                else:
                    self.writer.write_outputappend_add(item, frame)

                # autoescape, safe, and escape
                if isinstance(item, jinja2.nodes.Filter):
                    if item.name == "safe":
                        self.visit(item.node, frame)
                        continue

                if frame.eval_ctx.autoescape:
                    self.writer.write_htmlescape(node, frame)
                    escaped_frame = frame.soft()
                    escaped_frame.escaped = True

                    self.visit(item, escaped_frame)

                    self.writer.write_htmlescape_end(node, frame)
                else:
                    self.visit(item, frame)

        if not start:
            self.writer.write_outputappend_end(node, frame)

    def visit_Filter(self, node, frame):
        # safe attribute with autoesacape is handled in visit_Output
        if node.name == "escape":
            if node.kwargs:
                raise Exception("No kwargs")

            if not frame.escaped:
                self.writer.write_htmlescape(node, frame)
                frame = frame.soft()
                frame.escaped = True
                self.visit(node.node, frame)
                self.writer.write_htmlescape_end(node, frame)
            else:
                self.visit(node.node, frame)
        elif node.name in FILTERS:
            kwargs = {}
            for kwarg in node.kwargs:
                kwargs[kwarg.key] = kwarg.value

            FILTERS[node.name](self, node, frame, *node.args, **kwargs)
        else:
            raise jinja2.compiler.TemplateAssertionError(
                "Filter does not exist: '%s'" % node.name,
                node.lineno, self.name, self.filename)

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
            self.writer.write(output)
        else:
            dotted_name.append(output)

        return False

    def visit_List(self, node, frame):
        self.writer.write("[")
        for idx, item in enumerate(node.items):
            if idx:
                self.writer.write(", ")
            self.visit(item, frame)
        self.writer.write("]")

    def visit_Dict(self, node, frame):
        self.writer.write("{")
        for idx, item in enumerate(node.items):
            if idx:
                self.writer.write(", ")

            # item.key should be a constant string. Otherwise how do you
            # get to output a dictionary with a variable key string?
            # So it is either a `Const` or `Name` node.
            if isinstance(item.key, jinja2.nodes.Const):
                if "." in item.key.value:
                    raise jinja2.compiler.TemplateAssertionError(
                        "My templates get confused when you try and create a"
                        " dictionary with a key with a dot in it.",
                        item.key.lineno, self.name, self.filename)
                self.writer.write(item.key.value)
            elif isinstance(item.key, jinja2.nodes.Name):
                self.writer.write(item.key.name)
            else:
                raise jinja2.compiler.TemplateAssertionError(
                    "Dictionary keys must be constant.",
                    item.key.lineno, self.name, self.filename)

            self.writer.write(": ")
            self.visit(item.value, frame)

        self.writer.write("}")

    def visit_Name(self, node, frame, dotted_name=None):
        # declared_parameter
        # declared
        # outer_undeclared
        # declared_locally
        # undeclared
        name = node.name
        isparam = False

        ids = frame.identifiers
        if name in ids.declared_parameter or name in ids.outer_undeclared:
            output = "__data." + name
            isparam = True
        elif frame.parent is not None and \
               name in frame.parent.identifiers.declared_parameter:
            # Once we have tried any local variables we need to check
            # the parent if we have a declared parameter from there
            output = '__data.' + name

            isparam = True
        elif name in frame.reassigned_names:
            output = frame.reassigned_names[name]

            isparam = True
        elif name in frame.identifiers.declared or \
                 name in frame.identifiers.declared_locally:
            output = name

        elif name in ids.imports:
            # This is an import.
            output = ids.imports[name]

            frame.assigned_names.add(ids.imports[name])
        else:
            if dotted_name is None:
                raise jinja2.compiler.TemplateAssertionError(
                    "Variable '%s' not defined" % name,
                    node.lineno, self.name, self.filename)

            output = name

        if dotted_name is None:
            self.writer.write(output)
        else:
            dotted_name.append(output)

        return isparam

    def visit_Getitem(self, node, frame):
        # Careful, there is something in Jinja2 about node.arg extending
        # jinja2.nodes.Slice
        self.visit(node.node, frame)
        self.writer.write("[")
        self.visit(node.arg, frame)
        self.writer.write("]")

    def visit_Getattr(self, node, frame, dotted_name=None):
        # We only need to check when `loop` is the first name-space in the
        # Getattr node. Sometimes we have more then one level name-spaces and
        # we are inside a for loop, likely when we are calling other macros.
        if frame.forloop_buffer and getattr(node.node, "name", None) == "loop":
            if node.attr == "index0":
                self.writer.write("%sIndex" % frame.forloop_buffer)
            elif node.attr == "index":
                self.writer.write("%sIndex + 1" % frame.forloop_buffer)
            elif node.attr == "revindex0":
                self.writer.write("%sListLen - %sIndex"
                                  % (frame.forloop_buffer,
                                     frame.forloop_buffer))
            elif node.attr == "revindex":
                self.writer.write("%sListLen - %sIndex - 1"
                                  % (frame.forloop_buffer,
                                     frame.forloop_buffer))
            elif node.attr == "first":
                self.writer.write("%sIndex == 0" % frame.forloop_buffer)
            elif node.attr == "last":
                self.writer.write("%sIndex == (%sListLen - 1)"
                                  % (frame.forloop_buffer,
                                     frame.forloop_buffer))
            elif node.attr == "length":
                self.writer.write("%sListLen" % frame.forloop_buffer)
            else:
                raise AttributeError("loop.%s not defined" % node.attr)
        else:
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
                self.writer.write(".".join(dotted_name))

    def binop(operator):
        def visitor(self, node, frame):
            self.writer.write("(")
            self.visit(node.left, frame)
            self.writer.write(" %s " % BINOPERATORS.get(operator, operator))
            self.visit(node.right, frame)
            self.writer.write(")")
        return visitor

    # Math operators
    visit_Add = binop("+")
    visit_Sub = binop("-")
    visit_Mul = binop("*")
    visit_Div = binop("/")

    def visit_FloorDiv(self, node, frame):
        self.writer.write("Math.floor(")
        self.visit(node.left, frame)
        self.writer.write(" / ")
        self.visit(node.right, frame)
        self.writer.write(")")

    def visit_Pow(self, node, frame):
        self.writer.write("Math.pow(")
        self.visit(node.left, frame)
        self.writer.write(", ")
        self.visit(node.right, frame)
        self.writer.write(")")

    visit_Mod = binop("%")
    visit_And = binop("and")
    visit_Or = binop("or")

    def uaop(operator):
        def visitor(self, node, frame):
            self.writer.write("(" + UNARYOP.get(operator, operator))
            self.visit(node.node, frame)
            self.writer.write(")")
        return visitor

    visit_Pos = uaop("+")
    visit_Neg = uaop("-")
    visit_Not = uaop("not ")

    visit_And = binop("and")
    visit_Or = binop("or")

    del binop, uaop

    def visit_Compare(self, node, frame):
        self.visit(node.expr, frame)
        # XXX - ops is a list. Can we have a list of comparisons
        for op in node.ops:
            self.visit(op, frame)

    def visit_Operand(self, node, frame):
        if node.op not in OPERATORS:
            raise jinja2.compiler.TemplateAssertionError(
                "Comparison operator '%s' not supported in JavaScript",
                node.lineno, self.name, self.filename)
        self.writer.write(" %s " % OPERATORS[node.op])
        self.visit(node.expr, frame)

    def visit_If(self, node, frame):
        if_frame = frame.soft()
        self.writer.writeline("if (", node)
        self.visit(node.test, if_frame)
        self.writer.write(") {")

        self.writer.indent()
        self.blockvisit(node.body, if_frame)
        self.writer.outdent()

        if node.else_:
            self.writer.writeline("} else {")
            self.writer.indent()
            self.blockvisit(node.else_, if_frame)
            self.writer.outdent()

        self.writer.writeline("}")

    def visit_For(self, node, frame):
        node.iter_child_nodes(exclude=("iter",))

        if node.recursive:
            raise NotImplementedError(
                "JSCompiler doesn't support recursive loops")

        # try to figure out if we have an extended loop.  An extended loop
        # is necessary if the loop is in recursive mode or if the special loop
        # variable is accessed in the body.
        extended_loop = "loop" in jinja2.compiler.find_undeclared(
            node.iter_child_nodes(only=("body",)), ("loop",))

        # JavaScript for loops don't change namespace
        loop_frame = frame.soft()

        if extended_loop:
            loop_frame.identifiers.add_special("loop")
            loop_frame.forloop_buffer = node.target.name
        for name in node.find_all(jinja2.nodes.Name):
            if name.ctx == "store" and name.name == "loop":
                raise jinja2.compiler.TemplateAssertionError(
                    "Can't assign to special loop variable in for-loop target",
                    name.lineno, self.name, self.filename)

        self.writer.writeline("var %sList = " % node.target.name)
        self.visit(node.iter, loop_frame)
        self.writer.write(";")

        self.writer.writeline("var %(name)sListLen = %(name)sList.length;"
                              % {"name": node.target.name})
        if node.else_:
            self.writer.writeline("if (%sListLen > 0) {" % node.target.name)
            self.writer.indent()

        self.writer.writeline("for (var %(name)sIndex = 0; %(name)sIndex <"
                              " %(name)sListLen; %(name)sIndex++) {"
                              % {"name": node.target.name})
        self.writer.indent()

        self.writer.writeline("var %(name)sData = %(name)sList[%(name)sIndex];"
                              % {"name": node.target.name})
        loop_frame.reassigned_names[node.target.name] =\
                "%sData" % node.target.name
        self.blockvisit(node.body, loop_frame)
        self.writer.outdent()
        self.writer.writeline("}")

        if node.else_:
            self.writer.outdent()
            self.writer.writeline("} else {")
            self.writer.indent()
            self.blockvisit(node.else_, frame)
            self.writer.outdent()
            self.writer.writeline("}")

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
            raise jinja2.compiler.TemplateAssertionError(
                "It's not possible to set and access variables "
                "derived from an outer scope! (affects: %s)" % (
                    ", ".join(sorted(overriden_closure_vars)), node.lineno),
                    node.lineno, self.name, self.filename)

        # remove variables from a closure from the frame's undeclared
        # identifiers.
        func_frame.identifiers.undeclared -= (
            func_frame.identifiers.undeclared &
            func_frame.identifiers.declared
        )

        # Handle special variables.
        if "caller" in func_frame.identifiers.undeclared:
            func_frame.identifiers.undeclared.discard("caller")
            func_frame.reassigned_names["caller"] = "__caller"

        return func_frame

    def macro_body(self, name, node, frame, children=None):
        frame = self.function_scoping(node, frame, children=children)

        self.writer.writeline("%s = function() {" % name)
        self.writer.indent()
        self.writer.writeline("var __arg_len = arguments.length;")
        self.writer.writeline("var __caller = __arg_len > 0 && typeof(arguments[__arg_len-1]) === 'function' ? arguments.pop() : null;")

        if node.args:
            self.writer.writeline("var __data = {")
            js_args = []
            for i in xrange(len(node.args)):
                arg = node.args[i]
                js_args.append("%s: arguments[%d]" % (arg.name, i))
            self.writer.write(", ".join(js_args))
            self.writer.write("};")
        self.writer.writeline_startoutput(node, frame)
        self.blockvisit(node.body, frame)
        self.writer.writeline_endoutput(node, frame)
        self.writer.outdent()
        self.writer.writeline("};")

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
        self.macro_body("func_caller", node, frame, children=children)

        # call the macro passing in the caller method
        if self.writer.__class__.__name__ == STRINGBUILDER:
            self.writer.newline(node)
        elif self.writer.__class__.__name__ == CONCAT:
            self.writer.writeline_outputappend(node, frame)
        else:
            # XXX - we shouldn't get here
            raise jinja2.compiler.TemplateAssertionError(
                "Unknown writer class", node.lineno, self.name, self.filename)

        self.visit(node.call, frame, forward_caller="func_caller")
        self.writer.write(";")

    def signature(self, node, frame, forward_caller):
        if node.args and node.kwargs:
            raise jinja2.compiler.TemplateAssertionError(
                "Function call with positional and keyword arguments "
                "are not allowed", node.lineno, self.name, self.filename)

        if node.dyn_args or node.dyn_kwargs:
            raise jinja2.compiler.TemplateAssertionError(
                "JS Does not support positional or keyword arguments",
                node.lineno, self.name, self.filename)

        if node.args:
            # We have only positional arguments here. In this case we assume
            # that we have an ordinary Java Script function we wish to call
            start_arg = True
            for arg in node.args:
                if not start_arg:
                    self.writer.write(", ")
                self.visit(arg, frame)
                start_arg = False

            # Since this is a ordinary call bail out
            return

        # Now assume that we are calling an other macro
        # XXX - we should be able test this by looking up the environment to
        # see if that is the case.

        start_kw = True
        for kwarg in node.kwargs:
            if not start_kw:
                self.writer.write(", ")
            self.visit(kwarg.value, frame)
            start_kw = False

        if forward_caller is not None:
            if self.writer.__class__.__name__ == CONCAT:
                # XXX - This is a hack to get around inconsistencies
                # between the two different styles.
                self.writer.write(", null")

            self.writer.write(", ")
            self.writer.write(forward_caller)

    def visit_Call(self, node, frame, forward_caller=None):
        # function symbol to call
        dotted_name = []
        self.visit(node.node, frame, dotted_name=dotted_name)
        func_name = ".".join(dotted_name)

        # Like signature(), this assumes that function calls with only
        # positional arguments are calls to javascript functions. This
        # allows you to call differently named functions in the client JS
        # than when rendering a template on the server.
        if node.args and not node.kwargs \
               and func_name in getattr(self.environment, "js_func_aliases",
                                        []):
            func_name = self.environment.js_func_aliases[func_name]

        # function signature
        self.writer.write("%s(" % func_name)
        self.signature(node, frame, forward_caller)
        self.writer.write(")")

    def visit_Assign(self, node, frame):
        # XXX - test that we don't override any variable names doing this
        self.writer.newline(node)
        self.visit(node.target, frame)
        self.writer.write(" = ")
        self.visit(node.node, frame)
        self.writer.write(";")

    def visit_CondExpr(self, node, frame):
        self.visit(node.test, frame)
        self.writer.write(' ? ')
        self.visit(node.expr1, frame)
        self.writer.write(' : ')
        # XXX - should this allow undefined else clauses? it's tough to
        #       really judge what the correct behaviour should be, but
        #       I have chosen an empty string since it is falsy and won't
        #       be printed if that's what the value is ultimately used for.
        if node.expr2:
            self.visit(node.expr2, frame)
        else:
            self.writer.write("''")

_pre_tag_whitespace = re.compile(r'\s*<')
_post_tag_whitespace = re.compile(r'>\s*')
_excess_whitespace = re.compile(r'\s\s+')


def strip_html_whitespace(value):
    value = _pre_tag_whitespace.sub('<', value)
    value = _post_tag_whitespace.sub('>', value)
    return _excess_whitespace.sub(' ', value)

FILTERS = {}


class register_filter(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        FILTERS[self.name] = func

        return func


@register_filter("default")
def filter_default(generator, node, frame, default_value=""):
    generator.writer.write("(")
    generator.visit(node.node, frame)
    generator.writer.write(" ? ")
    generator.visit(node.node, frame)
    generator.writer.write(" : ")
    generator.visit(default_value, frame)
    generator.writer.write(")")


@register_filter("truncate")
def filter_truncate(generator, node, frame, length):
    generator.visit(node.node, frame)
    generator.writer.write(".substring(0, ")
    generator.visit(length, frame)
    generator.writer.write(")")


@register_filter("capitalize")
def filter_capitalize(generator, node, frame):
    generator.visit(node.node, frame)
    generator.writer.write(".substring(0, 1).toUpperCase()")
    generator.writer.write_outputappend_add(node, frame)
    generator.visit(node.node, frame)
    generator.writer.write(".substring(1)")


@register_filter("last")
def filter_last(generator, node, frame):
    generator.visit(node.node, frame)
    generator.writer.write(".pop()")


@register_filter("length")
def filter_length(generator, node, frame):
    generator.visit(node.node, frame)
    generator.writer.write(".length")


@register_filter("replace")
def filter_replace(generator, node, frame, old, new):
    generator.visit(node.node, frame)
    generator.writer.write(".replace(")
    generator.visit(old, frame)
    generator.writer.write(", ")
    generator.visit(new, frame)
    generator.writer.write(")")


@register_filter("round")
def filter_round(generator, node, frame, precision=jinja2.nodes.Const(0)):
    # get precision
    precision_value = []
    generator.visit(precision, frame, precision_value)
    precision = ".".join(precision_value)
    try:
        precision = 10 ** int(precision)
    except ValueError:
        # assume we are a parameter or declared variable and raise to power
        # of 10
        precision = "Math.pow(10, %s)" % precision

    generator.writer.write("Math.round(")
    generator.visit(node.node, frame)
    if precision > 1:
        generator.writer.write(" * %s" % precision)
    generator.writer.write(")")
    if precision > 1:
        generator.writer.write(" / %s" % precision)


def _generate(node, generator):
    if not isinstance(node, jinja2.nodes.Template):
        raise TypeError("Can't compile non template nodes")

    generator.visit(node)
    return generator.writer.stream.getvalue()


def generate(node, environment, name, filename):
    """Generate the python source for a node tree."""
    generator = CodeGenerator(environment, name, filename)
    return _generate(node, generator)
