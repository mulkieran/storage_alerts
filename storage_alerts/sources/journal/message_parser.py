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

""" Abstract parser that recognizers can use. """

import abc

from six import with_metaclass

class MessageParser(with_metaclass(abc.ABCMeta, object)):
    """ An abstract message parser class for journal entries. """

    @abc.abstractmethod
    def parseMessage(self, message):
        """ Parse a journal message returning a dict of key/value pairs.

            :param str message: contents of log MESSAGE field
            :returns: a dict of key/value pairs, empty if non-matching
            :rtype: dict
        """
        raise NotImplementedError() #pragma: no cover
