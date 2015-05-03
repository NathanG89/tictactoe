import pygame

white = 204, 204, 204
black = 54, 54, 54 

pygame.font.init()
font = pygame.font.Font('lato.ttf', 32)

"""Button class.  

~Nate

Recent update made by James: 4/29/15"""

class Button(pygame.sprite.Sprite):
    def __init__(self, pos,offset=(0,0), text="", action=None, args=None):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.image = font.render(text, True, white, black)
        x1, y1 = pos
        x, y = offset
        self.rect = self.image.get_rect().move((x1 + x, y1 + y))
        self.action = self.original_action = action
        self.args = args
        
    @property
    def enabled(self):
        return self.action
    
    @enabled.setter
    def enabled(self, boolean):
        if boolean:
            self.action = self.original_action
        else:
            self.action = lambda: None


class Menu(object):
    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.active_button = None

    def draw(self, surface):
        self.buttons.draw(surface)

    def action(self):
        if self.active_button.args == None:
            self.active_button.action()
        else:
            self.active_button.action(*self.active_button.args)
        self.active_button = None

    def check_clicked(self, pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos) and button.enabled:
                self.active_button = button
                return True

class Messenger(pygame.sprite.Sprite):
    def __init__(self, msg=""):
        pygame.sprite.Sprite.__init__(self)
        self.__message = msg
        self.__image = None
        self.rect = None
        self.offset = 0, 0

    def draw(self, surface):
        self.rect.topleft = self.offset
        surface.blit(self.image, self.rect)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, img):
        self.rect = img.get_rect().move(self.offset)
        self.__image = img

    @property
    def message():
        return self.__message

    @message.setter
    def message(self, msg):
        self.image = font.render(msg, True, black, white)
