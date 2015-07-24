""" Module that implements scanning of journal entries.

    Journal entries are scanned line-by-line from a designated starting time.

    Each journal entry is processed by all registered Recognizer objects.

    Recognizer objects have three states, yes, no, maybe.

    Classes exported by this package:
     * Entry - represents a single journal entry
     * Recognizer - an abstract Recognizer class
     * RecognizerStates - container class for recognizer states
     * Scanner - has one method that scans the journal and yield all matches
       detected by the recognizers.
"""

from ..entry import Entry
from .recognizer import Recognizer
from .recognizer import RecognizerStates
from .scanner import Scanner
