#!/usr/bin/python3 

import os
import classyjson as cj


def getConfig(confPath = "./secret.json"):
    """ Return json from config file

        Input:  confPath (Str) path to file
        Output: config (cj) config
    """
    # Read in config 

    if not os.path.isfile(confPath):
        msg = f"{confPath} not found! Please add it and try again"
        raise FileNotFoundError(msg)

    with open(confPath) as file:
        config = cj.load(file)
    
    return config
    
def getCogs(): 
    """ Return list of Cogs for bot to load

        Input:  None
        Output: (List) Cog name list in form cogs.<name>
    """

    cogList = []
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            cogName = f"cogs.{file[:-3]}"
            cogList.append(cogName)
    
    return cogList

            

    