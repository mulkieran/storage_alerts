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

from six import with_metaclass

from .states import RecognizerStates

class Recognizer(with_metaclass(abc.ABCMeta, object)):
    """ Abstract parent class of Recognizer classes.

        A recognizer may need to read multiple journal
        entries before deciding whether it has found a match.

        Once a recognizer has arrived at the YES conclusion it
        no longer actually consumes entries or changes. It
        should be taken out of service.

        The info property consists solely of information that
        can be synthesized from the journal entries.
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
        raise NotImplementedError("Abstract Method") #pragma: no cover

    def consume(self, entry):
        """ Consume a journal entry.

            :param :class:`.Entry` entry: a journal entry
            :rtype: :class:`.scanner.RecognizerState`
            :returns: a state indicating status of scanner
        """
        if self.state is RecognizerStates.YES:
            return self.state
        self._consume(entry)
        return self.state

    state = abc.abstractproperty(doc="the state of this scanner")
    """ :rtype: :class:`.scanner.RecognizerState` """

    evidence = abc.abstractproperty(doc="the evidence for the decision")
    """ :rtype: list of :class:`.Entry` """

    info = abc.abstractproperty(doc="information for consumers")
    """ :rtype: dict of key/value pairs """

    @abc.abstractmethod
    def __eq__(self, other):
        raise NotImplementedError() #pragma: no cover

    @abc.abstractmethod
    def __ne__(self, other):
        raise NotImplementedError() #pragma: no cover

    @abc.abstractmethod
    def initializeNew(self):
        """ Make an initial object from this object.

            The new object should have the same type and
            have values that a newly constructed object of this
            type should have.

            Should have the same result as deepcopy would have if the
            copy were made immediately after the object were instantiated.
        """
        raise NotImplementedError() #pragma: no cover
