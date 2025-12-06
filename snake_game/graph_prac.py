#Graphics animation

from graphics import *
import random


def win_background(title, width, height, color):
    var = GraphWin(title, width, height)
    var.setBackground(color)
    return var
def draw_circ(win, xcoord, ycoord, radius):
    circle = Circle(Point(xcoord, ycoord), radius)
    circle.draw(win)
    return circle
def draw_rec(win, p1x, p1y, p2x, p2y):
    rect = Rectangle(Point(p1x, p1y), Point(p2x, p2y))
    rect.draw(win)
    return rect
def draw_text(win, px, py, text, size = 12, style = "normal", color = "black"):
    msg = Text(Point(px, py), text)
    msg.setSize(size)
    msg.setStyle(style)
    msg.setTextColor(color)
    msg.draw(win)
    return msg
def get_shape_center(shape):
    if isinstance(shape, Circle):
        c = shape.getCenter()
        return c.getX(), c.getY(), shape.getRadius(), shape.getRadius()
    elif isinstance(shape, Rectangle):
        p1, p2 = shape.getP1(), shape.getP2()
        x, y = (p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2
        half_w, half_h = abs(p2.getX() - p1.getX()) / 2, abs(p2.getY() - p1.getY()) / 2
        return x, y, half_w, half_h
    else:
        raise TypeError("Shape not supported yet!")  
def bounce_around(shape, width, height, dx, dy):
    bounced = 0

    shape.move(dx, dy)
    x, y, half_w, half_h = get_shape_center(shape)
    if x - half_w <= 0 or x + half_w >= width:
        dx = -dx
        bounced = 1
    if y - half_h <= 0 or y + half_h >= height:
        dy = -dy
        bounced = 1
    return dx, dy, bounced

def main():
    width, height, radius = 300, 300, 25
    win = win_background("Animation", width, height, "white")
    circle = draw_circ(win, 150, 150, radius)
    rect = draw_rec(win, 20, 20, 50, 50)
    sq_score_txt = draw_text(win, 42, 8, "Square Score:")
    circ_score_txt = draw_text(win, 255, 8, "Cicle Score:")
    circ_score, sq_score = 0, 0
    dx1, dy1, dx2, dy2 = 1, 1, 1, 1
    while True:
        dx1, dy1, bounced1 = bounce_around(circle, width, height, dx1, dy1)
        dx2, dy2, bounced2 = bounce_around(rect, width, height, dx2, dy2)
        if bounced1:
            circ_score += 1
        if bounced2:
            sq_score += 1
        circ_score_txt.setText(f"Circle Score: {circ_score}")
        sq_score_txt.setText(f"Square Score: {sq_score}")
        update(80)
        if win.checkMouse():
            break
    win.close()
main()