import random
import numpy as np
from signals.base_signal import Signal, Const
from signals.simple_signals import Step
from signals.complex_signals import CosineSmoothedStep
from dataclasses import dataclass


@dataclass(kw_only=True)
class RandomizedStepSequence(Signal):
    block_width: float = 1.0
    max_ampl: float = 1.0
    timing_offset_variance: float = 0.0
    start_with_zero: bool = True

    def __post_init__(self):

        # Generate a bunch of steps from start to end
        assert self.t_start != np.NINF
        assert self.t_end != np.PINF

        self.steps = Const(0.0)
        t_start = (
            self.t_start + self.block_width if self.start_with_zero else self.t_start
        )
        t_end = (
            t_start + 2 * self.block_width
            if self.start_with_zero
            else self.t_start + self.block_width
        )
        while t_end < self.t_end:
            ampl = random.uniform(-self.max_ampl, self.max_ampl)
            self.steps = self.steps + ampl * Step(t_start=t_start, t_end=t_end)
            t_start = t_end

            # Add random variation to the block width
            delta_block_width = np.random.uniform(
                -self.timing_offset_variance, self.timing_offset_variance
            )

            t_end += self.block_width + delta_block_width

    def _signal(self, t: float) -> float:
        return self.steps(t)


def RandomizedCosineStepSequence(
    t_max: float,
    ampl_max: float,
    block_width: float,
    smooth_width: float,
    start_with_zero: bool = True,
    n_levels: int = 10,
    vary_timings: float = 0.0,
) -> Signal:

    assert (
        smooth_width < block_width
    ), "Smoothed region must be shorter than block width"

    assert (
        t_max / block_width < n_levels
    ), "You must provide more levels than individual generated blocks (random choice is without replacement) "

    assert (
        vary_timings < block_width / 2
    ), "vary timings should be smaller than half block width"

    # Starting time of each step block
    t_starts = np.arange(0, t_max, block_width)

    # Possible choices
    ampl_choices = np.linspace(-ampl_max, ampl_max, n_levels)

    # Generate random amplitudes
    amplitudes = np.random.choice(ampl_choices, size=t_starts.size, replace=False)

    if start_with_zero:
        amplitudes[0] = 0.0

    signal = Const(0.0)

    for idx, t0 in enumerate(t_starts):
        # Vary the timings of the time array:
        t0 = t0 + np.random.uniform(-vary_timings, vary_timings)

        if idx == 0:
            a = 0
        else:
            a = amplitudes[idx - 1]
        b = amplitudes[idx]
        signal += (b - a) * CosineSmoothedStep(t_start=t0, width=smooth_width)

    return signal


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    T = 30.0
    s = RandomizedCosineStepSequence(
        t_max=T,
        ampl_max=25,
        block_width=9,
        smooth_width=3.0,
        n_levels=10,
        vary_timings=0.1,
    )

    tt = np.arange(0, T, 0.001)
    ss = []
    for t_i in tt:
        ss.append(s(t_i))

    plt.plot(tt, ss)
    plt.grid()
    plt.show()
