import pygame
from config import config
from resources import Resources
from src.util.window import Window
from src.util.input import Input
from src.World import World
from sys import exit

# IMPORTANT DEVELOPMENT CONSIDERATIONS

# Develop when needed
# Keep things simple
# Maintain modularity
# Dont render in update
# Keep input separated
# Use composition

class Game():
    def boot(self):
        pygame.init()
        print("Booting Up Rogueskill...")
        self.window = Window()
        self.inputManager = Input()

        self.window.bootWindow() # Btw the height and width are already in self so go to src/util/window to look for it
        self.window.setResizable()
        self.resources = Resources()
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.testWorld = World("New World",123,self.resources,self.inputManager,self.window)

    @staticmethod
    def getEvents():
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        mousePosition = pygame.mouse.get_pos()
        return mousePosition,running


    def update(self,mousePosition,dt):
        inputManager = self.inputManager
        inputManager.updateKeys()
        inputManager.updateMouse()

        self.window.isFullScreen()


        window = self.window
        testWorld = self.testWorld
        if window.fullScreenUpdate:
            testWorld.prepForFullScreen(
                window.playerWindowPosition,
                window.verticalRenderDistance,
                window.horizontalRenderDistance,
                window.windowDimensions
            )
            window.toggleUpdateFalse()

        testWorld.update(mousePosition,dt)

    def render(self,mousePosition):
        window = self.window
        window.clearWindow()
        self.testWorld.render(window,self.clock.get_fps(),mousePosition)
        pygame.display.flip()

    def run(self):
        frameRate = config.frameRate 
        clock = self.clock
        while self.running:
            dt = clock.tick(frameRate) / 1000.0
            mousePos,running = Game.getEvents()
            self.running = running
            self.update(mousePos,dt)
            self.render(mousePos)
            
    def quit(self): 
        pygame.quit()
        exit()