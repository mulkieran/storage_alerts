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

from . import controllers
from . import examples
from . import handlers
from . import scanner
from . import sources

class Runner(object):
    """ Runs the whole thing. """

    def __init__(self):
        recognizers = [
            examples.journal.by_line.hundred.HundredRecognizer,
            examples.journal.by_line.no.NoRecognizer,
            examples.journal.by_line.yes.YesRecognizer
        ]
        self._journal = controllers.time.FromTime(
           recognizers,
           datetime.datetime.now(),
           scanner.LogScanner(
              sources.journal.by_line.Reader(),
              sources.generic.by_line.RecognizerManager(recognizers)
           )
        )
        self._handler = handlers.simpleprint.PrintHandler()

    def run(self):
        for rec in self._journal.matches():
            self._handler.doIt(rec.info)
