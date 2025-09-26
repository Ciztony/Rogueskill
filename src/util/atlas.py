import pygame

class Atlas:
    def __init__(self,metDat,atlasTexture):
        # Reuse textures
        self.textureReuse = {}
        # Renders texture first, so only scaling needed
        self.preRenderedTextures = {}

        self.atlasTexture = atlasTexture
        textureMetaData = metDat
        tileSize = textureMetaData["atlasTileSize"]

        for id,data in textureMetaData["textureMeta"].items():
            isFlipped = isinstance(data,str)
            if not isFlipped:
                subSurfaceRect = data["subSurfaceRect"]
                x, y, width, height = subSurfaceRect # Unpacking can increase processing times
                subSurface = pygame.Rect(x * tileSize, y * tileSize, width, height)  
                texture = atlasTexture.subsurface(subSurface)
            else:
                textureToFlipFromId = data.removeprefix("flip.")
                texture = pygame.transform.flip(self.preRenderedTextures[textureToFlipFromId],True,False)
            
            self.preRenderedTextures[id] = texture


    def getTexture(self,id,dimensions):
        key = (id, dimensions)
        textureReuse = self.textureReuse
        if key in textureReuse:
            return textureReuse[key]

        texture = pygame.transform.scale(self.preRenderedTextures[id].copy(),dimensions)
        textureReuse[key] = texture
        return texture
        