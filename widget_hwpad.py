#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: widget_hwpad.py
# Author: Paul Goins
# Created on: 25 Nov 2008

import gtk
import cairo

class Point:
    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y

class WidgetHWPad(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)

        self.set_events(
            gtk.gdk.EXPOSURE_MASK  |
            gtk.gdk.BUTTON1_MOTION_MASK |
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK |
            gtk.gdk.POINTER_MOTION_HINT_MASK
            )
        self.connect("expose-event", self.on_expose)
        self.connect("motion-notify-event", self.on_motion)
        self.connect("button-press-event", self.on_press)
        self.connect("button-release-event", self.on_release)

        self.current_line = None
        self.lines = []
        self.results = []

    def on_expose(self, widget, event):
        cairo_context = self.window.cairo_create()

        # Clip update region
        cairo_context.rectangle(
            event.area.x, event.area.y, event.area.width, event.area.height)
        cairo_context.clip()

        # Set drawing style
        cairo_context.set_line_width(5)
        cairo_context.set_line_join(cairo.LINE_JOIN_ROUND)
        cairo_context.set_line_cap(cairo.LINE_CAP_ROUND)

        # Fill background to white
        cairo_context.set_source_rgb(1, 1, 1)
        cairo_context.paint()

        # Create path from stored data
        # Also, if a line is being drawn, append the partial line temporarily.
        if self.current_line: self.lines.append(self.current_line)
        for line in self.lines:
            if len(line) < 2: continue
            line_started = False

            for point in line:
                if not line_started:
                    cairo_context.move_to(point.x, point.y)
                    line_started = True
                else:
                    cairo_context.line_to(point.x, point.y)
        if self.current_line: self.lines.pop()

        # Draw lines
        cairo_context.set_source_rgb(0, 0, 0)
        cairo_context.stroke()
        return True

    def on_motion(self, widget, event):
        if event.state | gtk.gdk.BUTTON1_MASK:
            if self.current_line:
                self.current_line.append(Point(event.x, event.y))
            self.update_drawing_area()

        # This was marked as non-Win32 in the C++ version.  Unsure whether
        # it's okay as it is here.
        gtk.gdk.event_request_motions(event)

        return True

    def on_press(self, widget, event):
        # On left mouse click, create a new line
        if event.button == 1:
            self.current_line = []
            self.current_line.append(Point(event.x, event.y))

        return True

    def on_release(self, widget, event):
        """Returns False when the control's state has been changed by a button release, True otherwise."""

        if event.button == 1:
            if self.current_line:
                self.lines.append(self.current_line)
                self.current_line = None
                self.update_drawing_area()
                self.look_up_chars()
                return False
            # If no line was written, return true (no change in state)
            return True

        elif event.button == 3:
            if self.current_line:
                self.current_line = None
                self.update_drawing_area()
                # No change in search results has occurred, so return true
                return True
            elif (self.lines):
                self.lines.pop()
                self.update_drawing_area()
                self.look_up_chars()
                # The search -has- changed, return False so we can capture it.
                return False
            else:
                return True

        return True

    def get_results(self):
        """Returns an array of 5 UTF8-encoded kanji characters."""

        print "WidgetHWPad.get_results() \n\t= %s" % (self.results,)

        return self.results

    def update_drawing_area(self):
        self.window.invalidate_rect(None, False)

    def look_up_chars(self):
        print "WidgetHWPad.look_up_chars()"

        # Currently this does nothing.  This -will- call the jben_kpengine(.exe)
        # external program and capture its results.
