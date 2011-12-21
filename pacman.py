#!/usr/bin/env python

# Wentao Han (wentao.han@gmail.com)
# Logo of PACMAN Group, Tsinghua Univeristy

#   __
#  /  \ p1
# | p0<
#  \__/ p2

import math
import cairo

WIDTH, HEIGHT = 512, 512
LINE_WIDTH = 0.05
RADIUS = 0.45
START_ANGLE = math.radians(30)
END_ANGLE = math.radians(330)
BORDER_COLOR = (0.1, 0.1, 0.1)
INNER_COLOR = (236 / 255.0, 142 / 255.0, 255 / 255.0)

x0 = 0.5
y0 = 0.5
x1 = x0 + RADIUS * math.cos(START_ANGLE)
y1 = y0 + RADIUS * math.sin(START_ANGLE)
x2 = x0 + RADIUS * math.cos(END_ANGLE)
y2 = y0 + RADIUS * math.sin(END_ANGLE)

surface = cairo.PDFSurface('pacman.pdf', WIDTH, HEIGHT)
ctx = cairo.Context(surface)
ctx.scale(WIDTH / 1.0, HEIGHT / 1.0)

ctx.move_to(x0, y0)
ctx.line_to(x1, y1)
ctx.arc(x0, y0, RADIUS, START_ANGLE, END_ANGLE)
ctx.close_path()
path = ctx.copy_path()

ctx.set_source_rgb(INNER_COLOR[0], INNER_COLOR[1], INNER_COLOR[2])
ctx.set_line_width(LINE_WIDTH)
ctx.set_line_join(cairo.LINE_JOIN_ROUND)
ctx.fill()

ctx.append_path(path)
ctx.set_source_rgb(BORDER_COLOR[0], BORDER_COLOR[1], BORDER_COLOR[2])
ctx.stroke()

surface.write_to_png('pacman.png')
