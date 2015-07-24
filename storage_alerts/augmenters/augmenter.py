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

""" Abstract classes for augmenting information obtained by recognizers. """

import abc

from collections import defaultdict

from six import add_metaclass

class Key(object):
    """ A key object. """

    def __init__(self, name, owner):
        """ Initializer.

            :param str name: name of key
            :param class owner: key owner
        """
        self._name = name
        self._owner = owner

class KeyFactory(object):
    """ Stores keys belonging to different augmenters. """

    def __init__(self):
        self._keys = defaultdict(dict)

    def getKey(self, name, owner):
        """ Obtain a key from the factory.

            :param str name: the key name
            :param Augmenter owner: the owner of the key

            Constructs a new key if none exists.
        """
        owner_dict = self._keys[type(owner)]
        key = owner_dict.get(name)
        if key is None:
            owner_dict[name] = Key(name, type(owner))
        return owner_dict.get(name)

KeyFactory = KeyFactory()

@add_metaclass(abc.ABCMeta)
class Augmenter(object):
    """ Abstract class for augmenting info from recognizer. """

    KEY_NAMES = abc.abstractproperty("names of keys that might be set")

    @abc.abstractmethod
    def augment(self, info):
        """ Augments info param with additional fields.

            :param dict info: a dict of key/value pairs
            :returns: a list of keys added
            :rtype: list of :class:`Key`
        """
        raise NotImplementedError()
