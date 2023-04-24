from test_system import pretty_input


def test_0():
    assert pretty_input("""1
2""") == """2"""

def test_1():
    assert pretty_input("""3
4""") == """12"""

def test_2():
    assert pretty_input("""3
0""") == """0"""

def test_3():
    assert pretty_input("""1
abcd""") == """ValueError"""