from config import config
import pygame
from math import floor
pygame.init()
pygame.font.init()


class Hud:
    def __init__(self,resources):
        self.font = resources.font
        self.invtileSize = 1/ config.tileSize # Store as inverse to optimise
        self.tileSize = config.tileSize
        self.chunkSize = config.chunkSize
        self.mousePos = None,None # Big number to trigger calculation
        self.lastPlayerBlockPos = None,None
        self.blockDestroyAtlas = resources.blockDestroyAtlas
        self.breakingAnimationSize = config.breakingAnimationSize,config.breakingAnimationSize

        self._prepDebug()
        self._preppointer(resources.pointerTexture)
        #self._prepBlockOutline(resources.blockOutline)
    def _prepDebug(self):
        self.lineSpacing = 20
        self.box = pygame.Surface((800,110))
        self.box.fill((255,255,255))

    def _preppointer(self,crosshair):
        pointer32x32 = pygame.transform.scale(crosshair, (50,50))
        hotspot = (5,5)  # Middle as the hotspot
        self.pointer = pygame.cursors.Cursor(hotspot, pointer32x32)
        pygame.mouse.set_cursor(self.pointer)

    # def _prepBlockOutline(self,outlineTexture):
    #     self.outline = outlineTexture



    def displayDebug(self,window,fps,player):
        bx,by = player.playerBlockX,player.playerBlockY
        cx,cy = player.playerChunkX,player.playerChunkY

        debugLines = [
            f"FPS: {round(fps)}",
            f"Player Block X: {bx:.2f}",
            f"Player Block Y: {by:.2f}", # Know that rendered Position is not the same as the internal top left coordinate system
            f"Chunk Block X: {floor(cx+0.5):.2f}",
            f"Chunk Block Y: {floor(cy+0.5):.2f}"
        ]
        window.blit(self.box,(0,0))
        for index,line in enumerate(debugLines):
            text = self.font.render(line,True,(0,0,0))
            window.blit(text,(0,index*self.lineSpacing))


    def _getMousePos(self,playerWindowPosition,playerBlockX, playerBlockY,mousePos):
        chunkSize = self.chunkSize
        invtileSize = self.invtileSize
        mx,my = mousePos
        pwx,pwy = playerWindowPosition
        dx = (pwx - mx) * invtileSize
        dy = (pwy - my) * invtileSize

        # Decimal global block position
        self.mouseBlockX = mouseBlockX = playerBlockX - dx
        self.mouseBlockY = mouseBlockY = playerBlockY - dy
        self.mousePos = mousePos

        # Chunk-relative and chunk coordinates based on rounded block
        intBlockX = floor(mouseBlockX + 8) 
        intBlockY = floor(mouseBlockY + 8)
        mouseInChunkX = intBlockX % chunkSize
        mouseInChunkY = intBlockY % chunkSize
        mouseChunkX = intBlockX // chunkSize
        mouseChunkY = intBlockY // chunkSize
        self.lastPlayerBlockPos = (playerBlockX,playerBlockY)
        self.mousePositionalData = mouseInChunkX, mouseInChunkY, mouseChunkX, mouseChunkY

        return mouseInChunkX, mouseInChunkY, mouseChunkX, mouseChunkY
    
    def _isCached(self,mousePos, playerBlockX, playerBlockY):
        return mousePos == self.mousePos and (playerBlockX,playerBlockY) == self.lastPlayerBlockPos


    def getBlockMouseTouching(self, playerWindowPosition,mousePos, playerBlockX, playerBlockY):

        if self._isCached(mousePos,playerBlockX,playerBlockY):
            return self.mousePositionalData
        else:
            return self._getMousePos(playerWindowPosition,playerBlockX,playerBlockY,mousePos)
    
    def renderBlockBreakingAnimation(self,screen,blockDestroyStage,destroyX,destroyY):
        screen.blit(self.blockDestroyAtlas.getTexture(blockDestroyStage,self.breakingAnimationSize),(destroyX,destroyY))

    # def renderBlockOutline(self, window,mousePos):
    #     bx, by = self.mouseBlockX, self.mouseBlockY
    #     mx, my = mousePos
    #     tileSize = self.tileSize

    #     # Adjust screen position based on sub-block decimal offset
    #     offsetX = (floor(bx) - bx) * tileSize
    #     offsetY = (floor(by) - by) * tileSize
    #     renderPosX = mx + offsetX
    #     renderPosY = my + offsetY
    #     window.blit(self.outline, (renderPosX,renderPosY))





