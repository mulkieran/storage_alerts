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

""" Test for scanners. """
import unittest
import datetime

from storage_alerts.sources.generic.by_line.ejection import NewerDuplicates
from storage_alerts.sources.generic.by_line.ejection import NoneEjector
from storage_alerts.sources.generic.by_line.manager import RecognizerManager
from storage_alerts.sources.generic.by_line.recognizers import LazyRecognizer
from storage_alerts.sources.generic.by_line.recognizers import ManyRecognizer
from storage_alerts.sources.generic.by_line.recognizers import YesRecognizer
from storage_alerts.sources.generic.by_line.scanner import LogScanner
from storage_alerts.sources.generic.by_line.reader import NullReader

class ScannerTestCase(unittest.TestCase):
    """ Test a scanner. """

    def testEmpty(self):
        """ The manager does not recognize, so no results. """
        manager = RecognizerManager([])
        reader = NullReader(10)
        scanner = LogScanner(reader, manager, NoneEjector)
        yeses, maybes = scanner.matches(datetime.datetime.now, [])
        self.assertEqual(len(yeses), 0)
        self.assertEqual(len(maybes), 0)

    def testYes(self):
        """ The manager always says yes, and never filters. """
        manager = RecognizerManager([YesRecognizer()])
        reader = NullReader(10)
        scanner = LogScanner(reader, manager, NoneEjector)
        yeses, maybes = scanner.matches(datetime.datetime.now, [])
        self.assertEqual(len(yeses), 10)
        self.assertEqual(len(maybes), 0)

    def testMaybeYes(self):
        """ Lazy recognizers do not say yes until log is read. """
        manager = RecognizerManager([LazyRecognizer()])
        reader = NullReader(10)
        scanner = LogScanner(reader, manager, NoneEjector)
        yeses, maybes = scanner.matches(datetime.datetime.now, [])
        self.assertEqual(len(yeses), 10)
        self.assertEqual(len(maybes), 10)

    def testMaybeNo(self):
        """ Many recognizers says no if it does not get enough entries. """
        manager = RecognizerManager([ManyRecognizer(11)])
        reader = NullReader(10)
        scanner = LogScanner(reader, manager, NoneEjector)
        yeses, maybes = scanner.matches(datetime.datetime.now, [])
        self.assertEqual(len(yeses), 0)
        self.assertEqual(len(maybes), 10)

    def testEjection(self):
        """ Ejecting all newer duplicates should leave just 1. """
        manager = RecognizerManager([YesRecognizer()])
        reader = NullReader(10)
        scanner = LogScanner(reader, manager, NewerDuplicates)
        yeses, maybes = scanner.matches(datetime.datetime.now, [])
        self.assertEqual(len(yeses), 10)
        self.assertEqual(len(maybes), 0)

    def testCurrentScanner(self):
        """ Show that passing in process scanners builds on previous. """
        manager = RecognizerManager([ManyRecognizer(11)])
        reader = NullReader(10)
        scanner = LogScanner(reader, manager, NoneEjector)
        yeses, maybes = scanner.matches(datetime.datetime.now, [])
        self.assertEqual(len(yeses), 0)
        self.assertEqual(len(maybes), 10)

        # take all undecided scanners from previous run and reuse
        many_recognizers = maybes
        manager = RecognizerManager([])
        reader = NullReader(5)
        scanner = LogScanner(reader, manager, NoneEjector)
        yeses, maybes = scanner.matches(datetime.datetime.now, many_recognizers)
        self.assertEqual(len(yeses), 5)
        self.assertEqual(len(maybes), 5)
