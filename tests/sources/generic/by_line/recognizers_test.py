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

from storage_alerts.sources.generic.by_line.recognizers import LazyRecognizer
from storage_alerts.sources.generic.by_line.recognizers import ManyRecognizer
from storage_alerts.sources.generic.by_line.recognizers import NoRecognizer
from storage_alerts.sources.generic.by_line.recognizers import YesRecognizer
from storage_alerts.sources.generic.by_line.states import RecognizerStates

class YesRecognizerTestCase(unittest.TestCase):
    """ Test the recognizer that says yes to any line. """

    def testZero(self):
        """ It always says no at start. """
        rec = YesRecognizer()
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.evidence, [])
        self.assertEqual(len(rec.info), 0)

    def testOne(self):
        """ It says yes whatever it reads. """
        rec = YesRecognizer()
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(len(rec.evidence), 1)
        self.assertEqual(len(rec.info), 0)
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(len(rec.evidence), 1)
        self.assertEqual(len(rec.info), 0)

    def testCopy(self):
        rec = YesRecognizer()
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(len(rec.evidence), 1)
        self.assertEqual(len(rec.info), 0)

        rec2 = rec.initializeNew()
        self.assertEqual(rec2.state, RecognizerStates.NO)
        self.assertEqual(len(rec2.evidence), 0)
        self.assertEqual(len(rec2.info), 0)

        self.assertEqual(rec, rec2)
        self.assertFalse(rec != YesRecognizer())

class MaybeYesRecognizerTestCase(unittest.TestCase):
    """ Test the maybe yes recognizer. """

    def testZero(self):
        """ It always says no at start. """
        rec = LazyRecognizer()
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.evidence, [])
        self.assertEqual(len(rec.info), 0)

    def testOne(self):
        """ It says maybe whatever it reads. """
        rec = LazyRecognizer()
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_YES)
        self.assertEqual(len(rec.evidence), 1)
        self.assertEqual(len(rec.info), 0)
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_YES)
        self.assertEqual(len(rec.evidence), 1)
        self.assertEqual(len(rec.info), 0)

    def testCopy(self):
        """ Test that copy really resets. """
        rec = LazyRecognizer()
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_YES)
        self.assertEqual(len(rec.evidence), 1)
        self.assertEqual(len(rec.info), 0)

        rec2 = rec.initializeNew()
        self.assertEqual(rec2.state, RecognizerStates.NO)
        self.assertEqual(rec2.evidence, [])
        self.assertEqual(len(rec2.info), 0)

        self.assertEqual(rec, rec2)
        self.assertFalse(rec != LazyRecognizer())

class NoRecognizerTestCase(unittest.TestCase):
    """ Test the recognizer that always says no. """

    def testZero(self):
        """ It always says no at start. """
        rec = NoRecognizer()
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.evidence, [])
        self.assertEqual(len(rec.info), 0)

    def testOne(self):
        """ It says no whatever it reads. """
        rec = NoRecognizer()
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.evidence, [])
        self.assertEqual(len(rec.info), 0)

    def testCopy(self):
        """ Test copying. """
        rec = NoRecognizer()
        rec2 = rec.initializeNew()
        self.assertFalse(rec is rec2)
        self.assertEqual(rec, rec2)
        self.assertFalse(rec != NoRecognizer())

class ManyRecognizerTestCase(unittest.TestCase):
    """ Test the many recognizer. """

    def testZero(self):
        """ If zero are enough it should be in yes state already. """
        rec = ManyRecognizer(0)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(rec.evidence, [])
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(rec.evidence, [])

    def testOne(self):
        """ Should behave just like the yes recognizer. """
        rec = ManyRecognizer(1)
        self.assertEqual(rec.state, RecognizerStates.NO)
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(len(rec.evidence), 1)

    def testTwo(self):
        """ If two are required it should pass through the maybe state. """
        rec = ManyRecognizer(2)
        self.assertEqual(rec.state, RecognizerStates.NO)
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_NO)
        self.assertEqual(len(rec.evidence), 1)
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(len(rec.evidence), 2)

    def testInfo(self):
        """ The info is a bunch of key/value pairs. """
        rec = ManyRecognizer(2)
        info = rec.info
        self.assertEqual(info['COUNT'], 0)
        self.assertEqual(info['REQUIRED'], 2)

    def testStr(self):
        """ The description contains some relevant information. """
        rec = ManyRecognizer(2)
        self.assertIn(str(rec.NUMBER), str(rec))

    def testCopy(self):
        """ Test copying. """
        rec = ManyRecognizer(1)
        self.assertEqual(rec.state, RecognizerStates.NO)
        rec.consume(None)
        self.assertEqual(rec.state, RecognizerStates.YES)
        self.assertEqual(len(rec.evidence), 1)

        rec2 = rec.initializeNew()
        self.assertEqual(rec2.state, RecognizerStates.NO)

        self.assertEqual(rec, rec2)
        self.assertNotEqual(rec, ManyRecognizer(2))

class HashTestCase(unittest.TestCase):
    """ Test hashing properties. """

    _RECS = [
       LazyRecognizer(),
       ManyRecognizer(2),
       NoRecognizer(),
       YesRecognizer()
    ]

    def setUp(self):
        self._recs = [r.initializeNew() for r in self._RECS]

    def testEqualNew(self):
        """ Test that newly initialized recognizers hash to same value. """
        for r in self._RECS:
            self.assertEqual(hash(r), hash(r.initializeNew()))
