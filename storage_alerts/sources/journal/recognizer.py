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

""" For generating objects that interpret a sequence of journal entries. """

import abc

from six import add_metaclass

class RecognizerState(object):
    """ Class for defining enumeration of states of a scanner. """

    def __init__(self, desc):
        """ Initializer.

            :param str desc: meaning of scanner state
        """
        self._desc = desc

    def __str__(self):
        return self._desc
    __repr__ = __str__

class RecognizerStates(object):
    """ Organizes all allowed states of a scanner object. """

    MAYBE = RecognizerState("May be in the process of recognizing the error.")
    YES = RecognizerState("The error has been recognized.")
    NO = RecognizerState("The entry just read does not indicate the error.")

@add_metaclass(abc.ABCMeta)
class Recognizer(object):
    """ Abstract parent class of Recognizer classes.

        A recognizer may need to read multiple journal
        entries before deciding whether it has found a match.

        Once a recognizer has arrived at the YES conclusion it
        no longer actually consumes entries or changes. It
        should be taken out of service.
    """

    description = abc.abstractproperty(doc="brief description")

    def __str__(self):
        return self.description

    @abc.abstractmethod
    def _consume(self, entry):
        """ Consume a journal entry.

            :param :class:`.Entry` entry: a journal entry

            Updates internal structures that indicate match or not.
        """
        raise NotImplementedError("Abstract Method")

    def consume(self, entry):
        """ Consume a journal entry.

            :param :class:`.Entry` entry: a journal entry
            :rtype: :class:`.scanner.RecognizerState`
            :returns: a state indicating status of scanner
        """
        if self.state == RecognizerStates.YES:
            return self.state
        self._consume(entry)
        return self.state

    state = abc.abstractproperty(doc="the state of this scanner")
    """ :rtype: :class:`.scanner.RecognizerState` """

    evidence = abc.abstractproperty(doc="the evidence for the decision")
    """ :rtype: list of :class:`.Entry` """

    info = abc.abstractproperty(doc="information for consumers")
    """ :rtype: dict of key/value pairs """
