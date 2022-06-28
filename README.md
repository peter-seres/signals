# Signals for control tasks

This is a small package to provide `Signal` objects that can be evaluated at time `t`.
The package only relies on `numpy` and implements arithmetic operations between `Signal` types, `int` and `float` primitives.

## Usage

### Add two signals together and evaluate at a single time-step

```py
from signals import Step, Sinusoid

step = Step(t_start=2.0, t_end=20.0)
sine = Sinusoid(t_start=0.0, t_end=10.0, freq=2.0)
reference = 5 * step + sine

# Reference at t = 5.0:
r_t = reference(t=5.0)
```

Every `Signal` object has `t_start` and a `t_end` arguments.
In most cases the default `t_start` and `t_end` are set to `0` and `+inf` respectively.
For any `t` not in  `[t_start, t_end]` the Signal object returns 0.

### Make a sequence of step signals and evaluate them on an array time-signals:

```py
import numpy as np
from signals import StepSequence

amplitudes = [2, 1, 0, -1, 2, 0]
times = [1, 2, 3, 4, 5, 7]
step_sequence = StepSequence(times=times, amplitudes=amplitudes)

# Time array:
t = np.arange(0, 10.0, 0.1)
s = step_sequence.eval_on(t=t)
```

## Installation

### 1. Manually using pip

```bash
pip install git+https://github.com/aerospace-rl/signals.git
```

### 2. In local virtual environment in edit mode

```bash
git clone https://github.com/aerospace-rl/signals.git`
cd signals
pip install -e .
```

### 3. Automatically using conda and environment.yml:

```yaml
dependencies:
  - pip
  - pip:
    - git+https://github.com/aerospace-rl/signals.git
```

## Defining custom signals

In order to make your own signal, make a class that derives from `Signal` and 
define the `_signal(self, t: float) -> float` method.

```py
from signals import Signal

class NegativeRamp(Signal):
    def _signal(self, t: float) -> float:
        return -t
```

## To-do / Feature list

- unit testing
- CI with unit tests and `black` formatting
