#!/usr/bin/python3

def parse_line_to_dict(line: str):
  name, properties = line.split('=', 1)

  properties = properties.strip()
  prop_dict = {'name': name.strip()}

  for prop in properties.split(','):
    key, value = prop.split(':', 1)
    prop_dict[key.strip()] = value.strip()

  return prop_dict


def add_row_to_table(row_dict, body):
  TEMPLATE = """
      <tr>
        <td style="border: 1px solid black; padding:10px">
          <h4>{name}</h4>
          <ul>No {number}</ul>
          <ul>{small}</ul>
          <ul>{molar}</ul>
          <ul>{electron} electron</ul>
          </ul>
        </td>
      </tr>
"""

  body += TEMPLATE.format(
    name=row_dict['name'],
    number=row_dict['number'],
    small=row_dict['small'],
    molar=row_dict['molar'],
    electron=row_dict['electron']
  )

  return body


def main():
  HTML = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>periodic_table</title>
    <style>
      table{{
        border-collapse: collapse;
      }}
      h4 {{
        text-align: center;
      }}
      ul {{
        list-style:none;
        padding-left:0px;
      }}
      td {{
        border: 1px solid black;
        padding:10px;
      }}
    </style>
  </head>
  <body>
    <table>
      {body}
    </table>
  </body>
</html>
"""

  elements_dict = {}
  body = ""

  with open('periodic_table.txt', 'r') as f:
    for line in f:
      if line.strip():
        line_dict = parse_line_to_dict(line)
        elements_dict[line_dict['name']] = line_dict

    elements_dict = dict(sorted(elements_dict.items(), key=lambda x: int(x[1]['position'])))
    
  for _, entry in elements_dict.items():
    body = add_row_to_table(entry, body)

  with open('periodic_table.html', 'w') as f:
    f.write(HTML.format(body=body))


if __name__ == '__main__':
  main()
