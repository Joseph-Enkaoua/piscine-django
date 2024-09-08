#!/usr/bin/python3

from elements import Elem, Text, Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br


class Page:
  def __init__(self, elem: Elem):
    self.elem = elem

  def is_valid(self) -> bool:
    return self.is_elem_valid(self.elem)

  def __str__(self) -> str:
    if isinstance(self.elem, Html):
      return f"<!DOCTYPE html>\n{str(self.elem)}"
    else:
      return str(self.elem)

  def write_to_file(self, filename: str):
    with open(filename, 'w') as file:
      file.write(str(self))

  @staticmethod
  def html_head_body_check(elem) -> bool:
    if type(elem) == Html:
      found_head = False
      for content_elem in elem.content:
        if isinstance(content_elem, Head):
          found_head = True
        elif isinstance(content_elem, Body) and found_head:
          return True
      return False
    return True

  @staticmethod
  def table_row_check(elem) -> bool:
    if isinstance(elem, Tr):
      if all(isinstance(con, (Th, Td)) for con in elem.content) \
      and all(type(con) == type(elem.content[0]) for con in elem.content):
        return True
      return False
    return True

  @staticmethod
  def head_title_check(elem) -> bool:
    if isinstance(elem, Head):
      titles_found = 0
      for content_elem in elem.content:
        if isinstance(content_elem, Title):
          titles_found += 1
      if titles_found != 1:
        return False
    return True

  @staticmethod
  def list_check(elem) -> bool:
    if isinstance(elem, (Ul, Ol)):
      items_found = 0
      for con in elem.content:
        if isinstance(con, Li):
          items_found += 1
        else:
          return False
      if items_found < 1:
        return False
    return True

  def is_elem_valid(self, elem) -> bool:
    if not (isinstance(elem, (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li,
                       H1, H2, P, Div, Span, Hr, Br)) or type(elem) == Text):
      return False

    if Page.html_head_body_check(elem) == False:
      return False

    if Page.head_title_check(elem) == False:
      return False

    if Page.list_check(elem) == False:
      return False

    if Page.table_row_check(elem) == False:
      return False

    if isinstance(elem, (Body, Div)):
      if not all(isinstance(con, (H1, H2, Div, Table, Ul, Ol, Span, Text)) for con in elem.content):
        return False
    elif isinstance(elem, (Title, H1, H2, Li, Th, Td)):
      if not all(isinstance(con, Text) for con in elem.content):
        return False
    elif isinstance(elem, P) and not all(isinstance(con, Text) for con in elem.content):
      return False
    elif isinstance(elem, Span) and not all(isinstance(con, (Text, P)) for con in elem.content):
      return False
    elif isinstance(elem, Table) and not all(isinstance(con, Tr) for con in elem.content):
      return False

    if not isinstance(elem, Text):
      for content in elem.content:
        if not self.is_elem_valid(content):
          return False
    return True


def test():
    # Test case 1: Valid HTML structure (Html -> Head -> Title and Body)
    html_elem = Html([Head([Title(Text("Test Page"))]), Body([H1(Text("Heading"))])])
    page = Page(html_elem)
    assert page.is_valid() == True, "Test case 1 failed"
    print("Test case 1 passed")

    # Test case 2: Invalid HTML structure (Head without Title)
    html_elem = Html([Head(), Body([H1(Text("Heading"))])])
    page = Page(html_elem)
    assert page.is_valid() == False, "Test case 2 failed"
    print("Test case 2 passed")

    # Test case 3: Invalid HTML structure (Body before Head)
    html_elem = Html([Body([H1(Text("Heading"))]), Head([Title(Text("Test Page"))])])
    page = Page(html_elem)
    assert page.is_valid() == False, "Test case 3 failed"
    print("Test case 3 passed")

    # Test case 4: Valid Table with valid Tr and Td/Th
    table_elem = Table([Tr([Th(Text("Header1")), Th(Text("Header2"))]), Tr([Td(Text("Data1")), Td(Text("Data2"))])])
    page = Page(table_elem)
    assert page.is_valid() == True, "Test case 4 failed"
    print("Test case 4 passed")

    # Test case 5: Invalid Table (Tr contains invalid elements, such as Div)
    table_elem = Table([Tr([Th(Text("Header1")), Div()])])
    page = Page(table_elem)
    assert page.is_valid() == False, "Test case 5 failed"
    print("Test case 5 passed")

    # Test case 6: Valid list (Ul with Li elements)
    list_elem = Ul([Li(Text("Item1")), Li(Text("Item2"))])
    page = Page(list_elem)
    assert page.is_valid() == True, "Test case 6 failed"
    print("Test case 6 passed")

    # Test case 7: Invalid list (Ul contains non-Li elements)
    list_elem = Ul([Li(Text("Item1")), Div()])
    page = Page(list_elem)
    assert page.is_valid() == False, "Test case 7 failed"
    print("Test case 7 passed")

    # Test case 8: Span containing valid content (Text or P)
    span_elem = Span([Text("Some text"), P([Text("Paragraph text")])])
    page = Page(span_elem)
    assert page.is_valid() == True, "Test case 8 failed"
    print("Test case 8 passed")

    # Test case 9: Span containing invalid content (Table inside Span)
    span_elem = Span([Text("Some text"), Table()])
    page = Page(span_elem)
    assert page.is_valid() == False, "Test case 9 failed"
    print("Test case 9 passed")

    # Test case 10: Valid P element with Text content
    p_elem = P([Text("This is a paragraph.")])
    page = Page(p_elem)
    assert page.is_valid() == True, "Test case 10 failed"
    print("Test case 10 passed")

    # Test case 11: Invalid P element with non-Text content
    p_elem = P([Div()])
    page = Page(p_elem)
    assert page.is_valid() == False, "Test case 11 failed"
    print("Test case 11 passed")


if __name__ == "__main__":
    test()
