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

""" For managing  objects. """

import logging

from .states import RecognizerStates

class RecognizerManager(object):
    """ Maintains a set of Recognizer classes. """

    #    Invariants:
    #     * all scanner objects in self._scanners are in MAYBE states
    #     * there are no duplicates in self._recognizers

    def __init__(self, recognizers, ejector, scanners):
        """ Initializer.

            :param recognizers: list of recognizer objects
            :type recognizers: list of :class:`Recognizer`
            :param :class:`EjectionPolicy` ejector: an ejection policy
            :param scanners: a list of recognizers
            :type scanners: list of :class:`Recognizer`
        """
        self._recognizers = set(recognizers)
        self._ejector = ejector
        self._scanners = scanners

    def _scannersStr(self, scanners):
        """ Returns a str representation of a list of scanners.

            :param list scanners: a list of Recognizers
            :rtype: str
        """
        # pylint: disable=no-self-use
        return ", ".join(str(s) for s in scanners)

    def processEntry(self, entry):
        """ Process a journal entry.

            :param :class:`.Entry` entry: a journal entry
            :returns: a list of matching objects, may be empty
            :rtype: list of :class:`.scanner.Recognizer`

            Use all current scanners, which all have state MAYBE_*, and also
            instantiates new objects for every registered scanner class.
        """
        scanners = self._scanners + [r.initializeNew() for r in self._recognizers]
        for scanner in scanners:
            scanner.consume(entry)
        yeses = [s for s in scanners if s.state is RecognizerStates.YES]
        self._scanners = [s for s in scanners if s.state in (RecognizerStates.MAYBE_STATES)]
        self._ejectRecognizers()
        logging.debug(self._scannersStr(self._scanners))
        return yeses

    def _ejectRecognizers(self):
        """ Remove scanners according to a scanner ejection policy. """
        self._scanners = list(self._ejector.filtered(self._scanners))

    def unrefuted(self):
        """ Get unrefuted recognizers.

            These recognizers have recognized a problem but are waiting
            until they can be certain that the problem has not yet been
            resolved before committing.

            :returns: a list of recognizers
            :rtype: list of :class:`.recognizer.Recognizer`
        """
        return [s for s in self._scanners if s.state is RecognizerStates.MAYBE_YES]

    def undecided(self):
        """ Get undecided recognizers.

            These recognizers may learn more if given more log.

            :returns: a list of recognizers
            :rtype: list of :class:`.recognizer.Recognizer`

            Note that unrefuted is a subset of undecided.
        """
        return self._scanners[:]
