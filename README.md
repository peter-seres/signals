# Signals for control tasks

This is a small package to provide `Signal` objects that can be evaluated at time `t`.
The package only relies on `numpy` and implements arithmetic operations between `Signal` types, `int` and `float` primitives.

## Usage

```py
from signals import Step, Sinusoid

step = Step(t_start=2.0, t_end=20.0)
sine = Sinusoid(t_start=0.0, t_end=10.0, freq=2.0)
reference = 5 * step + sine

# Reference at t = 5.0:
r_t = reference(t=5.0)
```

Every `Signal` object has `t_start` and a `t_end` arguments, default is set to `-inf` and `+inf` respectively.
For any `t` not in  `[t_start, t_end]` the Signal returns 0.

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

