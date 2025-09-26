import pygame
from config import config

class Window:
    def __init__(self):
        self.chunkPixels = config.chunkPixels
        self.windowWidth,self.windowHeight = config.windowWidth,config.windowHeight
        self.fullScreenUpdate = False
    

    def _addChunkRenderBuffer(self,rendDis):
        total = int(rendDis * 2 + 1)
        return total | 1

    def _setScreenAttributes(self,windowWidth,windowHeight):
        chunkPixels = self.chunkPixels
        buffer = self._addChunkRenderBuffer
        self.playerWindowPosition = windowWidth // 2, windowHeight // 2
        
        self.verticalRenderDistance = buffer(((windowHeight / chunkPixels) - 1) // 2 + 1) # Calculate number of chunks in viewport
        self.horizontalRenderDistance = buffer(((windowWidth  / chunkPixels)- 1) // 2 + 1)
        self.windowDimensions = windowWidth,windowHeight

    def bootWindow(self):
        try:
            windowWidth,windowHeight = self.windowWidth,self.windowHeight
            self.window = pygame.display.set_mode((windowWidth,windowHeight))

            self._setScreenAttributes(windowWidth,windowHeight)

            pygame.display.set_caption("Rogueskill")
        except Exception as e:
            print(f"Window Booting error: {e}")
    
    def setResizable(self):
        try:
            self.window = pygame.display.set_mode((self.windowWidth,self.windowHeight),pygame.RESIZABLE,pygame.NOFRAME)
        except Exception as e:
            print(f"Resize screen error: {e}")

    def isFullScreen(self):
        windowWidth,windowHeight = self.window.get_size()
        if self.windowDimensions != (windowWidth,windowHeight): # Means that it is getting full screened

            self._setScreenAttributes(windowWidth,windowHeight)
            self.fullScreenUpdate = True
            return
        self.fullScreenUpdate = False
    
    def toggleUpdateFalse(self):
        self.fullScreenUpdate = False
    
    def blit(self,surface,position):
        self.window.blit(surface,position)
    
    def fill(self,colour):
        self.window.fill(colour)
        
    def clearWindow(self):
        self.fill((0,0,0))
