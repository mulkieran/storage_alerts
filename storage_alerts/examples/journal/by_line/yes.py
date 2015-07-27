# Copyright (C) 2015  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>

""" A module that panics for every journal entry. """

from storage_alerts.sources.generic.by_line import Recognizer
from storage_alerts.sources.generic.by_line import RecognizerStates

class YesRecognizer(Recognizer):
    """ A recognizer that always says yes. """

    description = "any journal entry represents an error"

    def __init__(self):
        self._evidence = []

    def _consume(self, entry):
        self._evidence = [entry]

    @property
    def state(self):
        return RecognizerStates.YES if self._evidence else RecognizerStates.NO

    @property
    def evidence(self):
        return self._evidence

    @property
    def info(self):
        # pylint: disable=no-self-use
        return {
           'MESSAGE': "There is a message in the journal."
        }
