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

from .recognizer import RecognizerStates

class RecognizerManager(object):
    """ Maintains a set of Recognizer classes. """

    #    Invariants:
    #     * all scanner objects in self._scanners are in MAYBE state
    #     * there are no duplicate classes in self._klasses

    def __init__(self, klasses):
        """ Initializer.

            :param klasses: list of Recognizer classes
            :type klasses: any sequence-like object
        """
        self._scanners = []
        self._klasses = set(klasses)

    def processEntry(self, entry):
        """ Process a journal entry.

            :param :class:`.Entry` entry: a journal entry
            :returns: a list of matching objects, may be empty
            :rtype: list of :class:`.scanner.Recognizer`

            Use all current scanners, which all have state MAYBE, and also
            instantiates new objects for every registered scanner class.
        """
        scanners = self._scanners + [c() for c in self._klasses]
        for scanner in scanners:
            scanner.consume(entry)
        yeses = [s for s in scanners if s.state == RecognizerStates.YES]
        self._scanners = [s for s in scanners if s.state == RecognizerStates.MAYBE]
        self._cullRecognizers()
        return yeses

    def _cullRecognizers(self):
        """ Remove scanners according to a scanner ejection policy. """
        pass
