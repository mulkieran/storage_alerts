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

""" A module with a couple of recognizers in it. """

from ...generic.by_line.recognizer import Recognizer
from ...generic.by_line.states import RecognizerStates

class ProcessRecognizer(Recognizer):
    """ A recognizer that says yes after a message from a specified process. """

    description = "a process recognizer"

    def __init__(self, process):
        """ Initializer.

            :param str process: name of process
        """
        self._process = process
        self._evidence = []

    def _consume(self, entry):
        """ Consumes a journal entry.

            :param :class:`..entry.Entry` entry: a journal entry
        """
        self._evidence = []
        comm = entry.fields.get("_COMM")
        if comm == self._process:
            self._evidence = [entry]

    @property
    def state(self):
        if self._evidence:
            return RecognizerStates.YES
        else:
            return RecognizerStates.NO

    @property
    def evidence(self):
        return self._evidence

    @property
    def info(self):
        # pylint: disable=no-self-use
        return dict()
