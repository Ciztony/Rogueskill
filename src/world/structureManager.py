from config import config
import numpy as np

class StructureManager:
    def __init__(self, resources):

        self.structureData = resources.structureData
        self.structureTextures = resources.structureTextures
        self.chunkSize = config.chunkSize

    # Generate a list of structure IDs that are eligible to spawn in a chunk
    def generateStructureData(self):
        structureSpawnData = {}
        chunkSize = self.chunkSize
        # Attempt to generate all structures with individual spawn attempt lists, where 0 is no structure
        for index,structureData in self.structureData.items():
            spawnRate,generationProbabilityArray = structureData
            structureSpawnArray = np.random.choice([0,index+1],size=spawnRate,p=generationProbabilityArray) # Contains ids on whether structure of this index has spawned
            spawnStructureProbability = (chunkSize ** 2) / spawnRate # The probability of a block in a chunk being a structure of a certain index
            structureSpawnData[index] = tuple(structureSpawnArray),spawnStructureProbability
        #print("StructureSpawnData",structureSpawnData)
        return structureSpawnData
    
    # Determine whether a structure should spawn
    @staticmethod 
    def spawnStructure(structureSpawnData):
        # Random integer between 0 and spawnStructureProbability
        structureSpawnArray,spawnStructureProbability = structureSpawnData
        spawnStructure = int(np.random.random() * spawnStructureProbability)
        
        # Conditions for spawning:
        # 1. Random number must equal 5
        # 2. There must be at least one structure in the array
        # 3. The last structure ID cannot be 0 (assumed "no structure")
        if spawnStructure == 5 and len(structureSpawnArray) > 0 and structureSpawnArray[-1] != 0:
            return True
        
        # Otherwise, do not spawn
        return False