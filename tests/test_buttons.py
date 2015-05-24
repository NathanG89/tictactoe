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

def btn_2(*args):
    # num = args[0]
    # str = args[1]
    values = (args)
    print values
    return True

def btn_3(*args):
    print args
    return True

def btn_4(*args):
    print args
    return True

buttons = [('Test 1', btn_1, None),
           ('Test 2', btn_2, [1, 'test']),
           ('Test 3', btn_3, 'testing'),
           ('Test 4', btn_4, 'testing2')]
menu = create_menu(buttons, offset=(0,0))
WIDTH, HEIGHT = 640, 640

for button in menu.buttons:
    if button.text == 'Test 3':
        button.enabled = False
    
def test_init():
    for button in menu.buttons:
        assert not button.text == ''
        print button.text
        print button.rect.x
        print button.rect.y
        print button.rect.width
        print button.rect.height
        # print button.rect

def test_action():
    for button in menu.buttons:
        if not button.enabled:
            assert not button.action()
        else:
            button.action()
            
def test_clicked():
    print "button corner click"
    for button in menu:
        assert menu.check_clicked((button.rect.x,button.rect.y))
        assert menu.check_clicked((button.rect.x,button.rect.y+button.rect.height))
        assert menu.check_clicked((button.rect.x+button.rect.width,button.rect.y))
        assert menu.check_clicked((button.rect.x+button.rect.width,button.rect.y+button.rect.height))
    x = button.rect.x
    y = button.rect.y
    print "button click"
    for button in menu:
        while x < button.rect.x + button.rect.width:
            while y < button.rect.y + button.rect.height:
                assert menu.check_clicked((x,y))
                y+=1
            y = 0
            x+=1
    x = 0
    y = 0
    print "clicking everywhere else"
    for button in menu:
        while x < WIDTH:
            # if x == button.rect.x:
            #     x = button.rect.x + button.rect.width + 1
            while y < HEIGHT:
                if y == button.rect.y and x == button.rect.x:
                    y = button.rect.y + (button.rect.height*4) + 1
                assert not menu.check_clicked((x,y))
                y+=1
            y = 0
            x+=1
    for button in menu:
        
        
if __name__ == '__main__':
    test_init()
    test_action()
    test_clicked()
