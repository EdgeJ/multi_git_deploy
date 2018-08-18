"""
Common helper code for unit tests
"""


def test_print(message):
    """
    Print test messages to stdout
    """
    print('\033[95m[TEST] ==> {message}\033[0m'.format(message=message))
