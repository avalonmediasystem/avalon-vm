#
# Brian Wheeler <bdwheele@indiana.edu>
#
# Based (rather heavily) on eula.py by
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
import os
import glob
import re

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
        self.priority = 3
        self.sidebarTitle = N_("License Information")
        self.title = N_("License Information")
        self.icon = "workstation.png"
        self.eula_path = "/usr/share/avalon-vm/EULA"

        
    def apply(self, interface, testing=False):
        if self.okButton.get_active() == True:
            return RESULT_SUCCESS
        else:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_NONE,
                                    (_("Do you want to reread or reconsider the Licence Agreement?  " 
                                       "If not, please shut down the computer and remove this "
                                       "product from your system. ")))

            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(True)

            continueButton = dlg.add_button(_("_Reread license"), 0)
            shutdownButton = dlg.add_button(_("_Shut down"), 1)
            continueButton.grab_focus()

            rc = dlg.run()
            dlg.destroy()

            if rc == 0:
                return RESULT_FAILURE
            elif rc == 1:
                os.system("/sbin/halt")
                return RESULT_FAILURE

    def createScreen(self):
        self.vbox = gtk.VBox(spacing=10)

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)
        internalVBox.set_spacing(5)

        textBuffer = gtk.TextBuffer()
        textView = gtk.TextView()
        textView.set_editable(False)
        textView.set_wrap_mode(gtk.WRAP_WORD)
        textSW = gtk.ScrolledWindow()
        textSW.set_shadow_type(gtk.SHADOW_IN)
        textSW.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textSW.add(textView)

        locale_id = re.split("[._@]", os.environ["LANG"], 1)[0]
        use_translated_eula = True
        license_file = None
        while True:
            try:
                lookup_path = self.eula_path
                if use_translated_eula:
                    lookup_path += "_%s" % locale_id
                license_file = glob.glob(lookup_path)[0]
            except IndexError:
                if use_translated_eula:
                    use_translated_eula = False
                    continue
                lines = "No license file found in %s\n" % lookup_path
                break
            else:
                lines = open(license_file).readlines()
                break
                
        iter = textBuffer.get_iter_at_offset(0)

        for line in lines:
            textBuffer.insert(iter, line)
        textView.set_buffer(textBuffer)

        self.okButton = gtk.RadioButton(None, (_("_Yes, I agree to the License Agreement")))
        self.noButton = gtk.RadioButton(self.okButton, (_("N_o, I do not agree")))
        self.okButton.set_active(True)

        internalVBox.pack_start(textSW, True)
        internalVBox.pack_start(self.okButton, False)
        internalVBox.pack_start(self.noButton, False)

        self.vbox.pack_start(internalVBox, True, 5)

    def initializeUI(self):
        pass
