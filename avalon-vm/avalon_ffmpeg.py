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
import sys

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
        self.priority = 200
        self.sidebarTitle = N_("Build FFMPEG")
        self.title = N_("Build FFMPEG")
        self.icon = "workstation.png"
        self.built = False
        self.running = False
        self.buildCommand = ['/usr/bin/script', '-f', '-c',
                             '/usr/share/avalon-vm/buildFFMPEG',
                             '/root/ffmpeg-build.log']

    def apply(self, interface, testing=False):
        return RESULT_SUCCESS

    def createScreen(self):
        self.vbox = gtk.VBox(spacing=10)

        label = gtk.Label(_("FFMPEG is an open source tool used for "
                            "converting audio and visual files into other "
                            "formats.  "
                            "The configuration of FFMPEG used by Avalon "
                            "requires a build of FFMPEG which cannot be "
                            "redistributed in binary form.  In order to "
                            "be compliant with the licenses, the end-user "
                            "(you) must build FFMPEG.\n\nBy pressing the "
                            "'Build FFMPEG' button "
                            "below you will start the FFMPEG build process "
                            "and you acknowledge that the FFMPEG binary "
                            "created cannot be redistributed.\n\n"
                            "The build log is stored in /root/ffmpeg-build.log"
                            ))
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(600, -1)
        self.vbox.pack_start(label, False, True)

        self.term = vte.Terminal()        
        self.vbox.pack_start(self.term, False, True)

        button = gtk.Button("Build FFMPEG")
        button.connect("clicked", self.buildFFMPEG)
        self.vbox.pack_start(button, False, True)

    def buildFFMPEG(self, clicker):
        message = ""
        if not self.built:
            childPid = self.term.fork_command(self.buildCommand[0], 
                                              self.buildCommand)
            if childPid > 0:
                self.running = True
                while self.running:
                    time.sleep(0.1)
                    try:
                        pid, rc = os.waitpid(childPid, os.WNOHANG)
                        if childPid == pid:
                            self.running = False
                    except:
                        self.running = False
                    while gtk.events_pending():
                        gtk.main_iteration_do()
                self.built = True
                if rc != 0:
                    message = "Build/Install exited with return code " + str(rc)
            else:
                message = "Couldn't run the command '" + self.buildCommand + "'"
        if message != "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, 
                                    gtk.BUTTONS_NONE, "FFMPEG has not been "
                                    "built because of an error: " + message +
                                    "\n\nAvalon install will continue but  "
                                    "some functionality will not be "
                                    "available.\n\n"
                                    "Please inform the developers!")
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(True)
            dlg.add_button("OK", 1)
            dlg.run()
            dlg.destroy()
            self.built = True



    def apply(self, interface, testing=False):
        if not self.built:
            message = "FFMPEG has not been built so Avalon install cannot continue."
            if self.running:
                message = "FFMPEG is still building."

            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, 
                                    gtk.BUTTONS_NONE, "FFMPEG has not been "
                                    "built so Avalon install cannot continue.")
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(True)
            dlg.add_button("OK", 1)
            rc = dlg.run()
            dlg.destroy()
            if rc == 1:
                return RESULT_FAILURE            
        return RESULT_SUCCESS

    def initializeUI(self):
        pass
