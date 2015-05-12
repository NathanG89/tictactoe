from nose.tools import *
from menu import *
from graphics import *

buttons = [('Test 1', btn_test1),
           ('Test 2', btn_test2, [1, 'test']),
           ('Test 3', btn_test3, 'testing')]
menu = create_menu(buttons, offset=(0,0))

def btn_test1():
    return True

def btn_test2(num, str):
    values = (num, str)
    return values

def btn_test3(str):
    return str

def test_init():
    for button in menu:
        assert not button.text == ''
        
    pass

