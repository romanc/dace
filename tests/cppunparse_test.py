# Copyright 2019-2021 ETH Zurich and the DaCe authors. All rights reserved.
from dace.codegen import cppunparse


def _test_py2cpp(func, expected_string):
    result = cppunparse.py2cpp(func)
    assert result == expected_string


def _test_pyexpr2cpp(func, expected_string):
    result = cppunparse.pyexpr2cpp(func)
    assert result == expected_string


def gfunc(woo):
    i = 0
    result = 0
    while i < woo and i > 0:
        for j in range(i):
            result += (2 // 1)**j
    return result


def test():
    _test_py2cpp("""def notype(a, b):
    a = a + 5
    c = a + b
    return c*b
""", """auto notype(auto a, auto b) {
    a = (a + 5);
    auto c = (a + b);
    return (c * b);
}""")

    _test_py2cpp("""def typed(a: int, b: float) -> float:
    c = a + b
    return c*b
""", """float typed(int a, float b) {
    auto c = (a + b);
    return (c * b);
}""")

    # Ternary operators, strings
    _test_py2cpp("""printf('%f\\n', a if b else c);""", """printf("%f\\n", (b ? a : c));""")

    # Global functions, operators
    _test_py2cpp(
        gfunc, """auto gfunc(auto woo) {
    auto i = 0;
    auto result = 0;
    while (((i < woo) && (i > 0))) {
        for (auto j : range(i)) {
            result += dace::math::pow(dace::math::ifloor(2 / 1), j);
        }
    }
    return result;
}""")

    def lfunc():
        exit(1 >> 3)

    # Local functions
    _test_py2cpp(lfunc, """auto lfunc() {
    exit((1 >> 3));
}""")

    # void return value
    if six.PY3:
        _test_py2cpp("""
def lfunc() -> None:
    exit(1 >> 3)
""", """void lfunc() {
    exit((1 >> 3));
}""")

    # Local variable tracking
    _test_py2cpp('l = 1 + a; l = l + 8;', """auto l = (1 + a);
l = (l + 8);""")

    # Operations (augmented assignment)
    _test_py2cpp('l *= 3; l //= 8', """l *= 3;
l = dace::math::ifloor(l / 8);""")

    _test_pyexpr2cpp('a << 3', '(a << 3)')

    # Array assignment
    _test_py2cpp('A[i] = b[j]', """A[i] = b[j];""")

    # Named constants
    _test_py2cpp('''if x is not None:
    y = True if x else False
    ''', '''if ((x != nullptr)) {
    auto y = (x ? true : false);
}''')


def test_annotated_definition():
    _test_py2cpp('''a: dace.float32
if something:
    a = 5
    ''', '''dace::float32 a;
if (something) {
    a = 5;
}''')


def test_integer_power() -> None:
    python = "tmp: dace.float32\ntmp_2 = tmp ** 2"
    expected = "dace::float32 tmp;\nauto tmp_2 = (dace::math::ipow(tmp, 2));"
    success = _test_py2cpp(python, expected)
    assert success


if __name__ == "__main__":
    test()
    test_annotated_definition()
    test_integer_power()
