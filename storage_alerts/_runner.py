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

""" Coordinates running of the whole thing. """

import datetime
import logging

from . import controllers
from . import handlers
from . import sources

class Runner(object):
    """ Runs the whole thing. """

    def __init__(self, log_level=logging.DEBUG):
        logging.basicConfig(filename="storage_alerts.log", level=log_level)
        recognizers = [
            sources.generic.by_line.recognizers.ManyRecognizer(5),
            sources.journal.by_line.recognizers.ProcessRecognizer('python'),
            sources.generic.by_line.recognizers.NoRecognizer(),
            sources.generic.by_line.recognizers.YesRecognizer()
        ]

        self._journal = controllers.time.FromTime(
           datetime.datetime.now(),
           [],
           sources.generic.by_line.LogScanner(
              sources.journal.by_line.Reader(),
              sources.generic.by_line.RecognizerManager(recognizers),
              sources.generic.ejection.NewerDuplicates
           )
        )
        self._handler = handlers.simpleprint.PrintHandler()

    def run(self):
        for rec in self._journal.matches():
            self._handler.doIt(rec.info)
