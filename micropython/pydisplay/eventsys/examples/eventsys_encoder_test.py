"""
A simple test of an encoder in pydisplay.
"""

from board_config import display_drv, broker

color_byte = 1
bg_color = 0xFF00
w = display_drv.width
h = display_drv.height
thickness = 10
y_pos = h // 2
x_pos = w // 2
factor = -1  # change the sign to invert the direction


def draw_line():
    color = color_byte << 8 | color_byte
    display_drv.fill_rect(0, 0, x_pos, thickness, color)
    display_drv.fill_rect(x_pos, 0, w - x_pos, thickness, bg_color)


display_drv.vscsad(y_pos)
draw_line()

while True:
    if not (e := broker.poll()):
        continue
    if e.type == broker.Events.MOUSEWHEEL:
        if e.y != 0:
            direction = factor if e.y > 0 else -factor
            delta = e.y * e.y * direction  # Quadratic acceleration
            y_pos = (y_pos + delta) % h
            display_drv.vscsad(y_pos)
        if e.x != 0:
            direction = factor if e.x > 0 else -factor
            delta = e.x * e.x * direction
            x_pos = (x_pos + delta) % w
            draw_line()
    elif e.type == broker.Events.MOUSEBUTTONDOWN:
        if e.button == 2:
            color_byte = color_byte << 1 & 0xFF
            if color_byte == 0:
                color_byte = 1
            draw_line()
        elif e.button == 3:
            bg_color = ~bg_color
            draw_line()
