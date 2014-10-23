import jinja2.ext

from jinja2js import nodes

class Namespace(jinja2.ext.Extension):
    """
    [Token(1, 'name', 'examples'),
     Token(1, 'dot', u'.'),
     Token(1, 'name', 'const'),
     Token(1, 'block_end', u'%}')
     ]
    """

    tags = set(['namespace'])

    def parse(self, parser):
        node = nodes.NamespaceNode(lineno=next(parser.stream).lineno)
        namespace = []
        while not parser.is_tuple_end():
            namespace.append(parser.stream.next().value)
        node.namespace = ''.join(namespace)
        return node
