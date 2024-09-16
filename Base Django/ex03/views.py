from django.shortcuts import render


def generate_gradient(color, steps):
  gradient = []
  r, g, b = color
  for step in range(steps):
    factor = step / steps
    new_color = (
      int(r + (255 - r) * factor),
      int(g + (255 - g) * factor),
      int(b + (255 - b) * factor)
    )
    gradient.append(f"#{new_color[0]:02x}{new_color[1]:02x}{new_color[2]:02x}")
  return gradient


def index(request):
  white = (0, 0, 0)
  red = (255, 0, 0)
  blue = (0, 0, 255)
  green = (0, 255, 0)

  steps = 50
  black_to_white = generate_gradient(white, steps)
  red_to_white = generate_gradient(red, steps)
  blue_to_white = generate_gradient(blue, steps)
  green_to_white = generate_gradient(green, steps)

  table = []
  for i in range(steps):
    table.append([black_to_white[i], red_to_white[i], blue_to_white[i], green_to_white[i]])

  return render(request, 'ex03/index.html', {'table': table})
