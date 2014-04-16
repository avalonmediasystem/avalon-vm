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
        self.priority = 210
        self.sidebarTitle = N_("Avalon Config")
        self.title = N_("Avalon Configuration")
        self.icon = "workstation.png"
        self.built = False
        self.running = False
        self.avalon_host_config = "/etc/init.d/avalon_host_config"
        self.avalon_randomize_passwords = "/usr/share/avalon-vm/avalon_randomize_passwords"

    def _showErrorMessage(self, text):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
        dlg.set_position(gtk.WIN_POS_CENTER)
        dlg.set_modal(True)
        rc = dlg.run()
        dlg.destroy()
        return None



    def apply(self, interface, testing=False):
        if(self.passwordEntry.get_text() != self.verifyEntry.get_text()):
            self._showErrorMessage(_("The passwords do not match. Please enter the password again."))
            self.passwordEntry.set_text("")
            self.verifyEntry.set_text("")
            self.focus()
            return RESULT_FAILURE

        if(self.passwordEntry.get_text() == ""):
            self._showErrorMessage(_("The passwords cannot be blank. Please enter the password again."))
            self.passwordEntry.set_text("")
            self.verifyEntry.set_text("")
            self.focus()
            return RESULT_FAILURE

        if(self.usernameEntry.get_text() == ""):
            self._showErrorMessage(_("The username cannot be blank. Please enter the username again."))
            self.focus()
            return RESULT_FAILURE

        if not ("@" in self.usernameEntry.get_text()):
            self._showErrorMessage(_("The username must contain an '@'. Please enter the username again."))
            self.focus()
            return RESULT_FAILURE



        if(self.defaultHostname != self.hostnameEntry.get_text()):
            if(self.hostnameEntry.get_text() != ''):
                os.system(self.avalon_host_config + " sethostname " + self.hostnameEntry.get_text())
        os.system(self.avalon_host_config + " start")
        os.system(self.avalon_randomize_passwords)

        os.system("runuser -l root -c \"" +
                  "cd /var/www/avalon/current; " +
                  "RAILS_ENV=production " +
                  "bundle exec rake avalon:user:create avalon_username=" +
                  self.usernameEntry.get_text() + " " +
                  "avalon_password='" + self.passwordEntry.get_text() + "' " +
                  "avalon_groups=administrator\"")

        os.system("runuser -l root -c \"" +
                  "cd /var/www/avalon/current; " +
                  "RAILS_ENV=production " +
                  "bundle exec rake avalon:user:delete " +
                  "avalon_username=archivist1@example.com\"")

        return RESULT_SUCCESS

    def createScreen(self):
        self.vbox = gtk.VBox(spacing=10)

        label = gtk.Label("Avalon is nearly ready to use!\n\n"                  
                          "The Access hostname is the name that clients will "
                          "use to connect to Avalon.  The default is to use "
                          "the DNS address for the machine.  The value below "
                          "is the name for the current address.  If a "
                          "different name should be used, enter it below")
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(600, -1)
        self.vbox.pack_start(label, False, True)

        self.defaultHostname = subprocess.Popen([self.avalon_host_config, 'hostname'],stdout=subprocess.PIPE).communicate()[0].rstrip()
        domain = 'localdomain'
        emaildomain = 'example.com'
        if(string.find(self.defaultHostname, '.') != -1):
            domainarr = string.split(self.defaultHostname, '.')
            domainarr.pop(0)
            domain = string.join(domainarr, '.')
            while len(domainarr) > 2:
                domainarr.pop(0)
            emaildomain = string.join(domainarr, '.')

        table = gtk.Table(2, 1)
        table.set_row_spacings(6)
        table.set_col_spacings(6)

        label = gtk.Label("Access Hostname")
        label.set_alignment(1.0, 0.5)
        self.hostnameEntry = gtk.Entry()
        self.hostnameEntry.set_width_chars(32)
        self.hostnameEntry.set_text(self.defaultHostname)
        table.attach(label, 0, 1, 0, 1, gtk.FILL)        
        table.attach(self.hostnameEntry, 1, 2, 0, 1, gtk.SHRINK, gtk.FILL, 5)
        self.vbox.pack_start(table, False)

        label = gtk.Label("\n\nCreate a user which will be able to manage "
                          "other users and the collections within Avalon.  "
                          "The username should look like "
                          "an email address and the password should not be "
                          "easily guessed.")
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(600, -1)
        self.vbox.pack_start(label, False)
        table = gtk.Table(2, 3)
        table.set_row_spacings(6)
        table.set_col_spacings(6)

        label = gtk.Label("Username")
        label.set_alignment(1.0, 0.5)
        self.usernameEntry = gtk.Entry()
        self.usernameEntry.set_width_chars(32)
        self.usernameEntry.set_text('youremail@example.com')
        table.attach(label, 0, 1, 0, 1, gtk.FILL)
        table.attach(self.usernameEntry, 1, 2, 0, 1, gtk.SHRINK,gtk.FILL, 5)
        label = gtk.Label("Password")
        label.set_alignment(1.0, 0.5)
        self.passwordEntry = gtk.Entry()
        self.passwordEntry.set_width_chars(32)
        self.passwordEntry.set_visibility(False)
        table.attach(label, 0, 1, 1, 2, gtk.FILL)
        table.attach(self.passwordEntry, 1, 2, 1, 2, gtk.SHRINK,gtk.FILL, 5)        
        label = gtk.Label("Verify")
        label.set_alignment(1.0, 0.5)
        self.verifyEntry = gtk.Entry()
        self.verifyEntry.set_width_chars(32)
        self.verifyEntry.set_visibility(False)
        table.attach(label, 0, 1, 2, 3, gtk.FILL)
        table.attach(self.verifyEntry, 1, 2, 2, 3, gtk.SHRINK,gtk.FILL, 5)

        self.vbox.pack_start(table, False)

    def initializeUI(self):
        pass
