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

from .states import RecognizerStates

class RecognizerManager(object):
    """ Maintains a set of Recognizer classes. """

    #    Invariants:
    #     * there are no duplicates in self._RECOGNIZERS

    def __init__(self, recognizers):
        """ Initializer.

            :param recognizers: list of recognizer objects
            :type recognizers: list of :class:`Recognizer`
            :param :class:`EjectionPolicy` ejector: an ejection policy
            :param scanners: a list of recognizers
            :type scanners: list of :class:`Recognizer`
        """
        self._RECOGNIZERS = set(recognizers)

    def processEntry(self, entry, scanners):
        """ Process a journal entry.

            :param :class:`.Entry` entry: a journal entry
            :param scanners: a list of current scanners
            :type scanners: list of :class:`.scanner.Recognizer`
            :returns: a list of matching objects, may be empty
            :rtype: list of :class:`.scanner.Recognizer`

            Use all current scanners, which all have state MAYBE_*, and also
            instantiates new objects for every registered scanner class.
        """
        scanners = scanners + [r.initializeNew() for r in self._RECOGNIZERS]
        for scanner in scanners:
            scanner.consume(entry)
        yeses = [s for s in scanners if s.state is RecognizerStates.YES]
        maybes = [s for s in scanners if s.state in (RecognizerStates.MAYBE_STATES)]
        return yeses, maybes
