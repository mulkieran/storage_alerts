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

""" Test recognizers. """
import unittest

from storage_alerts.sources.journal.by_line.recognizers import ProcessRecognizer
from storage_alerts.sources.journal.entry import Entry
from storage_alerts.sources.generic.by_line.states import RecognizerStates

class ProcessRecognizerTestCase(unittest.TestCase):
    """ Test the recognizer that says yes to a process. """

    def testMessageWithProcess(self):
        """ Test recognition. """
        rec = ProcessRecognizer("python")
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.evidence, [])
        self.assertEqual(len(rec.info), 0)
        entry = Entry({'_COMM': 'python'})
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(rec.evidence, [entry])
        self.assertEqual(len(rec.info), 0)

    def testMessageNoProcess(self):
        """ Test non-recognition. """
        rec = ProcessRecognizer("python")
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.evidence, [])
        self.assertEqual(len(rec.info), 0)
        entry = Entry({'_COMM': 'systemd'})
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.evidence, [])
        self.assertEqual(len(rec.info), 0)

    def testStr(self):
        """ Test that str has relevant information. """
        rec = ProcessRecognizer("python")
        self.assertIn(rec.PROCESS, str(rec))

    def testCopy(self):
        """ Test copying. """
        rec = ProcessRecognizer("python")
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.evidence, [])
        self.assertEqual(len(rec.info), 0)
        entry = Entry({'_COMM': 'python'})
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(rec.evidence, [entry])
        self.assertEqual(len(rec.info), 0)

        rec2 = rec.initializeNew()
        self.assertEqual(rec2.state, RecognizerStates.NO)
        self.assertEqual(rec2.evidence, [])
        self.assertEqual(len(rec2.info), 0)
        entry = Entry({'_COMM': 'python'})
        rec2.consume(entry)
        self.assertEqual(rec2.state, RecognizerStates.YES)
        self.assertEqual(rec2.evidence, [entry])
        self.assertEqual(len(rec2.info), 0)

        self.assertEqual(rec, rec2)
        self.assertNotEqual(rec, ProcessRecognizer("multipathd"))

class HashTestCase(unittest.TestCase):
    """ Test hashing properties. """

    def testEqualNew(self):
        """ Test that a new process recognizer hashes to the same value. """
        rec = ProcessRecognizer("random")
        self.assertEqual(hash(rec), hash(rec.initializeNew()))
