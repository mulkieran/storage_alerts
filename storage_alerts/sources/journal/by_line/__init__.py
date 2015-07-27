""" Module that implements scanning of journal entries.

    Journal entries are scanned line-by-line from a designated starting time.

    Each journal entry is processed by all registered Recognizer objects.

    Recognizer objects have three states, yes, no, maybe.

    Classes exported by this package:
     * Entry - represents a single journal entry
     * Scanner - has one method that scans the journal and yield all matches
       detected by the recognizers.
"""

from ..entry import Entry
from .scanner import Scanner
