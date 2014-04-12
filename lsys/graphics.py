import math
from lsys.core import LToken, LStringParser


class Cursor(object):
    def __init__(self,  canvas, steplen=2, angle=270):
        self._canvas = canvas
        self._pen_color = "black"
        self._steplen = steplen
        self._x = self._y = self._cang = 0
        self._init_angle = angle % 360
        self.reset()

    def reset(self):
        self._x = int(self._canvas.cget("width")) / 2
        self._y = int(self._canvas.cget("height")) / 2
        self._cang = self._init_angle

    def get_coords(self):
        return (self._x, self._y)

    def set_coords(self, coords):
        (self._x, self._y) = coords

    def get_steplen(self):
        return self._steplen

    def set_steplen(self, steplen):
        self._steplen = steplen

    def save_state(self):
        return (self._x, self._y, self._cang,
                self._pen_color)

    def restore_state(self, state):
        (self._x, self._y, self._cang,
         self._pen_color) = state

    def move(self, steps):
        (self._x, self._y) = self._inspect(steps)

    def draw(self, steps):
        (nx, ny) = self._inspect(steps)
        self._canvas.create_line(self._x, self._y, nx, ny)
        (self._x, self._y) = (nx, ny)

    def turn_left(self, angle):
        self._add_angle(-angle)

    def turn_right(self, angle):
        self._add_angle(angle)

    def _inspect(self, steps):
        length = steps * self._steplen
        angle_rads = math.radians(self._cang)
        return [i[1] + i[0] * length for i in 
            zip((math.cos(angle_rads), math.sin(angle_rads)),
                (self._x, self._y))]

    def _add_angle(self, angle):
        self._cang += angle
        self._cang %= 360


class LSystemVisualiser(object):
    def __init__(self, canvas, angle, lstring):
        self._cursor = Cursor(canvas)
        self._canvas = canvas
        self._parser = LStringParser(lstring)
        self._angle = angle
        self._stack = []
        self._table = {
            LToken.DRAW: lambda: self._cursor.draw(1),
            LToken.FORWARD: lambda: self._cursor.move(1),
            LToken.TLEFT: lambda: self._cursor.turn_left(self._angle),
            LToken.TRIGHT: lambda: self._cursor.turn_right(self._angle),
            LToken.PUSH: lambda: self._stack.append(self._cursor.save_state()),
            LToken.POP: lambda: self._cursor.restore_state(self._stack.pop())
        }

    def draw(self):
        # get the coordinates of the minimum rectangle 
        # that can be created around the the picture we're 
        # going to draw
        (xmin, xmax, ymin, ymax) = self._get_picture_rect()

        # now, when we know the size of this rectangle,
        # we can try to enlarge it (so as the picture)
        # and fit it to the available area in the best
        # way.
        xlen = xmax - xmin
        ylen = ymax - ymin
        width = int(self._canvas.cget("width"))
        height = int(self._canvas.cget("height"))
        diff = min(width - xlen, height - ylen) / 2

        # adjust the step length
        old_slen = self._cursor.get_steplen()
        new_slen = old_slen + (old_slen * diff) / xlen
        self._cursor.set_steplen(new_slen)

        # adjust the coordinates so that picture will be
        # centered when drawn
        (x, y) = self._cursor.get_coords()
        nxmin = (width / 2) - (xlen / old_slen * new_slen) / 2
        nymin = (height / 2) - (ylen / old_slen * new_slen) / 2
        self._cursor.set_coords(((x - xmin) / old_slen * new_slen + nxmin,
                                (y - ymin) / old_slen * new_slen + nymin))


        # and draw it, finally
        token = self._parser.first_token()
        while token:
            self._process_token(token)
            token = self._parser.next_token()

    def _get_picture_rect(self):
        (x, y) = self._cursor.get_coords()
        (xmin, xmax) = (x - 1, x + 1)
        (ymin, ymax) = (y - 1, y + 1)

        token = self._parser.first_token()
        while token:
            self._process_token(token, dryrun=True)
            (x, y) = self._cursor.get_coords()
            xmin = min(x, xmin)
            xmax = max(x, xmax)
            ymin = min(y, ymin)
            ymax = max(y, ymax)
            token = self._parser.next_token()

        self._cursor.reset()
        return (xmin, xmax, ymin, ymax)

    def _process_token(self, token, dryrun=False):
        if dryrun and token == LToken.DRAW:
            token = LToken.FORWARD

        self._table[token]()
