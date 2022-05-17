# Signals for control tasks

This is a small package to provide Signal objects that can be evaluated at time `t`.
The package only relies on `numpy` and implements arithmetic operations between `Signal` types, `int` and `float` primitives.

## Usage

```py
from signals import Step, Sinusoid

s = Step(t_start=2.0, t_end=20.0)
sine = Sinusoid(t_start=0.0, t_end=10.0, freq=2.0)
reference = 5 * s + sine

# Reference at t = 5.0:
r_t = reference(t=5.0)
```

## To-do list:

- add implementation for +=, -=, *= and /= operators
- add more commonly used signals
