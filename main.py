# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:02:50 2024

@author: lcuev
"""
import src.header as h 
getter = h.Climb_Getter()

while True:
    try:
        climb_name = input('Name: ')
        climb = getter.get(climb_name)
        print(climb.climb_string())
    except NameError as error:
        print(error)
        continue
    except:
        break
    
print('\nSession terminating...\n')

