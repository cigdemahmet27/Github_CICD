import pytest

from app.calculator import add, average, divide, multiply, subtract


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(4, 5) == 20


def test_divide():
    assert divide(10, 4) == 2.5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_average():
    assert average([1, 2, 3, 4]) == 2.5


def test_average_empty():
    with pytest.raises(ValueError):
        average([])
