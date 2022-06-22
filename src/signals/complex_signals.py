from dataclasses import dataclass
from signals.base_signal import Signal
from signals.simple_signals import Sinusoid, Ramp
import numpy as np


class SeeSaw(Signal):
    """Alternating linear zigzag signal with a constant amplitude and frequency."""

    def __init__(
        self, t_start: float, t_end: float, ampl: float = 1.0, freq: float = 1.0
    ):
        super().__init__(t_start, t_end)
        self.halfperiod = 1 / (2 * freq)
        self.sine = Sinusoid(ampl=ampl, freq=freq)

        # Sample the discrete points from the sinusoid:
        self.sampling_times = np.arange(
            self.t_start - self.halfperiod / 2, t_end + self.halfperiod, self.halfperiod
        )

        # Correct for the half-period shift
        self.sampling_times[0] = self.t_start

        # Discrete samples
        self.samples = np.array([self.sine(t) for t in self.sampling_times])

    def _signal(self, t: float) -> float:
        return np.interp(t, self.sampling_times, self.samples)


@dataclass
class RampSinusoid(Signal):
    ampl_max: float = 1.0
    freq: float = 1.0

    def __post_init__(self):
        rate = self.ampl_max / (self.t_end - self.t_start)
        self.sine = rate * Ramp(t_start=self.t_start) * Sinusoid(freq=self.freq)

    def _signal(self, t: float) -> float:
        return self.sine(t)


class AlternatingRamp(Signal):
    """Alternating linear zigzag signal with a linearly increasing amplitude and frequency."""

    def __init__(
        self, t_start: float, t_end: float, ampl_max: float = 1.0, freq: float = 1.0
    ):
        super().__init__(t_start, t_end)
        self.ampl_max = ampl_max
        self.freq = freq

        self.period = 1 / freq
        self.halfperiod = 1 / (2 * freq)

        rate = self.ampl_max / (self.t_end - self.t_start)
        self.sine = rate * Ramp(t_start=self.t_start) * Sinusoid(freq=self.freq)

        # Sample the discrete points from the sinusoid:
        self.sampling_times = np.arange(
            self.t_start - self.halfperiod / 2, t_end + self.halfperiod, self.halfperiod
        )

        # Correct for the half-period shift
        self.sampling_times[0] = self.t_start

        # Discrete samples
        self.samples = np.array([self.sine(t) for t in self.sampling_times])

    def _signal(self, t: float) -> float:
        return np.interp(t, self.sampling_times, self.samples)


@dataclass
class CosineSmoothedStep(Signal):
    width: float = 1.0

    def _signal(self, t: float) -> float:
        if t < self.width:
            return -(np.cos(np.pi * t / self.width) - 1) / 2
        else:
            return 1.0


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # s1 = CosineSmoothedStep(t_start=5.0, width=2.0)
    # s2 = -2.0 * CosineSmoothedStep(t_start=15.0, width=4.0)
    #
    # s = s1 + s2
    # Casper's training signal for theta
    T = 20.0
    A = np.deg2rad(np.random.choice([20, 15, -15, 20]))

    s1 = A * CosineSmoothedStep(t_start=-1.0, width=2.0)
    s2 = -0.5 * A * CosineSmoothedStep(t_start=0.25 * T, width=0.5)
    s3 = -1.5 * A * CosineSmoothedStep(t_start=0.50 * T, width=1.5)
    s4 = -0.5 * A * CosineSmoothedStep(t_start=0.75 * T, width=0.5)

    s = s1 + s2 + s3 + s4

    # Plot s
    tt = np.arange(0, 20, 0.001)
    ss = []
    for t_i in tt:
        ss.append(s(t_i))

    plt.plot(tt, ss)
    plt.grid()
    plt.show()
