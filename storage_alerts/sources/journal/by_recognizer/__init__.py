""" Each recognizer interrogates the journal for information of interest.

    There is a designated time-from for each recognizer.

    This is an alternative to the journal-line-by-line option.

    The major advantage is that it makes use of the journal's own searching
    mechanism. It is not known whether there would be an overall
    performance gain from this approach.

    The disadvantage is that it places a greater burden on the writer of
    each recognizer to understand the operation of the journal, as each
    recognizer must construct its own journal queries.

    It is believed that the two approaches are equivalent in expressiveness.
"""
