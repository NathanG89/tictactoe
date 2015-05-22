from nose.tools import *
from menu import *
#from graphics import *

def create_menu(buttons, offset=(0,0)):
    menu = Menu()
    for i, args in enumerate(buttons):
        b = Button((16,i*48),offset,*args)
        menu.buttons.add(b)
    return menu

def btn_1():
    return True

def btn_2(num, str):
    values = (num, str)
    return values

def btn_3(str):
    return str

def setup():
    buttons = [('Test 1', btn_1),
               ('Test 2', btn_2, [1, 'test']),
               ('Test 3', btn_3, 'testing')
               ('Test 4', btn_4, 'testing2')]
    menu = create_menu(buttons, offset=(0,0))
    menu.buttons[3].enabled = False
    
def test_init():
    for button in menu:
        assert not button.text == ''
        print button.text
        assert not button.x1 == 0 and not button.y1 == 0
        print button.x1, button.y1
        assert button.x == 0 and button.y == 0
        print button.x, button.y
        if not button.enabled:
            assert button.action() == None
        else:
            assert not button.action() == None
        

