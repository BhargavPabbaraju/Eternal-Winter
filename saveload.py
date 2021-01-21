####IMPORTS
import shelve


saveData = shelve.open('savedata')
if 'exists' not in saveData:
    saveData['exists'] = False
##GAME STATUS
saveData = shelve.open('savedata')
if 'exists' not in saveData:
    saveData['exists'] = False




        

#####SWITCHES






####VARIABLES

def set(variable,data):
    saveData[variable]=data




def new_data(name='Red',gender=0):
    #####MAP DATA
    for i in range(10):
        saveData['Map'+str(i).zfill(3)]=0
        saveData['S'+str(i).zfill(3)]=0
        saveData['V'+str(i).zfill(3)]=0
    

    saveData['curmap'] = 1
    saveData['playerpos'] = (0,0)
    saveData['player'] = None



