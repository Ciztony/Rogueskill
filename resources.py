from src.util.file import loadFile
from config import config
from src.util.atlas import Atlas
from pathlib import Path
import pygame

class Resources:
    def __init__(self):
        try:
            self.loadAtlases()
            self.loadSingularTextures()
            self.loadStructures()
            self.loadFonts()
            self.loadHardCodedAttributes()
        except Exception as e:
            print(f"Resource reading error: {e}")


    def loadAtlases(self):
        self.blocksMetDat = loadFile("assets/data/blocks/blocks.dat","pickle")
        setattr(config,"scaleInTileSize",config.tileSize/self.blocksMetDat["atlasTileSize"])
        self.blockAtlasTexture = pygame.image.load("assets/textures/blocks/block_atlas.png").convert_alpha()
        self.blockAtlas = Atlas(self.blocksMetDat,self.blockAtlasTexture)

        self.playerMetDat = loadFile("assets/data/entities/player.json","json")
        self.playerAtlas = pygame.image.load("assets/textures/entities/player.png").convert_alpha()
        self.playerAnimationCycle = self.playerMetDat["totalAnimationCycle"]

        self.blockDestroyAtlasTexture = pygame.image.load("assets/textures/hud/block_destroy_atlas.png").convert_alpha()
        self.blockDestroyMetDat = loadFile("assets/data/hud/block_destroy.dat","pickle")
        self.blockDestroyAtlas = Atlas(self.blockDestroyMetDat,self.blockDestroyAtlasTexture)

    def loadSingularTextures(self):
        self.logo = pygame.image.load("assets/textures/rogueskillLogo.png").convert_alpha()
        self.pointerTexture = pygame.image.load("assets/textures/hud/pointer.png").convert_alpha()
        #self.blockOutline = pygame.image.load("assets/textures/hud/block_outline.png").convert_alpha()
        #self.blockOutline = pygame.transform.scale(self.blockOutline,(config.tileSize,config.tileSize))
        pygame.display.set_icon(self.logo)

    def loadFonts(self):
        self.font = pygame.font.Font("assets/fonts/font1.ttf",14)

    def loadHardCodedAttributes(self):
        self.chunkPixels = config.tileSize * config.chunkSize

    def loadStructures(self):
        self.structureData = {}
        self.structureTextures = {}
        self.updateTimes = {} # Breaking and placing time of structures
        scaleBy = config.scaleInTileSize
        rootDirectory = "assets/textures/structures/"
        structureData = "assets/data/structures"
        for index, structure in enumerate(list(Path(structureData).iterdir())):
            structureName = structure.stem
            structureJson = loadFile(structure.as_posix(), "json")
            #Load texture filepath
            textureFilePath = rootDirectory + structureName + ".png"
            #print(textureFilePath)

            texture = pygame.image.load(textureFilePath).convert_alpha()

            # Optional: resize the texture based on metadata
            renderedSize = structureJson["renderedSize"]
            if renderedSize != "default":
                texture = pygame.transform.scale(texture, renderedSize)

            # Apply an additional scaling factor (e.g., global scale for the game world)
            texture = pygame.transform.scale_by(texture, scaleBy)
            #print(texture.get_size())  

            probabilityOfGeneration = structureJson["probabilityOfGeneration"]
            # Store the processed data in a dictionary:
            # Key = index, Value = tuple of (spawnRate and probability array)
            # Probability array format: [chance not to generate, chance to generate]
            self.structureData[index] = (
                structureJson["spawnRate"],
                (1 - probabilityOfGeneration, probabilityOfGeneration)
            )
            self.structureTextures[index] = (
                texture,
                structureJson["renderingOffset"],
            )
            self.updateTimes[index] = (structureJson["breakTime"],structureJson["placeTime"],structureJson["breakTime"]/config.totalDestroyFrames) # Placing and breaking time of structure
        #print("Update times: ",self.updateTimes)
  



