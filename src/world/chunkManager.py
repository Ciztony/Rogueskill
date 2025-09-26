from src.world._chunk import Chunk
from config import config
from src.world.generator import Generator
from src.world.chunkRenderer import ChunkRenderer
from src.world.structureManager import StructureManager
import pygame

class ChunkManager:
    def __init__(self,player,resources,seed):
        self.player = player
        self.chunkCache = dict() # Stores chunk Surfaces
        self.loadedChunks = set() # Stores coordinates of loaded chunks
        self.chunkObjects = pygame.sprite.Group() # Store chunk classes
        self.chunkObjectsReference = {} # Stores references for chunk objects to optimise be able to access by id
        self.structureManager = StructureManager(resources)
        self.generator = Generator(config.chunkSize,seed,self.structureManager)
        self.chunkRenderer = ChunkRenderer(resources.blockAtlas,resources.font)
    
    def generateSpawnChunks(self):
        self.generator.generateSpawnChunks(self.generateChunk)

    # Cache chunk
    def cacheChunk(self,coordinates,newChunkSurface):
        self.chunkCache[coordinates] = newChunkSurface
        self.loadedChunks.add(coordinates)

    # Generate a single chunk
    def generateChunk(self,coordinates):
        cx,cy = coordinates
        staticTiles,dynamicTiles = self.generator.requestChunk(cx,cy)
        newChunkSurface = self.chunkRenderer.renderChunkSurface(staticTiles)

        self.cacheChunk(coordinates,newChunkSurface)
        # Create chunk instance
        chunk = Chunk(list(coordinates),staticTiles,dynamicTiles) # Note that chunkData is actually just visibleTiles
        self.chunkObjectsReference[coordinates] = chunk # Add reference of chunk for easy access
        self.chunkObjects.add(chunk)

    # Move chunks during window change
    def applyWindowSizeChangeToChunks(self,nx,ny):
        for chunk in self.chunkObjectsReference.values():
            chunk.applyRenderDistanceUpdate(nx,ny)

    # Clip chunks to be within frustum
    def moveChunksWithinFrustum(self,chunkChange):
        chunkXChange,chunkYChange = chunkChange
        loadedChunks = set()
        player = self.player
        self.chunkObjects.update(chunkXChange,chunkYChange,loadedChunks,player.playerChunkX,player.playerChunkY)
        self.loadedChunks = loadedChunks

    
    # Render all chunks in the loaded chunks array
    def renderLoadedChunks(self,window):
        getChunk = self.chunkCache.get # get is more optimised
        blit = self.chunkRenderer.blitChunkSurfaceOntoWindow
        player = self.player
        loadedChunks = self.loadedChunks
        coordinates = {}
        for chunk in loadedChunks:
            chunkSurface = getChunk(chunk)
            if chunkSurface is None:
                print("Unrendered at:", chunk)
                continue
            coordinates[chunk] = blit(player,chunk, chunkSurface, window)
        return loadedChunks,coordinates


        




          


