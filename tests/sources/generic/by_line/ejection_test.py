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

""" Test for ejection policies. """
import unittest

from storage_alerts.sources.generic.by_line.ejection import EjectionPolicy
from storage_alerts.sources.generic.by_line.ejection import NewerDuplicates

class AbstractParentTestCase(unittest.TestCase):
    """ Test that abstract parent does not do anything. """

    def testInvocation(self):
        """ Abstract parent does not filter. """
        with self.assertRaises(NotImplementedError):
            EjectionPolicy.filtered([])

class NewerDuplicatesTestCase(unittest.TestCase):
    """ Test ejection of newer duplicates. """

    def testEjection(self):
        """ Test that appropriate scanners are ejected. """
        scanners = [1, 2, 3, "a", "b", "c", 4]
        self.assertEqual(list(NewerDuplicates.filtered(scanners)), [1, "a"])

    def testEmpty(self):
        """ Test that empty list is handled correctly. """
        scanners = []
        self.assertEqual(list(NewerDuplicates.filtered(scanners)), [])
