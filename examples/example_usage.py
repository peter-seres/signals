from signals import Step, Sinusoid, Exponential, Ramp


def main():

    # Signal example
    s = Sinusoid(t_start=2.0)
    e = Exponential(t_start=2.0, alpha=0.1)
    r = Ramp()
    k = Step(t_start=5.0, t_end=10.0)
    x = k + (s * 2 * e + 3 * r - 4 * s) / (2 * e)

    print(f"Signal value at 4 seconds is: {x(4.0):.3f}")


if __name__ == "__main__":
    main()
