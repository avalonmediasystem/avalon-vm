# NOTICE: this requires SELINUX to be permissive or disabled
#
# Brian Wheeler <bdwheele@indiana.edu> 
#
# Based on create_user.py by
#    Chris Lumens <clumens@redhat.com>
#    Copyright 2008 Red Hat, Inc.
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
import os, string, sys, time
import os.path
import pwd

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
        self.priority = 50
        self.sidebarTitle = N_("Update Networking")
        self.title = N_("Update Networking")
        self.icon = "workstation.png"



    def apply(self, interface, testing=False):
        os.system("hostname localhost")
        os.system("/sbin/service network restart")
        return RESULT_SUCCESS

    def createScreen(self):
        self.vbox = gtk.VBox(spacing=10)

        label = gtk.Label(_("The default network configuration for the Avalon "
                            "VM uses DHCP.  "
                            "If you wish to change the network "
                            "settings, use the Network Settings button below."))

        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        self.vbox.pack_start(label, False, True)

        authHBox = gtk.HBox()
        authButton = gtk.Button(_("Network Settings"))
        authButton.connect("clicked", self._runNetworkSettings)
        align = gtk.Alignment()
        align.add(authButton)
        align.set(0.0, 0.5, 0.0, 1.0)
        authHBox.pack_start(align, True)
        self.vbox.pack_start(authHBox, False, False)



    def initializeUI(self):
        pass

    def _runNetworkSettings(self, *args):
        # Create a gtkInvisible to block until network config is done.
        i = gtk.Invisible()
        i.grab_add()

        pid = start_process("/usr/bin/nm-connection-editor")
        while True:
            while gtk.events_pending():
                gtk.main_iteration_do()

            child_pid, status = os.waitpid(pid, os.WNOHANG)
            if child_pid == pid:
                break
            else:
                time.sleep(0.1)

        i.grab_remove()



