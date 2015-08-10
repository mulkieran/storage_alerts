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

from storage_alerts.sources.journal.by_line.recognizers.multipath import MessageIDs
from storage_alerts.sources.journal.by_line.recognizers.multipath import MultipathRecognizer
from storage_alerts.sources.journal.by_line.recognizers.multipath import Parsing1
from storage_alerts.sources.journal.entry import Entry
from storage_alerts.sources.generic.by_line.states import RecognizerStates

class Parsing1TestCase(unittest.TestCase):
    """ Test parsing multipath syslog messages. """

    def testParsing1OfflineMessage(self):
        """ Test parsing message indicating offline. """
        message = "WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY: sdk - path offline"
        res = Parsing1.parseMessage(message)
        self.assertEqual(res['MESSAGE_ID'], str(MessageIDs.MID_OFFLINE))

    def testParsing1OnlineMessage(self):
        """ Test parsing message indicating online. """
        message = "WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY: sdk - directio checker reports path is up"
        res = Parsing1.parseMessage(message)
        self.assertEqual(res['MESSAGE_ID'], str(MessageIDs.MID_ONLINE))

    def testParsing1Empty(self):
        """ No failure on an empty message. """
        res = Parsing1.parseMessage("")
        self.assertEqual(res, dict())

    def testParsing1RegMatch(self):
        """ Unmatched message returns an empty dict. """
        res = Parsing1.parseMessage(": - ")
        self.assertEqual(res, dict())

class RecognizerTestCase(unittest.TestCase):
    """ Test the recognizer itself. """

    MESSAGE_UP = 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY: sdk - directio checker reports path is up'
    MESSAGE_DOWN = 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY: sdk - path offline'

    def testIrrelevantProcess(self):
        """ If the process is not multipathd, the message is irrelevant. """
        rec = MultipathRecognizer()
        entry = Entry({
           '_COMM' : 'multipathr',
           'MESSAGE' : self.MESSAGE_DOWN
        })
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(len(rec.evidence), 0)

        rec2 = rec.initializeNew()
        self.assertEqual(rec, rec2)

    def testInitialFunction(self):
        """ Test initial state to recognized state by match. """
        rec = MultipathRecognizer()
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : self.MESSAGE_DOWN
        })
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_YES)
        self.assertEqual(len(rec.evidence), 1)

        info = rec.info
        self.assertEqual(info['DEVICE'], 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY')
        self.assertEqual(info['PATH'], 'sdk')

        rec2 = rec.initializeNew()
        self.assertNotEqual(rec, rec2)

    def testInitialFunction2(self):
        """ Test non-transition on online message. """
        rec = MultipathRecognizer()
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : self.MESSAGE_UP
        })
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.info, dict())

    def testTransitionToFalse(self):
        """ Test transition to True and back to false. """
        rec = MultipathRecognizer()
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : self.MESSAGE_DOWN
        })
        rec.consume(entry)
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : self.MESSAGE_UP
        })
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.NO)
        self.assertEqual(rec.info, dict())

    def testManyOffline1(self):
        """ Two offline state messages about the same device should yield
            the same as one.
        """
        rec = MultipathRecognizer()
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : self.MESSAGE_DOWN
        })
        rec.consume(entry)
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_YES)
        self.assertEqual(len(rec.evidence), 2)

        info = rec.info
        self.assertEqual(info['DEVICE'], 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY')
        self.assertEqual(info['PATH'], 'sdk')

    def testManyOffline2(self):
        """ Two offline state messages about different devices should cause
            second message to be ignored.
        """
        rec = MultipathRecognizer()
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : self.MESSAGE_DOWN
        })
        rec.consume(entry)
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELK: sda - path offline'
        })
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_YES)
        self.assertEqual(len(rec.evidence), 1)

        info = rec.info
        self.assertEqual(info['DEVICE'], 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY')
        self.assertEqual(info['PATH'], 'sdk')

    def testMany(self):
        """ An offline state messages followed by an irrelevant message. """
        rec = MultipathRecognizer()
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : self.MESSAGE_DOWN
        })
        rec.consume(entry)
        entry = Entry({
           '_COMM' : 'multipathr',
           'MESSAGE' : 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELK: sda - path offline'
        })
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_YES)
        self.assertEqual(len(rec.evidence), 1)

        info = rec.info
        self.assertEqual(info['DEVICE'], 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY')
        self.assertEqual(info['PATH'], 'sdk')

    def testMany2(self):
        """ An offline state messages followed by an irrelevant message.
            Unlike the other, this originated w/ multipathd.
        """
        rec = MultipathRecognizer()
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : self.MESSAGE_DOWN
        })
        rec.consume(entry)
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELK: sda - irrelevant'
        })
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_YES)
        self.assertEqual(len(rec.evidence), 1)

        info = rec.info
        self.assertEqual(info['DEVICE'], 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY')
        self.assertEqual(info['PATH'], 'sdk')

    def testDifferentOnline(self):
        """ Test online message that does not match offline message. """
        rec = MultipathRecognizer()
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : self.MESSAGE_DOWN
        })
        rec.consume(entry)
        message = 'WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELK: sda - directio checker reports path is up'
        entry = Entry({
           '_COMM' : 'multipathd',
           'MESSAGE' : message
        })
        rec.consume(entry)
        self.assertEqual(rec.state, RecognizerStates.MAYBE_YES)

class HashTestCase(unittest.TestCase):
    """ Test hashing. """

    def testEqual(self):
        """ Test equality of hash's after initialization. """
        rec = MultipathRecognizer()
        self.assertEqual(hash(rec), hash(rec.initializeNew()))
