

from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, BoundedNumericProperty,
                             ListProperty,
                             ReferenceListProperty)
from kivy.clock import Clock
from kivy.graphics import Color
from math import pi

class ColorWheel(Widget):
    '''Chromatic wheel for the ColorPicker.

    .. versionchanged:: 1.7.1
        `font_size`, `font_name` and `foreground_color` have been removed. The
        sizing is now the same as others widget, based on 'sp'. Orientation is
        also automatically determined according to the width/height ratio.

    '''

    r = BoundedNumericProperty(0, min=0, max=1)
    '''The Red value of the color currently selected.

    :attr:`r` is a :class:`~kivy.properties.BoundedNumericProperty` and
    can be a value from 0 to 1. It defaults to 0.
    '''

    g = BoundedNumericProperty(0, min=0, max=1)
    '''The Green value of the color currently selected.

    :attr:`g` is a :class:`~kivy.properties.BoundedNumericProperty`
    and can be a value from 0 to 1.
    '''

    b = BoundedNumericProperty(0, min=0, max=1)
    '''The Blue value of the color currently selected.

    :attr:`b` is a :class:`~kivy.properties.BoundedNumericProperty` and
    can be a value from 0 to 1.
    '''

    a = BoundedNumericProperty(0, min=0, max=1)
    '''The Alpha value of the color currently selected.

    :attr:`a` is a :class:`~kivy.properties.BoundedNumericProperty` and
    can be a value from 0 to 1.
    '''

    color = ReferenceListProperty(r, g, b, a)
    '''The holds the color currently selected.

    :attr:`color` is a :class:`~kivy.properties.ReferenceListProperty` and
    contains a list of `r`, `g`, `b`, `a` values.
    '''

    _origin = ListProperty((100, 100))
    _radius = NumericProperty(100)

    _piece_divisions = NumericProperty(10)
    _pieces_of_pie = NumericProperty(16)

    _inertia_slowdown = 1.25
    _inertia_cutoff = .25

    _num_touches = 0
    _pinch_flag = False

    _hsv = ListProperty([1, 1, 1, 0])

    def __init__(self, **kwargs):
        super(ColorWheel, self).__init__(**kwargs)

        pdv = self._piece_divisions
        self.sv_s = [(float(x) / pdv, 1) for x in range(pdv)] + [
            (1, float(y) / pdv) for y in reversed(range(pdv))]

    def on__origin(self, instance, value):
        self.init_wheel(None)

    def on__radius(self, instance, value):
        self.init_wheel(None)

    def init_wheel(self, dt):
        # initialize list to hold all meshes
        self.canvas.clear()
        self.arcs = []
        self.sv_idx = 0
        pdv = self._piece_divisions
        ppie = self._pieces_of_pie

        for r in range(pdv):
            for t in range(ppie):
                self.arcs.append(
                    _ColorArc(
                        self._radius * (float(r) / float(pdv)),
                        self._radius * (float(r + 1) / float(pdv)),
                        2 * pi * (float(t) / float(ppie)),
                        2 * pi * (float(t + 1) / float(ppie)),
                        origin=self._origin,
                        color=(float(t) / ppie,
                               self.sv_s[self.sv_idx + r][0],
                               self.sv_s[self.sv_idx + r][1],
                               1)))

                self.canvas.add(self.arcs[-1])

    def recolor_wheel(self):
        ppie = self._pieces_of_pie
        for idx, segment in enumerate(self.arcs):
            segment.change_color(
                sv=self.sv_s[int(self.sv_idx + idx / ppie)])

    def change_alpha(self, val):
        for idx, segment in enumerate(self.arcs):
            segment.change_color(a=val)

    def inertial_incr_sv_idx(self, dt):
        # if its already zoomed all the way out, cancel the inertial zoom
        if self.sv_idx == len(self.sv_s) - self._piece_divisions:
            return False

        self.sv_idx += 1
        self.recolor_wheel()
        if dt * self._inertia_slowdown > self._inertia_cutoff:
            return False
        else:
            Clock.schedule_once(self.inertial_incr_sv_idx,
                                dt * self._inertia_slowdown)

    def inertial_decr_sv_idx(self, dt):
        # if its already zoomed all the way in, cancel the inertial zoom
        if self.sv_idx == 0:
            return False
        self.sv_idx -= 1
        self.recolor_wheel()
        if dt * self._inertia_slowdown > self._inertia_cutoff:
            return False
        else:
            Clock.schedule_once(self.inertial_decr_sv_idx,
                                dt * self._inertia_slowdown)

    def on_touch_down(self, touch):
        r = self._get_touch_r(touch.pos)
        if r > self._radius:
            return False

        # code is still set up to allow pinch to zoom, but this is
        # disabled for now since it was fiddly with small wheels.
        # Comment out these lines and  adjust on_touch_move to reenable
        # this.
        if self._num_touches != 0:
            return False

        touch.grab(self)
        self._num_touches += 1
        touch.ud['anchor_r'] = r
        touch.ud['orig_sv_idx'] = self.sv_idx
        touch.ud['orig_time'] = Clock.get_time()

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        r = self._get_touch_r(touch.pos)
        goal_sv_idx = (touch.ud['orig_sv_idx'] -
                       int((r - touch.ud['anchor_r']) /
                            (float(self._radius) / self._piece_divisions)))

        if (
            goal_sv_idx != self.sv_idx and
            goal_sv_idx >= 0 and
            goal_sv_idx <= len(self.sv_s) - self._piece_divisions
        ):
            # this is a pinch to zoom
            self._pinch_flag = True
            self.sv_idx = goal_sv_idx
            self.recolor_wheel()

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        self._num_touches -= 1
        if self._pinch_flag:
            if self._num_touches == 0:
                # user was pinching, and now both fingers are up. Return
                # to normal
                if self.sv_idx > touch.ud['orig_sv_idx']:
                    Clock.schedule_once(
                        self.inertial_incr_sv_idx,
                        (Clock.get_time() - touch.ud['orig_time']) /
                        (self.sv_idx - touch.ud['orig_sv_idx']))

                if self.sv_idx < touch.ud['orig_sv_idx']:
                    Clock.schedule_once(
                        self.inertial_decr_sv_idx,
                        (Clock.get_time() - touch.ud['orig_time']) /
                        (self.sv_idx - touch.ud['orig_sv_idx']))

                self._pinch_flag = False
                return
            else:
                # user was pinching, and at least one finger remains. We
                # don't want to treat the remaining fingers as touches
                return
        else:
            r, theta = rect_to_polar(self._origin, *touch.pos)
            # if touch up is outside the wheel, ignore
            if r >= self._radius:
                return
            # compute which ColorArc is being touched (they aren't
            # widgets so we don't get collide_point) and set
            # _hsv based on the selected ColorArc
            piece = int((theta / (2 * pi)) * self._pieces_of_pie)
            division = int((r / self._radius) * self._piece_divisions)
            self._hsv = \
                self.arcs[self._pieces_of_pie * division + piece].color

    def on__hsv(self, instance, value):
        c_hsv = Color(*value, mode='hsv')
        self.r = c_hsv.r
        self.g = c_hsv.g
        self.b = c_hsv.b
        self.a = c_hsv.a
        self.rgba = (self.r, self.g, self.b, self.a)

    def _get_touch_r(self, pos):
        return distance(pos, self._origin)

