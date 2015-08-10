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

from .recognizer import Recognizer
from .states import RecognizerStates

class YesRecognizer(Recognizer):
    """ A recognizer that always says yes. """

    _HASH = ord('Y')

    description = "any journal entry represents an error"

    def __init__(self):
        self._evidence = []

    def initializeNew(self):
        return YesRecognizer()

    def __eq__(self, other):
        return type(other) == YesRecognizer

    def __ne__(self, other):
        return type(other) != YesRecognizer

    def __hash__(self):
        return self._HASH

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
        return dict()

class LazyRecognizer(Recognizer):
    """ A recognizer that doesn't say yes until it has to. """

    _HASH = ord('L')
    description = "any journal entry represents an unrefutable error"

    def __init__(self):
        self._evidence = []

    def initializeNew(self):
        return LazyRecognizer()

    def __eq__(self, other):
        return type(other) == LazyRecognizer

    def __ne__(self, other):
        return type(other) != LazyRecognizer

    def __hash__(self):
        return self._HASH

    def _consume(self, entry):
        if self.state is RecognizerStates.MAYBE_YES:
            return
        self._evidence = [entry]

    @property
    def state(self):
        return RecognizerStates.MAYBE_YES if self._evidence else RecognizerStates.NO

    @property
    def evidence(self):
        return self._evidence

    @property
    def info(self):
        # pylint: disable=no-self-use
        return dict()

class NoRecognizer(Recognizer):
    """ A recognizer that always says no. """

    _HASH = ord('N')
    description = "does not recognize any errors"

    def initializeNew(self):
        return NoRecognizer()

    def __eq__(self, other):
        return type(other) == NoRecognizer

    def __ne__(self, other):
        return type(other) != NoRecognizer

    def __hash__(self):
        return self._HASH

    def _consume(self, entry):
        pass

    @property
    def state(self):
        # pylint: disable=no-self-use
        return RecognizerStates.NO

    @property
    def evidence(self):
        # pylint: disable=no-self-use
        return []

    @property
    def info(self):
        # pylint: disable=no-self-use
        return dict()

class ManyRecognizer(Recognizer):
    """ A recognizer that says yes after a designated number of messages. """

    @property
    def description(self):
        return "a %s message recognizer" % self.NUMBER

    def __init__(self, number):
        """ Initializer.

            :param int number: number of messages that indicates a problem
        """
        self.NUMBER = number
        self._evidence = []

    def __eq__(self, other):
        return type(other) == ManyRecognizer and self.NUMBER == other.NUMBER

    def __ne__(self, other):
        return type(other) != ManyRecognizer or self.NUMBER != other.NUMBER

    def __hash__(self):
        return self.NUMBER

    def initializeNew(self):
        return ManyRecognizer(self.NUMBER)

    def _consume(self, entry):
        self._evidence.append(entry)

    @property
    def state(self):
        l = len(self._evidence)
        if l == self.NUMBER:
            return RecognizerStates.YES
        if l == 0:
            return RecognizerStates.NO
        return RecognizerStates.MAYBE_NO

    @property
    def evidence(self):
        return self._evidence

    @property
    def info(self):
        return {
           'COUNT': len(self._evidence),
           'REQUIRED' : self.NUMBER
        }
