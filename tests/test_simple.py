import pytest
import signals


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
