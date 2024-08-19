# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:02:50 2024

@author: lcuev
"""
import src.header as h 
import os
os.system('color')
getter = h.Climb_Getter()
intro = """Welcome to ZynDex!
To quit, type a single character then press [enter].
To search a problem, type its name then press [enter].
------------------------------------------------------"""
print(intro)

while True:
    try:
        climb_name = input(': ')
        climb = getter.get(climb_name)
        print(climb.climb_string())
    except KeyError:
        print('\nQuitting...\n')
        break
    except Exception as error:
        print(error)
        continue
    


