import matplotlib.pyplot as plt
from signals import RandomizedStepSequence, RandomizedCosineStepSequence
import numpy as np

def main():

    T = 30.0

    s = RandomizedStepSequence(
        t_max=T,
        ampl_max=10,
        block_width=5,
        start_with_zero=True,
        vary_timings=0.2,
        n_levels=20
    )
    c = RandomizedCosineStepSequence(
        t_max=T,
        ampl_max=10,
        block_width=5,
        start_with_zero=True,
        vary_timings=0.2,
        smooth_width=0.5,
        n_levels=20
    )

    tt = np.arange(0, T, 0.001)
    ss = []
    cc = []

    # Evaluate the signals on the time range and store the data
    for t_i in tt:
        ss.append(s(t_i))
        cc.append(c(t_i))

    plt.plot(tt, ss, tt, cc)
    plt.show()


if __name__ == '__main__':
    main()
