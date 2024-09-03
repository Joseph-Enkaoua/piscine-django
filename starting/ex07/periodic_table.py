#!/usr/bin/python3

def parse_line_to_dict(line: str):
  name, properties = line.split('=', 1)

  properties = properties.strip()
  prop_dict = {'name': name.strip()}

  for prop in properties.split(','):
    key, value = prop.split(':', 1)
    prop_dict[key.strip()] = value.strip()

  return prop_dict


def create_table_body(positions_dict):
  rows = []

  for position, items in positions_dict.items():
    row_content = ""
    for item in items:
      row_content += f"""
      <td style="border: 1px solid black; padding:10px">
        <h4>{item['name']}</h4>
        <ul>No {item['number']}</ul>
        <ul>{item['small']}</ul>
        <ul>{item['molar']}</ul>
        <ul>{item['electron']} electron</ul>
      </td>
      """
    rows.append(f"<tr>{row_content}</tr>")

  return "\n".join(rows)


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
      table {{
        border-collapse: collapse;
      }}
      h4 {{
        text-align: center;
      }}
      ul {{
        list-style:none;
        padding-left:0px;
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

    positions_dict = {}

    with open('periodic_table.txt', 'r') as f:
      for line in f:
        if line.strip():
          line_dict = parse_line_to_dict(line)
          position = line_dict['position']
          if position not in positions_dict:
            positions_dict[position] = []
          positions_dict[position].append(line_dict)

    sorted_positions = dict(sorted(positions_dict.items(), key=lambda x: int(x[0])))

    body = create_table_body(sorted_positions)

    with open('periodic_table.html', 'w') as f:
        f.write(HTML.format(body=body))


if __name__ == '__main__':
    main()
