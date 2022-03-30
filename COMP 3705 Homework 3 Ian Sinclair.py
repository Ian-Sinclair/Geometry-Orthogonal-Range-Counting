# -*- coding: utf-8 -*-
"""
Author:                 Ian Sinclair
Date Created:           2/7/2022
Functionality:          Program implements orthogonal range counting algorithm
                        Allows user to interactively add points, then query using
                        any upright rectangle.
                        Click to add points.
                        Click 'add box' button then drag click to add a query box.
                        add a new query box by drag clicking again.
                        To switch back to adding points, click 'add points' button.
"""


import tkinter as tk 
from tkinter import *
from tkinter import filedialog



class point() :
    def __init__( self, x: int, y: int, z : int = 0) :
        self.x = x
        self.y = y
        self.z = z
    
    def isEqual( self, p ) :
        if self.x == p.x and self.y == p.y and self.z == p.z:
            return True
        return False
    
    def toString( self ) :
        return "( " + str( self.x ) + ", " + str( self.y ) + ", " + str(self.z) + " )"
    
    def draw( self ) :
        point_rad = 4
        self.color = canvas.create_oval(self.x-point_rad, 
                                        self.y-point_rad, 
                                        self.x+point_rad, 
                                        self.y+point_rad, 
                                        fill = 'yellow')
    
    def update_color( self, color : str) :
        canvas.itemconfig(self.color, fill=color)
    
    
    
    
class rectangle() :
    def __init__( self, a : point, c : point, b : point = None, d : point = None ) :
        if b == None and d == None :
            b = point(a.x, c.y)
            d = point(c.x, a.y)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.L1 = canvas.create_line(self.a.x,self.a.y,self.b.x,self.b.y, fill = 'red' )
        self.L2 = canvas.create_line(self.a.x,
                           self.a.y,
                           self.d.x,
                           self.d.y,
                           fill = 'red' )
        self.L3 = canvas.create_line(self.b.x,
                           self.b.y,
                           self.c.x,
                           self.c.y,
                           fill = 'red' )
        self.L4 = canvas.create_line(self.c.x,
                           self.c.y,
                           self.d.x,
                           self.d.y,
                           fill = 'red' )
    
    def update_A( self, u : point) :
        self.a = u
        self.b = point(self.a.x, self.c.y)
        self.d = point(self.c.x, self.a.y)
        self.draw_rectangle()

    def update_C( self, u : point) :
        self.c = u
        self.b = point(self.a.x, self.c.y)
        self.d = point(self.c.x, self.a.y)
    
    def draw_rectangle( self ) :
        canvas.coords(self.L1, (self.a.x,self.a.y,self.b.x,self.b.y) )
        canvas.coords(self.L2, (self.a.x,
                           self.a.y,
                           self.d.x,
                           self.d.y) )
        canvas.coords(self.L3, (self.b.x,
                           self.b.y,
                           self.c.x,
                           self.c.y) )
        canvas.coords(self.L4, (self.c.x,
                           self.c.y,
                           self.d.x,
                           self.d.y) )

class point_locus() :
    def __init__(self) :
        self.locus = {}
        self.points = []
        self.rectangles = []
    
    def add_point(self, v : point ) :
        self.points += [v]
        self.locus = locus_preprocess( self.points )
        v.draw()
    
    def new_rectangle( self ) :
        self.rectangles += [ rectangle(point(0,0), point(0,0) ) ]
    
    def update_rectangle_C( self, u : point ) :
        if len( self.rectangles ) == 0:
            self.new_rectangle()
        self.rectangles[-1].update_C( u )
        for v in self.points :
            v.update_color('yellow')
    
    def update_rectangle_A( self, u : point ) :
        if len( self.rectangles ) == 0:
            self.new_rectangle()
        self.rectangles[-1].update_A( u )
    
    def query_rectangle( self ) :
        Bounded = orthogonal_range_counting( self.rectangles[-1], self.locus )
        if Bounded is not None :
            for v in Bounded :
                v.update_color('green')
        return Bounded
    
    def track_rectangle( self, u : point ) :
        self.tracking_rectangle.update_A( u )
    
    def clearAll( self ) :
        self.locus = {}
        self.points = []
        self.rectangles = []
    









