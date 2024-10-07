class ScoreIsNotBetween1And5(Exception):
    """Score must be between 1 and 5, inclusive.

    If the score is outside of this range, this exception will be raised.
    """
    pass
