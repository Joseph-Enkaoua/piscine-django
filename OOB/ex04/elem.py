#!/usr/bin/python3


class Text(str):
    """
    A Text class to represent a text you could use with your HTML elements.

    Because directly using str class was too mainstream.
    """

    def __str__(self):
        return super().__str__().replace('\n', '\n<br />\n')


class Elem:
    class ValidationError(Exception):
        def __init__(self) -> None:
            super().__init__("Validation didn't pass, inccorect behavior.")

    def __init__(self, name=None, tag='div', attr={}, content=None, tag_type='double'):
        if tag_type != 'double' and tag_type != 'simple':
            raise Elem.ValidationError
        if not (self.check_type(content) or content is None):
            raise Elem.ValidationError
        self.content = []
        if type(content) == list:
            self.content = content
        elif content:
            self.content.append(content)
        self.name = name
        self.tag = tag
        self.attr = attr
        self.tag_type = tag_type

    def __str__(self):
        """
        The __str__() method will permit us to make a plain HTML representation
        of our elements.
        Make sure it renders everything (tag, attributes, embedded elements)
        """
        attr = self.__make_attr()
        result = '<{tag}{attr}'.format(tag=self.tag, attr=attr)
        if self.tag_type == 'double':
            content = self.__make_content()
            result += '>' + content + '</{tag}>'.format(tag=self.tag)
        elif self.tag_type == 'simple':
            result += '/>'
        return result

    def __make_attr(self):
        """
        Here is a function to render our elements attributes.
        """
        result = ''
        for pair in sorted(self.attr.items()):
            result += ' ' + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result

    def __make_content(self):
        """
        Here is a method to render the content, including embedded elements.
        """

        if len(self.content) == 0:
            return ''
        result = '\n'
        for elem in self.content:
            result += '  ' + str(elem).replace('\n', '\n  ') + '\n'
        return result

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        """
        Is this object a HTML-compatible Text instance or a Elem, or even a
        list of both?
        """
        return (isinstance(content, Elem) or type(content) == Text or
                (type(content) == list and all([type(elem) == Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))


def test():
    html = Elem(content=Elem(content=Elem(Text('TTT'))))
    print(html)

if __name__ == '__main__':
    test()
