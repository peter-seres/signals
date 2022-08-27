import pytest
import signals
import numpy as np


def test_const():
    c = signals.Const(value=5.0)

    # Const has to give the same value for any query:
    assert c(t=-500.0) == pytest.approx(5.0)
    assert c(t=4.0) == pytest.approx(5.0)
    assert c(t=2000.0) == pytest.approx(5.0)


def test_const_with_limits():
    c = signals.Const(value=5.0, t_start=3.0, t_end=10.0)

    # Before the signal starts
    assert c(t=-5.0) == pytest.approx(0.0)

    # When the signal is active
    assert c(t=4.0) == pytest.approx(5.0)

    # After the signal ends
    assert c(t=20.0) == pytest.approx(0.0)


def test_const_addition():
    c1 = signals.Const(value=2.0)
    c2 = signals.Const(value=3.0)

    # Make a sum of signals
    c = c1 + c2
    assert c(t=100.0) == pytest.approx(5.0)

    # Make a sum with a float
    c = c1 + 4.0
    assert c(t=100.0) == pytest.approx(6.0)

    # Make a right-handed sum with an int
    c = 4 + c1
    assert c(t=100.0) == pytest.approx(6.0)

    # Make a sum with a string
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        c = c1 + "a string"
        c(t=100)


def test_const_subtraction():
    c1 = signals.Const(value=2.0)
    c2 = signals.Const(value=3.0)

    # Make a sum signal
    c = c1 - c2
    assert c(t=100.0) == pytest.approx(-1.0)

    # Make a sum with a float
    c = c1 - 4.0
    assert c(t=100.0) == pytest.approx(-2.0)

    # Make a right-handed sum with an int
    c = 4 - c1
    assert c(t=100.0) == pytest.approx(2.0)

    # Make a sum with a string
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        c = c1 - "a string"
        c(t=100)


def test_const_multiplication():
    c1 = signals.Const(value=2.0)
    c2 = signals.Const(value=3.0)

    # Make a sum signal
    c = c1 * c2
    assert c(t=100.0) == pytest.approx(6.0)

    # Make a sum with a float
    c = c1 * 4.0
    assert c(t=100.0) == pytest.approx(8.0)

    # Make a right-handed sum with an int
    c = 4 * c1
    assert c(t=100.0) == pytest.approx(8.0)

    # Make a sum with a string
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        c = c1 * "a string"
        c(t=100)


def test_const_division():
    c1 = signals.Const(value=2.0)
    c2 = signals.Const(value=3.0)

    # Make a sum signal
    c = c1 / c2
    assert c(t=100.0) == pytest.approx(2.0 / 3.0)

    # Make a sum with a float
    c = c1 / 4.0
    assert c(t=100.0) == pytest.approx(0.5)

    # Make a right-handed sum with an int
    c = 4 / c1
    assert c(t=100.0) == pytest.approx(2.0)

    # Make a sum with a string
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        c = c1 / "a string"
        c(t=100)


def test_eval_on():
    t1 = [0, 5.0, 10.0]
    t2 = tuple(t1)
    t3 = np.array(t1)

    c = signals.Const(value=2.0, t_start=2.5, t_end=7.5)

    res1 = c.eval_on(t1)
    res2 = c.eval_on(t2)
    res3 = c.eval_on(t3)

    assert res1 == pytest.approx([0.0, 2.0, 0.0])
    assert res2 == pytest.approx([0.0, 2.0, 0.0])
    assert res3 == pytest.approx([0.0, 2.0, 0.0])


def test_implementation():

    # noinspection PyAbstractClass
    class CustomSignal(signals.Signal):
        pass

    # Custom signals must implement a _signal() method.
    with pytest.raises(TypeError):
        CustomSignal()
