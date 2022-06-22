import numpy as np
from signals.base_signal import Signal, Const
from signals.simple_signals import Step
from signals.complex_signals import CosineSmoothedStep


def RandomizedStepSequence(
    t_max: float,
    ampl_max: float,
    block_width: float,
    start_with_zero: bool = True,
    n_levels: int = 10,
    vary_timings: float = 0.0,
) -> Signal:

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
        signal += (b - a) * Step(t_start=t0)

    return signal


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
