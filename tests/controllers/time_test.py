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

from storage_alerts.controllers.time import FromTime
from storage_alerts.sources.generic.by_line.manager import RecognizerManager
from storage_alerts.sources.generic.by_line.recognizers import YesRecognizer
from storage_alerts.sources.generic.by_line.scanner import LogScanner
from storage_alerts.sources.generic.by_line.reader import NullReader
from storage_alerts.sources.generic.ejection import NoneEjector

class ScannerTestCase(unittest.TestCase):
    """ Test a scanner. """

    def testEmpty(self):
        """ The manager does not recognize, so no results. """
        manager = RecognizerManager([])
        reader = NullReader(10)
        scanner = LogScanner(reader, manager, NoneEjector)

        timer = FromTime(datetime.datetime.now(), [], scanner)
        yeses = list(timer.matches())
        self.assertEqual(len(yeses), 0)

    def testYes(self):
        """ The manager recognizes every line. """
        manager = RecognizerManager([YesRecognizer()])
        reader = NullReader(10)
        scanner = LogScanner(reader, manager, NoneEjector)

        timer = FromTime(datetime.datetime.now(), [], scanner)
        yeses = list(timer.matches())
        self.assertEqual(len(yeses), 10)

        yeses = list(timer.matches())
        self.assertEqual(len(yeses), 10)
