from fractions import Fraction

from digitar.temporal import Time

BEATS_PER_MINUTE = 75
BEATS_PER_MEASURE = 4
NOTE_VALUE = Fraction(1, 4)


class MeasureTiming:
    BEAT = Time(seconds=60 / BEATS_PER_MINUTE)
    MEASURE = BEAT * BEATS_PER_MEASURE


class Note:
    WHOLE = MeasureTiming.BEAT * NOTE_VALUE.denominator
    SEVEN_SIXTEENTH = WHOLE * Fraction(7, 16)
    FIVE_SIXTEENTH = WHOLE * Fraction(5, 16)
    THREE_SIXTEENTH = WHOLE * Fraction(3, 16)
    ONE_EIGHTH = WHOLE * Fraction(1, 8)
    ONE_SIXTEENTH = WHOLE * Fraction(1, 16)
    ONE_THIRTY_SECOND = WHOLE * Fraction(1, 32)


class StrummingSpeed:
    SLOW = Time.from_milliseconds(40)
    FAST = Time.from_milliseconds(20)
    SUPER_FAST = Time.from_milliseconds(5)
