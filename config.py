from src.util.file import loadFile
from src.util.optionReader import ReadOptions

optionReader = ReadOptions()

class GenerationData:
    def __init__(self):
        self.generationData = loadFile("assets/data/generation.json","json")
        self.perlinValues = self.generationData["perlinValues"]
        

class Config:
    def setHardCodedAttributes(self):
        self.playerWindowPosition = self.windowWidth // 2,self.windowHeight // 2
        self.breakingAnimationRenderingOffset = int(self.breakingAnimationSize * (1/7)), int(self.breakingAnimationSize * (5/7)) # Basically the rendering offset for the breaking animation

        
    scale: int = 1.5
    tileSize: int = int(48 * scale)
    playerTileSize = scale * 120
    playerAnimationSpeed = 0.1
    chunkSize: int = 16
    chunkPixels: int = tileSize * chunkSize
    spawnDefaultGenerationSize: int = 8
    verticalRenderDistance: int = 3
    horizontalRenderDistance: int = 3
    playerVelocity: int = 9 * tileSize
    skyColour: tuple = (198, 252, 255)
    totalDestroyFrames: int = 9


config = Config()
optionReader.readOptions(config,"options.txt")
config.setHardCodedAttributes()
generationData = GenerationData()