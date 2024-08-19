# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 13:09:37 2024

@author: lcuev
"""
import sqlite3 as sql
from termcolor import colored

def is_near(xy0,xy1):
    return (xy0[0] - xy1[0]) ** 2 + (xy0[1] - xy1[1]) ** 2 < 2

class Climb:
    ROLES = {5:'start', 6:'middle',7:'finish',8:'foot'}
    SYMS = {5: '$', 6: 'O', 7:'#',8: '*' }
    COLS = {5: 'green', 6: 'blue', 7: 'red', 8:'magenta'}

    def __init__(self, climb_name, climb_matrix):
        self.name = climb_name
        self.matrix = climb_matrix
        
    def string(self):
        string = ''
        for x,y,role in self.matrix:
            string += f'{self.ROLES[role]} at ({x}, {y})\n'
        return string
    
    def climb_string(self):
        C = 2
        D = 4
        SX = 64*2//C
        SY = 140//D
        
        string = '-' * (SX+C+2) + '\n'
        for Y in range(SY+D):
            string += '|'
            for X in range(SX+C):
                x, y = C*(X-SX//2), D*(SY - Y)
                occupied = False
                for x_,y_,role in self.matrix:
                    if is_near((x,y), (x_,y_)):
                        string += colored(self.SYMS[role],self.COLS[role])
                        occupied = True
                        break
                if not occupied:
                    string += ' '
            string += '|\n'
        string += '-' * (SX+C+2) + '\n'
        return string
    
class Climb_Getter:
    def __init__(self):
        pass
    
    def get(self,climb_name):
        con = sql.connect('dbs/Tension.sqlite')
        cur = con.cursor()
        climb_string = cur.execute(f'SELECT frames FROM climbs WHERE name=\'{climb_name}\';').fetchone()
        if climb_string is None:
            raise NameError(f'{climb_name} does not exist in archive.')
        if not len(climb_string):
            self.error()
        climb_string = climb_string[0]
        climb_matrix = []
        place_roles = climb_string[1:].split('p')
        for place_role in place_roles:
            place, role = place_role.split('r')
            hole_id = cur.execute(f'SELECT hole_id FROM placements WHERE id={place};').fetchone()[0]
            x = cur.execute(f'SELECT x FROM holes WHERE id={hole_id};').fetchone()[0]
            y = cur.execute(f'SELECT y FROM holes WHERE id={hole_id};').fetchone()[0]
            climb_matrix += [(int(x),int(y),int(role))]
        con.close()
        climb_matrix = sorted(climb_matrix,key=lambda x: x[2])
        return Climb(climb_name, climb_matrix)
        
    def error(self):
        raise Exception("CLimb Getter failed.")
    


