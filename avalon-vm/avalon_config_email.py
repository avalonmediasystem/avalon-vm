#
# Brian Wheeler <bdwheele@indiana.edu>
#
# Based on the work of:
#   Chris Lumens <clumens@redhat.com>
#   Copyright 2007 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 
#
import gtk
import vte
import time
import subprocess
import string


from firstboot.config import *
from firstboot.constants import *
from firstboot.functions import *
from firstboot.module import *

import gettext
_ = lambda x: gettext.ldgettext("firstboot", x)
N_ = lambda x: x

class moduleClass(Module):
    def __init__(self):
        Module.__init__(self)
        self.priority = 205
        self.sidebarTitle = N_("Avalon Email")
        self.title = N_("Avalon Email")
        self.icon = "workstation.png"
        self.built = False
        self.running = False
        self.buildCommand = "/usr/share/avalon-vm/avalon_config_email"

    def apply(self, interface, testing=False):
        os.system(self.buildCommand + 
                  " " + self.commentsEntry.get_text() +
                  " " + self.notificationsEntry.get_text() +
                  " " + self.supportEntry.get_text() +
                  " " + self.mailerEntry.get_text() +
                  " " + self.mailportEntry.get_text())
        return RESULT_SUCCESS

    def createScreen(self):
        self.vbox = gtk.VBox(spacing=10)

        label = gtk.Label("Avalon will send email in response to different "
                          "events or at the request of the users.  Enter the "
                          "email addresses for the different types of "
                          "messages below.")
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        self.vbox.pack_start(label, False, True)

        emaildomain = 'example.com'

        table = gtk.Table(2, 3)
        table.set_row_spacings(6)
        table.set_col_spacings(6)

        self.commentsEntry = gtk.Entry()
        self.commentsEntry.set_width_chars(32)
        self.commentsEntry.set_text('comments@' + emaildomain)
        label = gtk.Label("User Comments:")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0, 1, 0, 1, gtk.FILL)
        table.attach(self.commentsEntry, 1, 2, 0, 1, gtk.SHRINK, gtk.FILL, 5)

        self.notificationsEntry = gtk.Entry()
        self.notificationsEntry.set_width_chars(32)
        self.notificationsEntry.set_text('notifications@' + emaildomain)
        label = gtk.Label("Avalon Notifications:")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0, 1, 1, 2, gtk.FILL)
        table.attach(self.notificationsEntry, 1, 2, 1, 2, gtk.SHRINK, gtk.FILL, 5)

        self.supportEntry = gtk.Entry()
        self.supportEntry.set_width_chars(32)
        self.supportEntry.set_text('support@' + emaildomain)
        label = gtk.Label("Support Requests:")
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0, 1, 2, 3, gtk.FILL)
        table.attach(self.supportEntry, 1, 2, 2, 3, gtk.SHRINK, gtk.FILL, 5)
        self.vbox.pack_start(table, False)

        label = gtk.Label("\n\nAvalon needs an SMTP relay host to use for "
                          "sending email.  Enter it below")
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        self.vbox.pack_start(label, False, True)


        table = gtk.Table(2, 3)
        table.set_row_spacings(6)
        table.set_col_spacings(6)

        label = gtk.Label("Hostname:")
        label.set_alignment(1.0, 0.5)
        self.mailerEntry = gtk.Entry()
        self.mailerEntry.set_width_chars(32)
        self.mailerEntry.set_text('smtp.' + emaildomain)
        table.attach(label, 0, 1, 0, 1, gtk.FILL)
        table.attach(self.mailerEntry, 1, 2, 0, 1, gtk.SHRINK, gtk.FILL, 5)

        label = gtk.Label("Port:")
        label.set_alignment(1.0, 0.5)
        self.mailportEntry = gtk.Entry()
        self.mailportEntry.set_width_chars(4)
        self.mailportEntry.set_text('587')
        table.attach(label, 0, 1, 1, 2, gtk.FILL)
        table.attach(self.mailportEntry, 1, 2, 1, 2, gtk.SHRINK, gtk.FILL, 5)
        self.vbox.pack_start(table, False)

        
    def initializeUI(self):
        pass
