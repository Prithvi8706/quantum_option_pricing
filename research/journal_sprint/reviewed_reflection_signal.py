"""Versioned sign-endpoint repair; frozen W1/W2 producers remain reproducible."""

from .reflection_centered_signal import ReflectionSignal


class ReviewedReflectionSignal(ReflectionSignal):
    """Assign the negative sign to a nonpositive, nonzero constant interval.

    The inherited constructor rejects intervals strictly crossing zero. An
    interval [negative, 0] can represent a negative real coefficient and must
    use its negative sign. Zero itself contributes no weight, so this choice
    is valid at either endpoint. This changes neither the magnitude interval
    nor the PREP error bound. New experiments must opt into this version.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.negative_constant = self.constant.lo < 0
