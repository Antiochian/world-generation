# -*- coding: utf-8 -*- python3
"""
Created on Sun Dec 15 01:38:23 2019

@author: Antiochian

#region vertices

#marine contents: [region1,region2,...]
region1 = [region_shape , region_centroid]
#terrestial contents: [region1, region2,...]
region1 = [ region_shape , region_centroid, region_elevation,
                       region_temperature, region_precipitaion, biome, color, name?]

PLAN:
    make basic square grid
    overlay polygonal mesh on top of it
    set the traits of each polygon to the grid value at its centroid coordinate

"""

import pygame
import sys

import makedict
import regenerate_regions

global regionlist
regionlist = []
global borderlist
borderlist = []

#color_dictionary, constant_dictionary = makedict.color_dictionary, makedict.constant_dictionary


def init_pygame():
    
    graphscalex = makedict.constant_dictionary['graphscalex']
    graphscaley = makedict.constant_dictionary['graphscaley']
    windowscale = makedict.constant_dictionary['windowscale']
    
    pygame.init()
    Nx = graphscalex*windowscale
    Ny = graphscaley*windowscale
    Nx,Ny = int(Nx),int(Ny)
    window = pygame.display.set_mode( (Nx,Ny) )
    polylayer = pygame.Surface( (Nx,Ny), pygame.SRCALPHA ) 
    borderlayer = pygame.Surface( (Nx,Ny), pygame.SRCALPHA )
    centroidlayer = pygame.Surface( (Nx,Ny), pygame.SRCALPHA )
    return Nx,Ny,window,polylayer, borderlayer,centroidlayer

def clear():
    
    debugcolor = makedict.color_dictionary['debugcolor']
    
    window.fill(debugcolor)
    polylayer.fill(0)
    borderlayer.fill(0)
    centroidlayer.fill(0)
    return

def draw():
    draw_regions()
    draw_borders()
    draw_centroids()
    window.blit(polylayer, (0,0))
    window.blit(borderlayer, (0,0))
    window.blit(centroidlayer, (0,0))
    return

def shader(region):
    
    oceancolor = makedict.color_dictionary['oceancolor']
    deepoceancolor = makedict.color_dictionary['deepoceancolor']
    beachcolor = makedict.color_dictionary['beachcolor']
    snowcolor = makedict.color_dictionary['snowcolor']
    mountaincolor = makedict.color_dictionary['mountaincolor']
    lightgreen = makedict.color_dictionary['lightgreen']
    darkgreen = makedict.color_dictionary['darkgreen']
    debugcolor = makedict.color_dictionary['debugcolor']
    
    beach_threshold = makedict.constant_dictionary['beach_threshold']
    snow_threshold = makedict.constant_dictionary['snow_threshold']
    mountain_threshold = makedict.constant_dictionary['mountain_threshold']
    
    #ocean border
    ratio = region.elevation_ratio
    if ratio < 0:
        if ratio < -1:
            ratio = -1 #tapefix
        color = blend_color(oceancolor,deepoceancolor,-ratio)
    elif ratio < beach_threshold:
        color = beachcolor
    elif ratio > snow_threshold:
        color = snowcolor
    elif ratio > mountain_threshold:
        color = mountaincolor
    elif beach_threshold < ratio < mountain_threshold:
        newratio = (ratio-beach_threshold)/(mountain_threshold - beach_threshold)
        color = blend_color(lightgreen,darkgreen,newratio)
    else:
        color = debugcolor
    return color


def blend_color(lowcolor,highcolor,power):
    #power should be 0-1
    R = ( lowcolor[0]*(1-power) + highcolor[0]*power )
    G = ( lowcolor[1]*(1-power) + highcolor[1]*power )
    B = ( lowcolor[2]*(1-power) + highcolor[2]*power )
    
    color = (int(R),int(G),int(B))
    return color

def draw_regions():
    
    windowscale = makedict.constant_dictionary['windowscale']
    debugcolor = makedict.color_dictionary['debugcolor']
    
    for region in regionlist:
        #scale regions
        region_vertices = region.shape
        region_vertices = [x * windowscale for x in region_vertices]
        color = shader(region)
        #clip colors
        if any([not(-1 < x < 256) for x in color]):
            print("Color outside range:",color)
            color = debugcolor
        pygame.draw.polygon(polylayer, color, region_vertices)
    return


def draw_borders():
    
    windowscale = makedict.constant_dictionary['windowscale']
    bordercolor = makedict.color_dictionary['bordercolor']
    borderthickness = makedict.color_dictionary['borderthickness']
    for segment in borderlist:
        segment = [x * windowscale for x in segment]
        pygame.draw.line(borderlayer, bordercolor, segment[0],segment[1], borderthickness)
    return

def draw_centroids():
    windowscale = makedict.constant_dictionary['windowscale']
    centroidcolor = makedict.color_dictionary['centroidcolor']
    for region in regionlist:
        centroid_coord = [int(x*windowscale) for x in region.centroid]
        pygame.draw.circle(centroidlayer,centroidcolor,centroid_coord,1)
    return

def regenerate():
    global regionlist, borderlist
    regionlist, borderlist = regenerate_regions.regenerate()
    return

def main():

    FPS = makedict.constant_dictionary['FPS']

    regenerate()
    clear()
    draw()    
    pygame.display.update()
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)

        for event in pygame.event.get(): #detect events
            if event.type == pygame.QUIT: #detect attempted exit
                pygame.quit()
                sys.exit()      #these 2 optional lines fix a hangup bug in IDLE 
                
            if  pygame.key.get_pressed()[114]: #R to reset
                regenerate()
                clear()
                draw()    
                pygame.display.update()
        
        
Nx,Ny,window,polylayer,borderlayer,centroidlayer = init_pygame()
if __name__ == "__main__":
    main()
    