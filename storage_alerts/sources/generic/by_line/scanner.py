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

""" Scanner classes. """

from .states import RecognizerStates

class LogScanner(object):
    """ Scans for recognizable alerts in a log.

        Essentially combines the actions of the reader, which just
        obtains entries from some log, and a manager, which inspects
        the entries.
    """

    def __init__(self, reader, manager, ejector):
        """ Initializer.

            :param Reader reader: a reader object for the log
            :param Manager manager: a manager for recognizers
        """
        self._READER = reader
        self._MANAGER = manager
        self._EJECTOR = ejector

    def matches(self, start, maybes):
        """ Generate a sequence of recognizer matches.

            :param datetime start: start time
            :param maybes: a list of undecided recognizers
            :type mabyes: list of :class:`Recognizer`
            :returns: a pair of yeses and maybes
            :rtype: tuple of lists of :class:`Recognizer`
        """
        final_yeses = []
        for entry in self._READER.entries(start):
            yeses, maybes = self._MANAGER.processEntry(entry, maybes)
            final_yeses += yeses
            maybes = list(self._EJECTOR.filtered(maybes))
        final_yeses += [s for s in maybes if s.state is RecognizerStates.MAYBE_YES]
        final_yeses = list(self._EJECTOR.filtered(final_yeses))
        return final_yeses, maybes
