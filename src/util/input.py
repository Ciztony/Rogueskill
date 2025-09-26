import pygame

class Input:
    def __init__(self):
        self.boardKeys = {
        "Up": pygame.K_UP,
        "Down": pygame.K_DOWN,
        "Left": pygame.K_LEFT,
        "Right": pygame.K_RIGHT
    }
        self.mouseKeys = {
            "Place":2,
            "Break":0
        }

        self.boardKeysPressed = []
        self.mouseKeysPressed = []

    def updateKeys(self):
        self.boardKeysPressed = pygame.key.get_pressed()
       
        
    def updateMouse(self):
   
        self.mousePosition = pygame.mouse.get_pos()
        self.mouseKeysPressed = pygame.mouse.get_pressed()
        #print("Mouse keys pressed",self.mouseKeysPressed)

    def getMouseClickPressed(self,action):
        mouseKeysPressed = self.mouseKeysPressed
        clickCode = self.mouseKeys[action]
        pressed = mouseKeysPressed[clickCode]
        return pressed

    def getKeyPressed(self, action):
        keysPressed = self.boardKeysPressed
        keyCode = self.boardKeys[action]
        pressed = keysPressed[keyCode]
        return pressed



