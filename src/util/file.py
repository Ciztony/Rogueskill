import pickle
import json




def saveToFile(data,filePath:str,type:str) -> None:
    try:
        if type == "pickle":
            with open(filePath,"wb") as file:
                pickle.dump(data,file)
        elif type == "json":
            with open(filePath,"w") as file:
                json.dump(data,file)
        elif type == "txt":
            with open(filePath,"w") as file:
                file.write(data,file)
        else:
            raise ValueError("Unsupported file type:",type)
    except Exception as e:
        print("Error occured while saving file: ",e)
        return 

def loadFile(filePath:str,type:str) -> None:
    try:
        if type == "pickle":
            with open(filePath,"rb") as file:
                return pickle.load(file)
        elif type == "json":
            with open(filePath,"r") as file:
                return json.load(file)
        elif type == "txt":
            with open(filePath,"r") as file:
                return file.readlines()
        else:
            raise ValueError("Unsupported file type:",type)
    except Exception as e:
        print("Error occured while loading file: ",e)
        return 
