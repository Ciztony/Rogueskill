from config import config

# Handles top tiles that must be dynamically rendered

class DynamicLayereringManager:
    def __init__(self,structureManager,chunkObjectReferences):
        self.structureManager = structureManager
        self.tileSize = config.tileSize
        self.chunkPixels = config.chunkPixels
        self.chunkObjectReferences = chunkObjectReferences      

    @staticmethod
    def withinViewport(layeringData, windowDimensions):
        return abs(layeringData[1][0]) < windowDimensions[0] or abs(layeringData[1][1]) < windowDimensions[1]

    def generateDynamicTextureDrawStack(self,loadedChunks,coordinates,windowDimensions):
        drawStack  = []
        structureTextures = self.structureManager.structureTextures
        tileSize = self.tileSize
        chunkObjectReferences = self.chunkObjectReferences
        withinViewPort = DynamicLayereringManager.withinViewport

        for chunkCoord in loadedChunks:
            dynamicTiles = chunkObjectReferences[chunkCoord].dynamicTiles
            screenX,screenY = coordinates[chunkCoord]
            for coord,structureId in dynamicTiles.items():
                texture,offset = structureTextures[structureId]
                x,y = coord
                rx,ry = screenX + tileSize * x,screenY + tileSize * y
                structureData = (texture,(rx,ry),offset)
                if withinViewPort(structureData,windowDimensions):
                    drawStack.append(structureData) # Adds to call stack, according to its screen position, which is acquired from coordinates
        
        self.drawStack = drawStack
    
    def addPlayerToDrawStack(self,playerMetadata,windowDimensions):
        if DynamicLayereringManager.withinViewport(playerMetadata,windowDimensions):
            self.drawStack.append(playerMetadata)
  
    def renderDynamicTextureDrawStack(self,window):
        # Sort by y-position
        drawStack = self.drawStack
        tileSize = self.tileSize
        drawStack.sort(key=lambda texture:texture[1][1]+texture[2][1]*tileSize) # Sort by the yposition - offset to properly set its layering

        for surface,coord,offset in drawStack:
            x,y = coord
            renderingXOffset,_,renderingYOffset = offset # Layering Y offset sets how layering should be done, while rendering x and y are the physical rendering offsets
            window.blit(surface,(x+renderingXOffset*tileSize,y+renderingYOffset*tileSize))