from dataclasses import dataclass
from functools import cache
from itertools import cycle
from typing import Iterator, Sequence

import numpy as np

from digitar.burst import BurstGenerator, WhiteNoise
from digitar.chord import Chord
from digitar.instrument import PluckedStringInstrument
from digitar.processing import normalize, remove_dc
from digitar.stroke import Direction, Velocity
from digitar.temporal import Hertz, Time

AUDIO_CD_SAMPLING_RATE = 44100


@dataclass(frozen=True)
class Synthesizer:
    instrument: PluckedStringInstrument
    burst_generator: BurstGenerator = WhiteNoise()
    sampling_rate: int = AUDIO_CD_SAMPLING_RATE

    @cache
    def strum_strings(
        self, chord: Chord, velocity: Velocity, vibration: Time | None = None
    ) -> np.ndarray:
        if vibration is None:
            vibration = self.instrument.vibration

        if velocity.direction is Direction.UP:
            stroke = self.instrument.upstroke
        else:
            stroke = self.instrument.downstroke

        sounds = tuple(
            self.vibrate(pitch.frequency, vibration, self.instrument.damping)
            for pitch in stroke(chord)
        )

        return self._overlay(sounds, velocity.delay)

    @cache
    def _vibrate(
        self, frequency: Hertz, duration: Time, damping: float = 0.5
    ) -> np.ndarray:
        assert 0 < damping <= 0.5
        return normalize(
            remove_dc(
                np.fromiter(
                    feedback_loop(),
                    np.float64,
                    duration.get_num_samples(self.sampling_rate),
                )
            )
        )

        def feedback_loop() -> Iterator[float]:
            buffer = self.burst_generator(
                num_samples=round(self.sampling_rate / frequency),
                sampling_rate=self.sampling_rate,
            )
            for i in cycle(range(buffer.size)):
                yield (current_sample := buffer[i])
                next_sample = buffer[(i + 1) % buffer.size]
                buffer[i] = (current_sample + next_sample) * damping

            return np.fromiter(
                feedback_loop(),
                np.float64,
                duration.get_num_samples(self.sampling_rate),
            )

        def _overlay(self, sounds: Sequence[np.ndarray], delay: Time) -> np.ndarray:
            num_delay_samples = delay.get_num_samples(self.sampling_rate)
            num_samples = max(
                i * num_delay_samples + sound_size for i, sound in enumerate(sounds)
            )
            samples = np.zeros(num_samples, dtype=np.float64)
            for i, sound in enumerate(sounds):
                offset = i * num_delay_samples
                samples[offset : offset + sound_size] += sound
            return samples
