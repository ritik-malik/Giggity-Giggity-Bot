import pickle
import os


def ADD_NOTE(name,user_ID):
    os.chdir(user_ID)
    f_name = name
    name = {}
    with open(f_name, 'wb') as handle:
        pickle.dump(name, handle, protocol=pickle.HIGHEST_PROTOCOL)
    os.chdir('..')
    return 1


def NEW_NOTE(name,user_ID):
    
    if user_ID in os.listdir():
        if name in os.listdir(user_ID):
            return 0
        else:
           return ADD_NOTE(name,user_ID)
            
    else:
        os.mkdir(user_ID)
        return ADD_NOTE(name,user_ID)


def SHOW_ALL(user_ID):
    
    if user_ID in os.listdir():
        return '\n'.join(os.listdir(user_ID))
    else:
        return 0


def APPEND_NOTE(name,user_ID,data):
    
    if user_ID in os.listdir():
        if name in os.listdir(user_ID):
            
            data.pop(0)
            os.chdir(user_ID)
            
            with open(name, 'rb') as handle:
                data_dict = pickle.load(handle)
                
            if not bool(data_dict):
                data_dict[0] = data
            else:
                data_dict[max(data_dict)+1] = data
                
            with open(name, 'wb') as handle:
                pickle.dump(data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

            os.chdir('..')
            return 1
        else:
            return 0
    else:
        return 0


def SHOW_NOTE(name,user_ID):
    
    if user_ID in os.listdir():
        if name in os.listdir(user_ID):
            
            os.chdir(user_ID)
            
            with open(name, 'rb') as handle:
                data_dict = pickle.load(handle)
                
            if not bool(data_dict):
                os.chdir('..')
                return 1
            
            else:    
                note = ''
                for key in data_dict:
                    note=note+str(key)+'. '
                    for value in data_dict[key]:
                        note=note+value+' '
                    note+='\n'
                
                os.chdir('..')
                return note
        else:
            return 0
    else:
        return 0
            

def RM_FROM_NOTE(name,user_ID,note_ID):
    
    if user_ID in os.listdir():
        if name in os.listdir(user_ID):
            
            os.chdir(user_ID)
            
            with open(name, 'rb') as handle:
                data_dict = pickle.load(handle)
                
            if not bool(data_dict):
                os.chdir('..')          # empty note
                return 'empty_note'
            
            else:

                if note_ID in data_dict:
                    
                    for key in range(note_ID, len(data_dict)-1):
                        data_dict[key] = data_dict[key+1]
                    
                    del data_dict[len(data_dict)-1]
                    
                    with open(name, 'wb') as handle:
                        pickle.dump(data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    os.chdir('..')
                    return 'done'
                else:
                    os.chdir('..')
                    return 'key_not_found'
        else:
            return 0
    else:
        return 0
    
    
def RM_NOTE(name,user_ID):
    
    if user_ID in os.listdir():
        if name in os.listdir(user_ID):
            
            temp = user_ID+'/'+name
            os.remove(temp)
            return 1
        else:
            return 0
    else:
        return 0


def RM_USER(user_ID):
    
    if user_ID in os.listdir():
        temp = 'rm -rf '+user_ID
        os.system(temp)
        return 1
    else:
        return 0
