import subprocess
from pprint import pprint
import subprocess as sp
from subprocess import PIPE
from time import sleep
from useful_tools import *
import os
import pytest
from flask import jsonify


def format_solution(code):
    code = [' ' * 4 + line for line in code.splitlines()]
    code.append('except Exception as exc:')
    code.append(' ' * 4 + 'print(exc.__class__.__name__)')
    code.insert(0, 'try:')
    code = '\n'.join(code)
    with open('users_solution.py', 'w') as f:
        f.write(code)


def get(data):
    process = sp.Popen("python users_solution.py", stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True, shell=True)
    result = process.communicate(str(data))
    process.kill()
    return result


def pretty_input(data):
    return get(data)[0].rstrip()


def create_test_machine(tests):
    with open('script.py', 'w') as file:
        file.write('from test_system import pretty_input\n')
        for test in tests:
            file.write(f'''\n\ndef test_{ tests.index(test) }():
    assert pretty_input("{ test[0] }") == "{ test[1] }"''')


def start_processing(code, tests):
    create_test_machine(tests)
    format_solution(code)
    process = subprocess.Popen('python -m pytest script.py', text=True, stdout=subprocess.PIPE)
    output, errors = process.communicate()
    mistakes = list(filter(lambda x: x.startswith('FAILED'), output.splitlines()))
    request = {'errors': []}
    test_number = len(tests)
    error_number = len(mistakes)
    accuracy = round(float(test_number - error_number) / test_number, 2) * 100
    request['accuracy'] = accuracy
    for err in mistakes:
        shorter = err[err.find('test_') + 5:]
        number = int(smart_split(shorter, ' ')[0])
        err_output = {
            'test_number': number + 1,
            'input': tests[number][0],
            'expected_output': tests[number][1],
            'received_output': pretty_input(tests[number][0])
        }
        request['errors'].append(err_output)
    return request
        
        


if __name__ == '__main__':
    code = '''name = input()
if 'n' in name:
    raise(ValueError)
print(f'You are { name }')'''
    start_processing(code, [('spli', 'You are split'), ('splin', 'ValueError'), ('oshibka', 'You are not oshibka')])