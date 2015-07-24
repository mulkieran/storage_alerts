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

""" Abstract Scanner class. """

import abc

from six import add_metaclass

@add_metaclass(abc.ABCMeta)
class Scanner(object):
    """ Scans for recognizable alerts. """

    @staticmethod
    @abc.abstractmethod
    def matches(klasses, start, end=None):
        """ Generate a sequence of recognizer matches.

            :param klasses: a sequence of Recognizer classes
            :type klasses: any sequence-like object
            :param datetime start: start time
            :param end: end time, may be None
            :type end: datetime or NoneType
        """
        raise NotImplementedError()