"""
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

            HOMEWORK 3
            
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& 
       
----------------------------------
    Orthogonal Range Counting
----------------------------------
"""

def locus_preprocess( points : list ) :
    y_sort_points = sorted(points, key=lambda v: v.y)
    loci = {}
    
    for v in y_sort_points :
        #loci[v.y] = [ point(0,0) ]
        loci[v.y] = []
        loci[v.y] += sorted(y_sort_points[0:y_sort_points.index(v)+1], key=lambda q: q.x)
    
    
    return loci
    
def dominates( u : point, locus : dict ) :
    keys = locus.keys()
    q_y = 0
    
    dominated = []
    
    for i in keys :
        if i <= u.y:
            q_y = i
        else :
            break
            
    if q_y == 0 :
        return []
    
    for v in locus[q_y] :
        if v.x <= u.x:
            dominated += [v]
    
    return dominated


def orthogonal_range_counting( R : rectangle, Locus: dict) :
    y_max = max([R.a.y, R.b.y, R.c.y, R.d.y])
    x_max = max([R.a.x, R.b.x, R.c.x, R.d.x])
    
    y_min = min([R.a.y, R.b.y, R.c.y, R.d.y])
    x_min = min([R.a.x, R.b.x, R.c.x, R.d.x])
    
    
    A = point(x_max,y_max)
    B = point(x_max,y_min)
    C = point(x_min,y_min)
    D = point(x_min, y_max)
    
    dom_A = dominates(A , Locus)
    dom_B = dominates(B , Locus)
    dom_C = dominates(C , Locus)
    dom_D = dominates(D , Locus)

    for v in dom_C :
        dom_B.remove(v)
    
    for v in dom_B + dom_D :
        dom_A.remove(v)
    
    return dom_A



def click( event ) :
    x,y = event.x, event.y
    if ShapeToggle.config('relief')[-1] == 'raised':
        main_locus.add_point( point(x,y) )
        
    else:
        main_locus.update_rectangle_C( point(x,y) )
        
    
def drag( event ) :
    if ShapeToggle.config('relief')[-1] != 'raised':
        x,y = event.x, event.y
        main_locus.update_rectangle_A( point(x,y) )

def release( event ) :
    if ShapeToggle.config('relief')[-1] != 'raised':
        main_locus.query_rectangle()
        
def ClearScreen() :
    canvas.delete("all")
    main_locus.clearAll()

def toggle() :
    if ShapeToggle.config('relief')[-1] == 'sunken':
        ShapeToggle.config(relief="raised", text = "Add Query Box", bg = 'light blue')
        
    else:
        ShapeToggle.config(relief="sunken", text = "Add Point", bg = '#A877BA')



def init_GUI () :
    global canvas
    global root
    global ShapeToggle
    global color
    
    global main_locus
    main_locus = point_locus()
    
    
    root = tk.Tk()
    root.title("COMP 3705 HW 0 Ian Sinclair")
    root.geometry('800x400')
    
    ClearButton = Button(root, text = 'Clear', bd = '5',
                          command = ClearScreen)
    ClearButton.pack(side = 'top')
    
    ShapeToggle = tk.Button(text="Add Query Box", width=12, relief="raised", command = toggle, bg = 'light blue')
    ShapeToggle.pack(side = 'top')
    
    canvas = Canvas(root, width = 100, height = 100, bg = "black")
    canvas.pack(expand = YES, fill = BOTH)
    
    canvas.bind("<ButtonPress-1>", click)
    canvas.bind("<B1-Motion>", drag) 
    canvas.bind('<ButtonRelease-1>', release)
    

    message = Label( root, text = "Click to add a new point" )
    message.pack( side = BOTTOM )



def main() :    
    pass


def driver1() :
    L = locus_preprocess( [point(15,20), point(20,15), point(13,50), point(9,10)] )
    orthogonal_range_counting(rectangle(point(10,10),point(40,40)), L)


if __name__ == "__main__" :
    init_GUI()
    
    #main()
    #driver1()
    
    root.mainloop()
    
    
    