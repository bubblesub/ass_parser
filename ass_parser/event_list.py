"""ASS events container."""
from ass_parser.event import AssEvent
from ass_parser.observable_sequence import ObservableSequence


class AssEventList(ObservableSequence[AssEvent]):
    """ASS events container."""
