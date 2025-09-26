from src.util.file import loadFile

# Reads options
class ReadOptions:
    def __init__(self):
        self.availableOptions = [
            ("windowWidth","800"),
            ("windowHeight","800"),
            ("frameRate","60"),
            ("breakingAnimationSize","70")
        ]

    @staticmethod # Can be called from other parts of the codebase
    def parseOption(value):
        value = value.strip().lower()

        if value in ("true", "false"):
            return value == "true"

        for convert in (int, float, str):
            try:
                return convert(value)
            except ValueError:
                continue
        
        print(f"Error while reading options: Unable to convert '{value}' into any accepted datatype.")

    def parseText(self,configObject,file):
        for index in range(len(self.availableOptions)):
            configVariableName,defaultValue = self.availableOptions[index]
            if index < len(file):
                line = file[index]
                parsed = [val.strip() for val in line.split(":", 1)]  # Only split at first ":"
                # We bypass check for two values because players might fool around
                value = parsed[-1] # value
                if value == "":
                    value = defaultValue
            else:
                 # The name of the variable (given default value so no problem arise)
                value = defaultValue
            setattr(configObject, configVariableName, ReadOptions.parseOption(value)) # We get from defaultOptions to prevent player editing

    def readOptions(self,configObject,pathToOptions):
        file = loadFile(pathToOptions,"txt")
        print("File:",file)
        self.parseText(configObject,file)