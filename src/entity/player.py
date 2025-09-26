import pygame
from config import config
from src.util.atlas import Atlas
from time import time

class Player:
    def __init__(self,playerWindowPosition,inputManager,resources):
        self.velocity = config.playerVelocity / config.tileSize # Note that velocity in game is pixels not blocks
        self.chunkSize = config.chunkSize

        self.inputManager = inputManager
        self.blockXChange,self.blockYChange = 0,0
        self.playerChunkX,self.playerChunkY = 0,0
        self.playerBlockX,self.playerBlockY = 0,0  
        self.playerWindowPosition = playerWindowPosition

        playerTileSize = config.playerTileSize
        self.playerRect = pygame.Rect(0,0,config.playerTileSize,config.playerTileSize)
        self.playerRect.center = playerWindowPosition
        self.playerTileSize = playerTileSize
        self.surfaceUpdate = True
        self.invChunkSize = 1/ self.chunkSize
        self.playerAtlas = Atlas(resources.playerMetDat,resources.playerAtlas)
        self.animationTimer = time() # Last time a frame changed
        self.animationSpeed = config.playerAnimationSpeed # Amount of time between frames of animation
        self.totalAnimationCycle = resources.playerAnimationCycle # Length of the number of sprites for each direction of animation
        self.previousFrameDirection = None
        self.direction = "down"

    def handleMovement(self,dt): # Includes normalization of diagonal movement
        im = self.inputManager
        velocity = self.velocity
        dx = im.getKeyPressed("Right") - im.getKeyPressed("Left")
        dy = im.getKeyPressed("Down") - im.getKeyPressed("Up")
        moving = False
        # Y axis has priority in direction, thus if player moving upand left, texture would be up, and when only left, than left
        if dy:
            self.direction = "up" if dy == -1 else "down"
            moving = True
        if dx:
            self.direction = "left" if dx == -1 else "right"
            moving = True
        self.state = "walk" if moving else "idle"

        vec = pygame.Vector2(dx, dy)
        if vec.length_squared() > 0:
            vec = vec.normalize()

        self.blockXChange += vec.x * velocity * dt
        self.blockYChange += vec.y * velocity * dt
    
    def updateAnimation(self):
        # If same direction, continue with animation
        if self.state == "idle":
            animationId = f"idle_{self.direction}"
            return animationId

        if self.direction == self.previousFrameDirection:
            now = time()
            if now-self.animationTimer > self.animationSpeed:
                self.animationTimer = now
                self.frameIndex = (self.frameIndex + 1) % self.totalAnimationCycle
        else:
            # Reset
            self.frameIndex = 0

        self.previousFrameDirection = self.direction
        animationId = f"walk_{self.direction}_{self.frameIndex}"
        return animationId
        

    def updatePosition(self,dt):
        self.blockXChange,self.blockYChange = 0,0
        self.handleMovement(dt)
        if self.blockXChange == 0 and self.blockYChange == 0:
            self.surfaceUpdate = False
            return None

        bx,by = self.blockXChange,self.blockYChange
        invChunk = self.invChunkSize  # Inverse of chunk Size is more optimised than division

        chunkXChange,chunkYChange = bx * invChunk, by * invChunk

        self.playerBlockX += bx
        self.playerBlockY += by
        self.playerChunkX += chunkXChange
        self.playerChunkY += chunkYChange
       
        self.surfaceUpdate = True
        return chunkXChange, chunkYChange

    def updateWindowPosition(self,playerWindowPosition):
        self.playerWindowPosition = playerWindowPosition
        self.playerRect.center = playerWindowPosition
    
    def toggleUpdateFalse(self):
        self.surfaceUpdate = False

    def getPlayerTexture(self):
        animationId = self.updateAnimation()
        playerTileSize = self.playerTileSize
        texture = self.playerAtlas.getTexture(animationId,(playerTileSize,playerTileSize))
        return (texture,self.playerRect.topleft,(0,0,0))

