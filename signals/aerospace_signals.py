from dataclasses import dataclass
from signals.base_signal import Signal
from signals.simple_signals import Step


@dataclass
class Doublet(Signal):
    ampl: float = 1.0
    step_width: float = 1.0

    def __post_init__(self):
        up = self.ampl * Step(
            t_start=self.t_start, t_end=self.t_start + self.step_width
        )
        down = -self.ampl * Step(
            t_start=self.t_start + self.step_width,
            t_end=self.t_start + 2 * self.step_width,
        )

        self.doublet = up + down

    def _signal(self, t: float) -> float:
        return self.doublet(t)


@dataclass
class ThreeTwoOneOne(Signal):
    ampl: float = 1.0
    step_width: float = 1.0

    def __post_init__(self):
        up = self.ampl * Step(
            t_start=self.t_start, t_end=self.t_start + (3 + 2 + 1 + 1) * self.step_width
        )
        down1 = (
            -2.0
            * self.ampl
            * Step(
                t_start=self.t_start + 3 * self.step_width,
                t_end=self.t_start + 5 * self.step_width,
            )
        )
        down2 = (
            -2.0
            * self.ampl
            * Step(
                t_start=self.t_start + 6 * self.step_width,
                t_end=self.t_start + 7 * self.step_width,
            )
        )

        self.s_3211 = up + down1 + down2

    def _signal(self, t: float) -> float:
        return self.s_3211(t)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    tt = np.arange(-1.0, 21.0, 0.001)

    s3 = Doublet(t_start=0.0, t_end=20.0, ampl=10.0, step_width=2.0)
    sd = ThreeTwoOneOne(t_start=5.0, t_end=20.0, ampl=10.0, step_width=1.0)

    s_doub_ = [sd(t_i) for t_i in tt]
    s_3211_ = [s3(t_i) for t_i in tt]
    plt.plot(tt, s_doub_, "--")
    plt.plot(tt, s_3211_, "--")
    plt.grid()
    plt.show()
