Storage Alerts
==============

A framework for detecting, classifying, and remediating storage failures.

Architecture
------------

The current architecture is very dispersed and abstracted because:

* It should be modular in a way that makes writing recognizers straightforward.
* It is not clear what the best approach is at this time.

Some parts of the directory tree are more concrete than other parts which
are just placeholders for possible alternative approaches.

One principle is that the framework should be retargetable. Therefore, the
sources of the alerts are separated from the ways of propagating the alerts
to clients. This is analogous to the distinction between a compiler's front
and back end.

Reading from the Journal
------------------------

The concrete part being explored is reading and interpreting messages from
the journal. At this point, there is an example implementation of a framework
for doing this in storage_alerts/sources/journal. There are two basic
approaches to interepreting messages from the journal:

* Reading each entry in the journal and deciding whether it can be used to identify any category of error.

* Scanning the journal for each category of possible error.

These approaches can be combined in various ways. Currently, the first approach
is taken, because it is the simplest to implement. The other approach,
because it uses journald's searching capability more, might be faster.
The implementation of this line-by-line approach is in the subdirectory
storage_alerts/sources/journal/by_line.

Since the only parts of reading from the journal that are really journal
specific are the journal entries, the interface that actually reads entries,
and the recognizers that are tailored to journal entries, most of the
implementation is actually located in storage_alerts/sources/generic/by_line.

The basic algorithm is described below:

* Open the journal
* Read each entry starting at a specified time and continuing until the end of the journal.

  * Initialize list of maybes to the empty list
  * For each entry, e:

    * For each recognizer, r in maybes + list of new recognizers for category

      * r processes e, and may change to a new internal state
      * if r's state is YES, add it to yeses
      * if r's state is NO, remove it
      * if r's state is a MAYBE_*, add it to maybes

  * Return yeses and maybes separately

Note that the scanner may filter the yeses and maybes, in case some of the 
members of either list are redundant.

The generic subdirectory contains a bunch of extremely generic recognizers.
These are useful only in exercising the framework.

The file storage_alerts/sources/journal/by_line/recognizers/multipath.py
contains a practical example of a recognizer that can detect if a path is
down. It is a simple recognizer based on a two-state finite
state machine. It detects a failed path nicely, and, if the path is brought
back up, will progress to a NO state so that it can be removed.

It also illustrates some of the problems that this approach presents.

In the first place, the MESSAGE field of the entry must be parsed to
identify the meaning of the journal entry. This is really undesirable, for
reasons that I assume are obvious to all readers. For this reason, the
parsing activity is isolated in a separate class, and the parsing is
used to generate a set of key/value pairs that the rest of the implementation
consumes. In particular, the parser generates a MESSAGE_ID field, which
is intended to uniquely indentify the message type. In a final implementation,
the Parsing1 class should disappear entirely, while the key/value pairs
that are required should be supplied by the log entry itself.

In the second place, even the MESSAGE field does not necessarily contain
all the information that a consumer of this information might require.
Multipath communicates a failure of a path in two ways, illustrated by the
Parsing1 and Parsing2 classes. In the first, the message contains the
id of the multipath device and the path. In the second, one message contains
the major and minor numbers and the id of the device, while the other just
contains the major and minor numbers.

Harness
--------------------------
Currently the implementation is just run from a simple interactive harness.

The file storage_alerts/controllers/time.py contains a simple class that
saves the completion time of the last journal read, so that the next read
of the journal can be started from that time.

The file storage_alerts/handlers/simpleprint.py contains a rudimentary
handler that simply prints the information provided it by a recognizer.
In a complete implementation, the handlers directory would contain more
useful handlers to communicate with clients of the framework.

The storage_alerts/augmenters directory contains nothing of interest at
this time. It is intended to hold classes that can extend the information
extracted from journal entries to give more useful information to handlers,
and therefore consumers of the alerts.
