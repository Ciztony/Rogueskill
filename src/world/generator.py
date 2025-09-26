from config import config,generationData
from src.util.perlin import PerlinNoise



class Generator:
    def __init__(self,chunkSize,seed,structureManager):
        self.chunkSize = chunkSize
        self.spawnDefaultGenerationSize = config.spawnDefaultGenerationSize
        self.perlinNoiseGen = PerlinNoise(seed)
        self.structureManager = structureManager
        self.perlinValues = {int(key):int(value) for key,value in generationData.perlinValues.items()}


    # When chunk is requested
    def requestChunk(self,chunkX,chunkY):

        perlinNoiseGenerator = self.perlinNoiseGen
        chunkSize = self.chunkSize

        staticTiles = {} # Tiles that are reused each frame
        dynamicTiles = {} # Tiles that are layered
        
        structureManager = self.structureManager
        perlinValues = self.perlinValues
        structureSpawnData = structureManager.generateStructureData() # Generate an array of ids with structure ids that determine what structure are able to spawn in this chunk (total 5 chunks -> spawnMaxStructures)
        #print(chunkX,chunkY)
        for x in range(chunkSize):
            for y in range(chunkSize):
                perlinValueAtCoords = perlinNoiseGenerator.perlin(x/chunkSize+chunkX,y/chunkSize+chunkY)
                convertedIntoTileValue = perlinValues[int(max(0, min(perlinValueAtCoords + 0.53, 1)))] # Converts heightmap into blocks
                chunkLayersAtCoords = [convertedIntoTileValue]
                # Generate all possible structures
                for index,spawnData in structureSpawnData.items():
                    structure = structureManager.spawnStructure(spawnData)

                    if structure: # If structure is spawned, add to dynamic tiles
                        dynamicTiles[(x,y)] = index

                staticTiles[(x,y)] = chunkLayersAtCoords

        

        return staticTiles,dynamicTiles
    

    def generateSpawnChunks(self,generateChunk):
        spawnDefaultGenerationSize = self.spawnDefaultGenerationSize
        for x in range(-spawnDefaultGenerationSize,spawnDefaultGenerationSize+1):
            for y in range(-spawnDefaultGenerationSize,spawnDefaultGenerationSize+1):
                # Within radius
                if (x*x + y*y) <= (spawnDefaultGenerationSize* spawnDefaultGenerationSize):
                    generateChunk((x,y))
    
    
