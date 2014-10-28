from jinja2.compiler import TemplateAssertionError

from jinja2js.compiler import JSFunction


class JSI18nBase(JSFunction):
    def kwargs_dict(self, gen, frame, kwargs, quote_keys):
        gen.write('{')
        for i, arg in enumerate(kwargs):
            if i > 0:
                gen.write(', ')
            key = "'%s'" % arg.key if quote_keys else arg.key
            gen.write("%s: ", key)
            gen.visit(arg.value, frame)
        gen.write('}')

class JSGettext(JSI18nBase):
    def call_signature(self, gen, node, frame):
        if len(node.args) != 1:
            raise TemplateAssertionError(
                'gettext requires one positional argument', 0)
        gen.write('%s(' % self.js_name)
        gen.visit(node.args[0], frame)
        if node.kwargs:
            gen.write(', ')
            self.kwargs_dict(gen, frame, node.kwargs, quote_keys=True)
        gen.write(')')

class JSNGettext(JSI18nBase):
    def call_signature(self, gen, node, frame):
        if len(node.args) != 3:
            raise TemplateAssertionError(
                'ngettext requires 3 positional arguments', 0)
        gen.write('%s(' % self.js_name)
        for i, arg in enumerate(node.args):
            if i > 0:
                gen.write(', ')
            gen.visit(arg, frame)
        if node.kwargs:
            gen.write(', ')
            self.kwargs_dict(gen, frame, node.kwargs, quote_keys=True)
        gen.write(')')
