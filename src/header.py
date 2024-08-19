# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 13:09:37 2024

@author: lcuev
"""
import sqlite3 as sql
from termcolor import colored

class Climb:
    ROLES = {5:'start', 6:'middle',7:'finish',8:'foot'}
    SYMS = {5: '$', 6: 'O', 7:'#',8: '*' }
    COLS = {5: 'green', 6: 'blue', 7: 'red', 8:'magenta'}

    def __init__(self, climb_name):
        self.name = climb_name
        self.matrix = []
        self.grade = None
        
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
                    if self.is_near((x,y), (x_,y_)):
                        string += colored(self.SYMS[role],self.COLS[role])
                        occupied = True
                        break
                if not occupied:
                    string += ' '
            string += '|\n'
        string += '-' * (SX+C+2) + '\n'
        string += f'Difficulty: {self.grade}'
        return string
    
    def is_near(self,xy0,xy1):
        return (xy0[0] - xy1[0]) ** 2 + (xy0[1] - xy1[1]) ** 2 <= 1
    
class Climb_Getter:
    def __init__(self):
        pass
    
    def get(self,climb_name):
        self.name=climb_name
        climb = Climb(climb_name)
        con = sql.connect('dbs/Tension.sqlite')
        cur = con.cursor()
        fetched = cur.execute(f'SELECT frames FROM climbs WHERE name=\'{climb_name}\';').fetchone()
        climb_string = self.valid_fetch(fetched)
        fetched = cur.execute(f'SELECT uuid FROM climbs WHERE name=\'{climb_name}\';').fetchone()
        climb_uuid = self.valid_fetch(fetched)
        fetched = cur.execute(f'SELECT difficulty_average FROM climb_stats WHERE climb_uuid=\'{climb_uuid}\';').fetchone()
        climb.grade = int(self.valid_fetch(fetched))
        place_roles = climb_string[1:].split('p')
        for place_role in place_roles:
            place, role = place_role.split('r')
            fetched = cur.execute(f'SELECT hole_id FROM placements WHERE id={place};').fetchone()
            hole_id = self.valid_fetch(fetched)
            fetched = cur.execute(f'SELECT x FROM holes WHERE id={hole_id};').fetchone()
            x = int(self.valid_fetch(fetched))
            fetched = cur.execute(f'SELECT y FROM holes WHERE id={hole_id};').fetchone()
            y = int(self.valid_fetch(fetched))
            climb.matrix += [(x,y,int(role))]
        con.close()
        climb.matrix = sorted(climb.matrix,key=lambda x: x[2])
        return self.valid_climb(climb)
    
    def valid_fetch(self,fetched):
        if fetched is None:
            self.error()
        return fetched[0]
    
    def valid_climb(self,climb):
        if not len(climb.matrix):
            self.error()
        if not isinstance(climb.grade,int):
            self.error()
        return climb
    
    def error(self):
        raise Exception(f'\'{self.name}\' does not exist in archive.')
    
    
    


