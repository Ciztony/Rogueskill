from shutil import rmtree
from os import path,makedirs
import sys
from config import config
from src.world.chunkManager import ChunkManager
from src.world.dynamicLayeringManager import DynamicLayereringManager
from src.entity.player import Player
from src.world.blockUpdates import BlockUpdates
from src.util.hud import Hud


class World:
    def __init__(self,worldName,seed,resources,inputManager,window):
        self.worldName = worldName
        self.inputManager = inputManager
        self._createWorldFolders()
        self._bootPlayer(resources)
        self._bootRender(resources,window)
        self.chunkManager = ChunkManager(self.player,resources,seed)
        self.blockUpdates = BlockUpdates(inputManager,resources)
        self._setUpScene()

    def _createWorldFolders(self):
        worldFolderPath = f"worlds/{self.worldName}"
        worldName = self.worldName

        if path.exists(worldFolderPath):
            print(f"World of folder name: {worldName} exists. Attempting override.")
            try:
                rmtree(worldFolderPath)
            except Exception as e:
                if isinstance(e,PermissionError):
                    print(f"Error occurred during override: Unable to delete folder of {worldName}")
                else:
                    print(f"Error occurred during override: Unable to delete folder of {e}")
        try:
            makedirs(worldFolderPath,exist_ok=True) # Create world folder
        except Exception as e:
            print(f"Error occured while creating world folder: {e}. Proceed to exit game.")
            sys.exit(1)

    def _bootRender(self,resources,window):
        self.atlas = resources.blockAtlas
        self.skyColour = config.skyColour # Kept as internal variable as the world might start off in a death screen
        self.font = resources.font
        self.hud = Hud(resources) # Store here cos hud variables different across worlds
        self.cachedWindowDimensions = window.windowDimensions
        self.breakingRenderingOffsetX,self.breakingRenderingOffsetY = config.breakingAnimationRenderingOffset
    
    def _bootPlayer(self,resources):
        self.playerWindowPosition = config.playerWindowPosition
        self.player = Player(config.playerWindowPosition,self.inputManager,resources)

    def _setUpScene(self):
        self.chunkManager.generateSpawnChunks()
        self.dynamicLayeringManager = DynamicLayereringManager(self.chunkManager.structureManager,self.chunkManager.chunkObjectsReference) # Create only when chunkObjectReferences have been updated

    def prepForFullScreen(self,newPlayerWindowPosition,newVertRendDis,newHorzRendDis,windowDimensions):
        self.player.updateWindowPosition(newPlayerWindowPosition)
        nx,ny = newVertRendDis,newHorzRendDis
        self.cachedWindowDimensions = windowDimensions
        self.chunkManager.applyWindowSizeChangeToChunks(nx,ny)


    def _updateMouse(self,mousePosition):
        player = self.player
        #mouseInChunkX,mouseInChunkY,mouseChunkX,mouseChunkY = 
        self.hud.getBlockMouseTouching(player.playerWindowPosition,mousePosition,player.playerBlockX,player.playerBlockY)

    def update(self,mousePosition,dt):
        chunkChange = self.player.updatePosition(dt)

        chunkManager = self.chunkManager
        if chunkChange is not None:
            chunkManager.moveChunksWithinFrustum(chunkChange)

        hud = self.hud
        self._updateMouse(mousePosition)
        mouseChunkCoordinates = hud.mousePositionalData[2],hud.mousePositionalData[3] # Chunk position of the mouse cursor
        #print("Mouse chunk coordinates",mouseChunkCoordinates)
        if mouseChunkCoordinates in chunkManager.chunkObjectsReference:
            self.renderBreakingAnimation = True
            self.blockUpdates.updateBlocks(
                hud.mouseBlockX,
                hud.mouseBlockY,
                chunkManager.chunkObjectsReference[mouseChunkCoordinates].dynamicTiles,
            )
        
    
    def render(self,window,fps,mousePosition):
        hud = self.hud
        player = self.player
        chunkManager = self.chunkManager
        blockUpdates = self.blockUpdates
        window.fill((self.skyColour))    
        loadedChunks,coordinates = chunkManager.renderLoadedChunks(window)
        windowDimensions = self.cachedWindowDimensions
        dLT = self.dynamicLayeringManager
        # Render the dynamic textures
        dLT.generateDynamicTextureDrawStack(loadedChunks,coordinates,windowDimensions)
        dLT.addPlayerToDrawStack(player.getPlayerTexture(),windowDimensions) # Add player to draw stack
        dLT.renderDynamicTextureDrawStack(window)

        hud.displayDebug(window,fps,player)
        if blockUpdates.renderBreakingAnimation and self.renderBreakingAnimation:
            self.renderBreakingAnimation = False
            #print(blockUpdates.renderBreakingAnimation,self.updateCoords)
            hud.renderBlockBreakingAnimation(
                window,
                blockUpdates.getCurrentBlockBroken(),
                mousePosition[0]-self.breakingRenderingOffsetX,
                mousePosition[1]-self.breakingRenderingOffsetY
                )
        #hud.renderBlockOutline(window,mousePosition)