from __future__ import annotations
from numpy import NINF, PINF
from abc import abstractmethod, ABC
from dataclasses import dataclass, field


class BaseSignal:
    def __add__(self, other: BaseSignal | float | int) -> BaseSignal:
        if isinstance(other, BaseSignal):
            return SumOfSignals(self, other)
        elif isinstance(other, (float, int)):
            return SumOfSignals(self, Const(value=other))
        else:
            raise TypeError(
                "Addition with Signal only support for [SignalOperations | float | int]. "
                f"Operand + was called for types: {type(self)} + {type(other)}"
            )

    def __radd__(self, other: BaseSignal | float | int) -> BaseSignal:
        return self + other

    def __mul__(self, other: BaseSignal | float | int) -> BaseSignal:
        if isinstance(other, BaseSignal):
            return ProductOfSignals(self, other)
        elif isinstance(other, (float, int)):
            return ProductOfSignals(self, Const(value=other))
        else:
            raise TypeError(
                f"Multiplication with Signal only support for [SignalOperations | float | int]. "
                f"Operand * was called for types: {type(self)} * {type(other)}"
            )

    def __rmul__(self, other: BaseSignal | float | int) -> BaseSignal:
        return self * other

    def __sub__(self, other: BaseSignal | float | int) -> BaseSignal:
        if isinstance(other, BaseSignal):
            return DifferenceOfSignals(self, other)
        elif isinstance(other, (float, int)):
            return DifferenceOfSignals(self, Const(value=other))
        else:
            raise TypeError(
                "Addition with Signal only support for [SignalOperations | float | int]. "
                f"Operand - was called for types: {type(self)} - {type(other)}"
            )

    def __rsub__(self, other: BaseSignal | float | int) -> BaseSignal:
        if isinstance(other, BaseSignal):
            return DifferenceOfSignals(other, self)
        elif isinstance(other, (float, int)):
            return DifferenceOfSignals(Const(value=other), self)
        else:
            raise TypeError(
                "Addition with Signal only support for [SignalOperations | float | int]. "
                f"Operand - was called for types: {type(other)} - {type(self)}"
            )

    def __truediv__(self, other: BaseSignal | float | int) -> BaseSignal:
        if isinstance(other, BaseSignal):
            return DivisionOfSignals(self, other)
        elif isinstance(other, (float, int)):
            return DivisionOfSignals(self, Const(value=other))
        else:
            raise TypeError(
                "Addition with Signal only support for [SignalOperations | float | int]. "
                f"Operand / was called for types: {type(self)} / {type(other)}"
            )

    def __rtruediv__(self, other: BaseSignal | float | int):
        if isinstance(other, BaseSignal):
            return DivisionOfSignals(other, self)
        elif isinstance(other, (float, int)):
            return DivisionOfSignals(Const(value=other), self)
        else:
            raise TypeError(
                "Addition with Signal only support for [SignalOperations | float | int]. "
                f"Operand / was called for types: {type(other)} / {type(self)}"
            )

    def __call__(self, t: float) -> float:
        raise NotImplementedError


@dataclass
class TwoSidedOperation(BaseSignal, ABC):
    lhs: BaseSignal | float | int
    rhs: BaseSignal | float | int


class SumOfSignals(TwoSidedOperation):
    def __call__(self, t: float) -> float:
        return self.lhs(t) + self.rhs(t)


class DifferenceOfSignals(TwoSidedOperation):
    def __call__(self, t: float) -> float:
        return self.lhs(t) - self.rhs(t)


class ProductOfSignals(TwoSidedOperation):
    def __call__(self, t: float) -> float:
        return self.lhs(t) * self.rhs(t)


class DivisionOfSignals(TwoSidedOperation):
    def __call__(self, t: float) -> float:
        return self.lhs(t) / self.rhs(t)


@dataclass
class Signal(BaseSignal, ABC):
    t_start: float = field(default=0.0, init=True)
    t_end: float = field(default=PINF, init=True)

    def __call__(self, t: float) -> float:
        if self.t_start <= t < self.t_end:
            return self._signal(t - self.t_start)
        else:
            return 0.0

    @abstractmethod
    def _signal(self, t: float) -> float:
        raise NotImplementedError


@dataclass
class Const(Signal):
    value: float = 0.0
    t_start: float = NINF

    def _signal(self, _: float) -> float:
        return self.value
