import numpy as np
from signals import StepSequence, SmoothedStepSequence


def main():
    amplitudes = [2, 1, 0, -1, 2, 0]
    times = [1, 2, 3, 4, 5, 7]
    step_sequence = StepSequence(times=times, amplitudes=amplitudes)
    smoothed_step_sequence = SmoothedStepSequence(
        times=times, amplitudes=amplitudes, smooth_width=0.4
    )

    # Time array:
    t = np.arange(0, 10.0, 0.01)
    s1 = step_sequence.eval_on(t=t)
    s2 = smoothed_step_sequence.eval_on(t=t)

    import matplotlib.pyplot as plt

    plt.plot(t, s1, "--")
    plt.plot(t, s2)
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel("Signal(t)")
    plt.show()


if __name__ == "__main__":
    main()
