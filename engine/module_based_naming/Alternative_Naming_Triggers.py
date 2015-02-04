def CheckIfModule(name):
    try: 
        a = sectorsInModule(name)
        return True
    except:
        return False

def CheckIfHalfModule(name):
    try: 
        a = sectorsInHalfModule(name)
        return True
    except:
        return False
