#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk
from jben import global_refs


class StoredSizeBase(object):

    """Mixin class for stored sizes.

    Note that this class sets several handlers:

    * delete-event
    * configure-event
    * window-state-event

    Do not connect these handlers in subclasses, or you'll end up with two
    calls which is probably not what you want!  Rather, please just override
    these functions and call them from within your customized versions.

    Alternatively, if you *insist* on adding additional connectors, then
    use function names which won't collide with the ones here.

    """

    def __init__(self, param, width=-1, height=-1):
        self.param_name = param
        prefs = global_refs.prefs
        pref = None
        if param:
            pref = prefs.get(param)
        if pref:
            width, height = [int(v) for v in pref.split("x", 1)]
        self.set_default_size(width, height)
        self.connect("delete-event", self.delete_event)
        self.connect("window-state-event", self.window_state_event)
        self.connect("configure-event", self.configure_event)
        self.stored_size = (width, height)
        self.prior_size = self.stored_size
        self.maximized = False

    def delete_event(self, widget, event, data=None):
        prefs = global_refs.prefs
        prefs[self.param_name] = "%dx%d" % self.stored_size
        return False

    # Not sure how best to handle size tracking *ONLY* when *NOT* maximized...
    # Sadly, the window state changes AFTER the resize.
    # Best thing I can think of is hack it: store the two most recent size
    # values, update them on any new size events, and force a fallback on
    # maximizing.
    # Although, this does have a corner case if the window is the same size
    # before the maximize...

    def configure_event(self, widget, event, data=None):
        if not self.maximized:
            new_size = (event.width, event.height)
            if new_size != self.stored_size:
                self.prior_size = self.stored_size
                self.stored_size = new_size
            return False

    def window_state_event(self, widget, event, data=None):
        old_state = self.maximized
        self.maximized = \
            (event.new_window_state & gtk.gdk.WINDOW_STATE_MAXIMIZED) != 0
        # Ugly hack for non-maximized size tracking
        if self.maximized and not old_state:
            self.stored_size = self.prior_size
        return False


class StoredSizeWindow(gtk.Window, StoredSizeBase):

    """Modified gtk.Window with size stored in the preferences object.

    Although defaults are defined, this class really expects the first 3
    values to be explicitly set, and then any remaining args will be properly
    passed to the gtk.Window.__init__ function.

    """

    def __init__(self, param, width=-1, height=-1, *args, **kwargs):
        gtk.Window.__init__(self, *args, **kwargs)
        StoredSizeBase.__init__(self, param, width, height)


class StoredSizeDialog(gtk.Dialog, StoredSizeBase):

    """Modified gtk.Dialog with size stored in the preferences object.

    Although defaults are defined, this class really expects the first 3
    values to be explicitly set, and then any remaining args will be properly
    passed to the gtk.Dialog.__init__ function.

    """

    def __init__(self, param, width=-1, height=-1, *args, **kwargs):
        gtk.Dialog.__init__(self, *args, **kwargs)
        StoredSizeBase.__init__(self, param, width, height)
