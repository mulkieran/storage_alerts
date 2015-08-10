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

""" A multipath failures recognizer. """

import re

from uuid import UUID

from ....generic.by_line.recognizer import Recognizer
from ....generic.by_line.states import RecognizerStates

class _States(object):
    INITIAL = 0
    RECOGNIZED = 1

class MessageIDs(object):
    """ Class for message ids. """
    MID_OFFLINE = UUID('25a9f021-5c61-49db-974c-6e1000740332')
    MID_ONLINE = UUID('3fe62535-e4d6-4d09-a2ff-8b97057e689c')

class Parsing1(object):
    """ A class to hold all message parsing activity for handling online
        and offline messages.

        Examples:
         * WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY: sdk - path offline
         * WDC_WD10EFRX-68PJCN0_WD-WCC4JLHVDELY: sdk - directio checker reports path is up

        Fields are:
         * DEVICE
         * PATH
         * STATUS

        Also, fake up a MESSAGE_ID field, based on what the message is
        discovered to be.

        The plan is for this to ultimately go away.
    """

    @staticmethod
    def parseMessage(message):
        """ Break the message up into key/value pairs.

            :param str message: contents of log MESSAGE field
            :returns: a dict of key/value pairs, empty if non-matching
        """
        res = {}

        match = re.match(r'(?P<DEVICE>.*):(?P<PATH>.*) - (?P<status>.*)', message)
        if match:
            match = match.groupdict()
            for k in match:
                match[k] = match[k].strip()

            status_str = str(match['status'])
            del match['status']
            if status_str.endswith('path offline'):
                res['MESSAGE_ID'] = str(MessageIDs.MID_OFFLINE)
                res['%s:STATUS' % MessageIDs.MID_OFFLINE] = 'offline'
            elif status_str.endswith('path is up'):
                res['MESSAGE_ID'] = str(MessageIDs.MID_ONLINE)
                res['%s:STATUS' % MessageIDs.MID_ONLINE] = 'online'

            mid = res.get('MESSAGE_ID')
            if mid:
                for k in match:
                    res[mid + ":" + k] = match[k]

        return res

class MultipathRecognizer(Recognizer):
    """ A recognizer that detects one kind of multipath failure. """

    _HASH = ord('M')
    description = "detects one kind of multipath failure"

    def __init__(self):
        self._PROCESS = "multipathd"
        self._evidence = []
        self.fsmstate = _States.INITIAL
        self.device = None
        self.path = None

    def initializeNew(self):
        return MultipathRecognizer()

    def __eq__(self, other):
        return type(other) is MultipathRecognizer and \
           self.fsmstate is other.fsmstate and \
           self.device == other.device and \
           self.path == other.path

    def __ne__(self, other):
        return type(other) is not MultipathRecognizer or \
           self.fsmstate is not other.fsmstate or \
           self.device != other.device or \
           self.path != other.path

    def __hash__(self):
        return self._HASH

    def _initialFunc(self, entry):
        """ Func for INITIAL state.

            :param :class:`..entry.Entry` entry: a journal entry
            :returns: the new state of the recognizer
            :rtype: a fields of _STATES class
        """
        fields = entry.fields
        comm = fields.get("_COMM")

        if comm == self._PROCESS:
            mid = fields.get("MESSAGE_ID")
            if mid == str(MessageIDs.MID_OFFLINE):
                self._evidence.append(entry)
                self.device = fields.get('%s:DEVICE' % mid)
                self.path = fields.get('%s:PATH' % mid)
                return _States.RECOGNIZED

        return _States.INITIAL

    def _recognizedFunc(self, entry):
        """ Func for RECOGNIZED state.

            :param :class:`..entry.Entry` entry: a journal entry
            :returns: the new state of the recognizer
            :rtype: a fields of _STATES class
        """
        fields = entry.fields
        comm = fields.get("_COMM")

        if comm == self._PROCESS:
            mid = fields.get('MESSAGE_ID')
            if mid == str(MessageIDs.MID_OFFLINE):
                device = fields.get('%s:DEVICE' % mid)
                path = fields.get('%s:PATH' % mid)
                if self.device == device and self.path == path:
                    self._evidence.append(entry)
                return _States.RECOGNIZED
            elif mid == str(MessageIDs.MID_ONLINE):
                device = fields.get('%s:DEVICE' % mid)
                path = fields.get('%s:PATH' % mid)
                if self.device == device and self.path == path:
                    self._evidence.append(entry)
                    return _States.INITIAL
                return _States.RECOGNIZED
            else:
                return _States.RECOGNIZED

        return _States.RECOGNIZED

    def _consume(self, entry):
        """ Consumes a journal entry.

            :param :class:`..entry.Entry` entry: a journal entry
        """
        message_dict = Parsing1.parseMessage(entry.fields.get("MESSAGE", ""))
        entry.fields.update(message_dict)
        if self.fsmstate is _States.INITIAL:
            self.fsmstate = self._initialFunc(entry)
        else:
            self.fsmstate = self._recognizedFunc(entry)

    @property
    def state(self):
        if self.fsmstate is _States.RECOGNIZED:
            return RecognizerStates.MAYBE_YES
        return RecognizerStates.NO

    @property
    def evidence(self):
        return self._evidence

    @property
    def info(self):
        if self.fsmstate is _States.RECOGNIZED:
            return {
               'DEVICE' : self.device,
               'PATH' : self.path
            }
        return dict()
