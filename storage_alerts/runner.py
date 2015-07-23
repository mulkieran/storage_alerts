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

""" For running the entire alert mechanism. """

import datetime

from .sources.journal import Scanner

class Journal(object):
    """ Handles high-level aspects of controlling journal scanning. """

    def __init__(self, recognizers, start_time):
        """ Initializer.

            :param recognizers: a sequence of Recognizer classes
            :type recognizers: sequence of :class:`.sources.journal.Recognizer`
            :param datetime start_time: from when to start next journal scan
        """
        self._start_time = start_time
        self._recognizers = set(recognizers)

    def matches(self):
        """ Returns a list of matches using recognizers from start time.

            Updates start time when done.
        """
        recognizers = Scanner.matches(
           self._recognizers,
           self._start_time,
           None
        )
        for recognizer in recognizers:
            yield recognizer
        self._start_time = datetime.datetime.now()