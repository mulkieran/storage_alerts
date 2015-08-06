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

""" States of a line-by-line recognizer. """

class _RecognizerState(object):
    """ Class for defining enumeration of states of a scanner. """

    def __init__(self, desc):
        """ Initializer.

            :param str desc: meaning of scanner state
        """
        self._DESC = desc

    def __str__(self):
        return self._DESC
    __repr__ = __str__

class RecognizerStates(object):
    """ Organizes all allowed states of a scanner object. """

    MAYBE_NO = _RecognizerState(
       "May be in the process of recognizing the error."
    )
    MAYBE_YES = _RecognizerState(
        "Has recognized an error which may be invalidated."
    )
    YES = _RecognizerState("The error has been recognized.")
    NO = _RecognizerState("The entry just read does not indicate the error.")

    MAYBE_STATES = (MAYBE_NO, MAYBE_YES)
