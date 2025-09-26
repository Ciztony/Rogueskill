import pygame
from math import floor
from config import config
# spawn relative coordinate is the chunk pos relative to spawn but player relative coordinate coordinate is the chunk pos relative to the chunk the player is currently in
# Chunk class
# chunks will only handle chunk updates not rendering updates
class Chunk(pygame.sprite.Sprite):
    def __init__(self,startingRelativeChunk,staticTiles,dynamicTiles):
        super().__init__()
        self.vertRendDis = config.verticalRenderDistance
        self.horzRendDis = config.horizontalRenderDistance

        # Data
        self.spawnRelativeChunk = startingRelativeChunk
        self.staticTiles = staticTiles
        self.dynamicTiles = dynamicTiles      

    def _updateSpawnRelativeChunk(self,chunkXChange,chunkYChange):
        self.spawnRelativeChunk[0] = round(self.spawnRelativeChunk[0] + chunkXChange)
        self.spawnRelativeChunk[1] = round(self.spawnRelativeChunk[1] + chunkYChange)


    # Update so the chunk matches the current one
    def update(self,chunkXChange,chunkYChange,loadedChunks,playerChunkX,playerChunkY):
        self._updateSpawnRelativeChunk(chunkXChange,chunkYChange)
        sx,sy = self.spawnRelativeChunk
        px,py = floor(playerChunkX+0.5),floor(playerChunkY+0.5)

        if abs(px-sx) <= self.horzRendDis and abs(py-sy) <= self.vertRendDis: # Keep in camera's frustum
            loadedChunks.add((sx,sy))

    def applyRenderDistanceUpdate(self,newVert,newHorz):
        self.vertRendDis = newVert
        self.horzRendDis = newHorz
            

   


       






    