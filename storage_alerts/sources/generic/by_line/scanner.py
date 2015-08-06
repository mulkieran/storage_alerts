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

class LogScanner(object):
    """ Scans for recognizable alerts in a log. """

    def __init__(self, reader, manager):
        """ Initializer.

            :param Reader reader: a reader object for the log
            :param Manager manager: a manager for recognizers
        """
        self._reader = reader
        self._manager = manager

    def matches(self, start):
        """ Generate a sequence of recognizer matches.

            :param datetime start: start time
            :returns: a generator of scanner matches
            :rtype: generator of :class:`Recognizer`
        """
        for entry in self._reader.entries(start):
            for scanner in self._manager.processEntry(entry):
                yield scanner
        for scanner in self._manager.unrefuted():
            yield scanner

    def undecided(self):
        """ Scanners that have not said yes or no.

            :returns: a list of recognizers
            :rtype: list of :class:`Recognizer`

            Note that all recognizers will be in an undecided state.
        """
        return self._manager.undecided()
