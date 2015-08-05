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

""" Test for managers. """
import unittest

from storage_alerts.sources.generic.by_line.ejection import NoneEjector
from storage_alerts.sources.generic.by_line.manager import RecognizerManager
from storage_alerts.sources.generic.by_line.recognizers import LazyRecognizer
from storage_alerts.sources.generic.by_line.recognizers import YesRecognizer

class ManagerTestCase(unittest.TestCase):
    """ Test a manager. """

    def testEmpty(self):
        """ Test that an entry w/out any recognizers is correctly processed. """
        manager = RecognizerManager([], NoneEjector)
        self.assertEqual(manager.processEntry(None), [])
        self.assertEqual(len(manager.unrefuted()), 0)

    def testYes(self):
        """ Test with an always true recognizer. """
        manager = RecognizerManager([YesRecognizer], NoneEjector)
        self.assertEqual(len(manager.processEntry(None)), 1)
        self.assertEqual(len(manager.unrefuted()), 0)

    def testLazy(self):
        """ Test with a lazy recognizer. """
        manager = RecognizerManager([LazyRecognizer], NoneEjector)
        self.assertEqual(len(manager.processEntry(None)), 0)
        self.assertEqual(len(manager.unrefuted()), 1)
