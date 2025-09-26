from time import time
from math import floor


class BlockUpdates:
    def __init__(self,inputManager,resources):
        self.inputManager = inputManager

        self.breakTimers = {} # Track via dictionary to prevent carrying over of time
        self.placeTimers = {}
        self.updateTimes = resources.updateTimes
        self.previousBlockPlaced = None
        self.renderBreakingAnimation = False
        #self.breakStartTimeTemp = 0
    
    def updateBlocks(self,mouseBlockX,mouseBlockY,dynamicTiles):
        im = self.inputManager
        now = time()

        #print("Dynamic Tiles",dynamicTiles)
        coordinates = (floor((mouseBlockX+8)%16),floor(mouseBlockY+8)%16)
        self.blockBeingUpdated = coordinates
        blockIsInDynamicTiles = coordinates in dynamicTiles
        #print("Coordinates mouse:",coordinates)
        breakTimers= self.breakTimers
        # Remove timers for coordinates no longer under the cursor and not being pressed
        for coord in list(breakTimers.keys()):
            if coord != coordinates or not im.getMouseClickPressed("Break"):
                del breakTimers[coord]

        #for coord in list(placeTimers.keys()):
            #if coord != coordinates or not im.getMouseClickPressed("Place"):
                #del placeTimers[coord]

        updateTimes = self.updateTimes # Where each id for a block stores its breaking time and placing time
        blockUpdated = [False,False] # Flag for toggling whether a block update has occured
        if im.getMouseClickPressed("Break") and blockIsInDynamicTiles: # If block is there and button for break pressed, then update
            id = dynamicTiles[coordinates]
            updateTimesForId = updateTimes[id]
            if coordinates not in breakTimers:
                #self.breakStartTimeTemp = now
                self.renderBreakingAnimation = True
                breakTimers[coordinates] = [now,0] # If not in breakTimers, means that the block is not currently being broken whatsoever
            elif (timeElapsed:=now-breakTimers[coordinates][0]) >= updateTimesForId[0]: # Check whether breaking interval has elapsed
                #print(now-self.breakStartTimeTemp,"s")
                del dynamicTiles[coordinates]
                del breakTimers[coordinates] # Remove the timer for the current block since it is broken
                blockUpdated[0] = True
                self.renderBreakingAnimation = False
            else:
                breakTimers[coordinates][1] = int(timeElapsed//updateTimesForId[2])
        else:
            #self.breakStartTimeTemp = 0
            self.renderBreakingAnimation = False
            breakTimers.pop(coordinates,None) # Pop the timer for the current block in the instance that the block is in dynamic tiles but not broken
            # None ensures error isnt raised if there indeed is no block there

        if im.getMouseClickPressed("Place") and coordinates != self.previousBlockPlaced and coordinates not in dynamicTiles: # If block is there and button for break pressed, then update
            #self.breakStartTimeTemp = 0
            self.renderBreakingAnimation = False
            id = 0 # Temporary block to place
            #if coordinates not in placeTimers:
                #placeTimers[coordinates] = now # If not in placeTimers, means that the block is not currently being placed whatsoever
            #elif now - placeTimers[coordinates] >= updateTimes[id][1]: # Check whether breaking interval has elapsed
            dynamicTiles[coordinates] = id
            self.previousBlockPlaced = coordinates
            #del placeTimers[coordinates] # Remove the timer for the current block since it is placed
            blockUpdated[1] = True
        #else:
            #placeTimers.pop(coordinates,None) # Pop the timer for the current block in the instance that the block is in dynamic tiles but not placed
    def getCurrentBlockBroken(self):
        return self.breakTimers[self.blockBeingUpdated][1]
  

