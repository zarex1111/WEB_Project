from test_system import pretty_input


def test_0():
    assert pretty_input("""3
4""") == """12"""

def test_1():
    assert pretty_input("""1
0""") == """0"""