from config import config
import pygame

class ChunkRenderer:
    def __init__(self,atlas,font):
        self.atlas = atlas
        self.chunkPixels = config.chunkPixels
        self.tileSize = config.tileSize
        self.font = font
        self.chunkBaseSurface = pygame.Surface((self.chunkPixels,self.chunkPixels))
    
    # Blits the current chunk surface onto the window
    def blitChunkSurfaceOntoWindow(self,player,chunkCoordinate,chunkTexture,window):
        # Below is the formula for player chunk rendering
        px, py = player.playerWindowPosition
        cx, cy = chunkCoordinate
        chunkPixels = self.chunkPixels

        x = px + (cx - 0.5 - player.playerChunkX) * chunkPixels
        y = py + (cy - 0.5 - player.playerChunkY) * chunkPixels

        chunkRenderPosition = (x, y)
        #fontText = self.font.render(f'{cx},{cy}',True,(0,0,0))
        #chunkTexture.blit(fontText,(0,0))
        window.blit(chunkTexture, chunkRenderPosition)
        return chunkRenderPosition

    # Render the chunk data onto the chunk surface
    def renderChunkOntoChunkSurface(self,chunkCacheSurface,staticTiles):
        chunkCacheSurface.fill((0,0,0))
        tileSize = self.tileSize
        atlas = self.atlas

        for (coordinate,layers) in staticTiles.items():
            for tileId in layers:
                
                texture = atlas.getTexture(tileId,(tileSize,tileSize))
                x,y = coordinate
                position = (x*tileSize,y*tileSize)
                chunkCacheSurface.blit(texture,position)
        #pygame.draw.rect(chunkCacheSurface,(0,0,0),(0,0,config.chunkPixels,config.chunkPixels),width=1)

        
    

    # Wrapper function for rendering chunks
    def renderChunkSurface(self,chunkData):
        # Render chunk's surface
        newChunkSurface = self.chunkBaseSurface.copy()
        self.renderChunkOntoChunkSurface(newChunkSurface,chunkData)
        return newChunkSurface
