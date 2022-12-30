'''Function for directory management'''
import os 

def _create_directory(shockname):
    if os.path.exists('bld')==True:
        if os.path.exists(f'bld/{shockname}')==True:
            pass
        else:
            os.makedirs(f'bld/{shockname}')
    else:
        os.makedirs('bld')
        os.makedirs(f'bld/{shockname}')