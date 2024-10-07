from line_provider.app.services.exceptions import ScoreIsNotBetween1And5
from line_provider.app.schemas.event import StatusEnum


def calculate_status_by_score(score: int) -> StatusEnum:
    if 5 < score < 1:
        raise ScoreIsNotBetween1And5

    if score >= 3:
        return StatusEnum.HIGH_SCORE

    return StatusEnum.LOW_SCORE
