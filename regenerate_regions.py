# -*- coding: utf-8 -*- python3
"""
Created on Mon Dec 16 16:25:32 2019

@author: Antiochian

output regionlist and borderlist
"""
from scipy.spatial import Voronoi
import numpy as np
import random
import time
import noise
import makedict

#unpack constants
class region_object:
    def __init__(self,shape,noiseseed,ocean_threshold):
        #unpack required constants
        self.noiseseed = noiseseed
        self.ocean_threshold = ocean_threshold
        self.shape = shape
        self.centroid = self.get_centroid()
        self.raw_elevation = self.get_elevation()
        self.elevation_ratio = (self.raw_elevation-self.ocean_threshold)/(1-self.ocean_threshold)
        #etc
        return
    
    def get_centroid(self):
        x_total = 0
        y_total = 0
        for vertex in self.shape:
            x_total += vertex[0]
            y_total += vertex[1]
        centroid = [x_total/len(self.shape) , y_total/len(self.shape)]
        return centroid
    
    def get_elevation(self):
        windowscale = makedict.constant_dictionary['windowscale']
        
        elevation = get_noise(self.centroid[0]*windowscale,self.centroid[1]*windowscale,self.noiseseed)
        return elevation

def generate_voronoi():
    
    avgpoints = makedict.constant_dictionary['avgpoints']
    pointspread = makedict.constant_dictionary['pointspread']
    graphscalex = makedict.constant_dictionary['graphscalex']
    graphscaley = makedict.constant_dictionary['graphscaley']
    
    n = int(np.random.normal(avgpoints,pointspread))
    if n < 12:
        n = 12 #minimum bound for adequate simplex  
    points = []
    for i in range(n):
        points.append([graphscalex*random.random(),graphscaley*random.random()])
    vor = Voronoi(points)
    return vor,points

def improve_voronoi(vor,points):
    
    voronoi_repeats = makedict.constant_dictionary['voronoi_repeats']
    
    if voronoi_repeats == 0:
        return vor,points
    
    for k in range(voronoi_repeats):
        #first make new points
        newpoints = []
        finite_regions = extract_regionshapes(vor)
        for region in finite_regions:
            x_total = 0
            y_total = 0
            for vertex in region:
                x_total += vertex[0]
                y_total += vertex[1]
            centroid = [x_total/len(region) , y_total/len(region)]
            newpoints.append(centroid)
        #then, add in old infinite-region points (will be later clipped by extract_regionshapes)
        #there is probably a faster way to do this, but since this openly happens once on startup its not a huge deal
        for index in range(len(vor.regions)-1): #clip non-finite regions
            if vor.regions[index] != [] and -1 in vor.regions[index]:
                newpoints.append(points[index])
        #compute new, improved voronoi graph
        vor = Voronoi(newpoints)
        points = newpoints
    return vor, points

def get_noise(x,y,noiseseed):
    
    f1 = makedict.constant_dictionary['f1']
    f2 = makedict.constant_dictionary['f2']
    f3 = makedict.constant_dictionary['f3']
    a1 = makedict.constant_dictionary['a1']
    a2 = makedict.constant_dictionary['a2']
    a3 = makedict.constant_dictionary['a3']
    
    x = int(x)
    y = int(y)
    noise1 = noise.snoise3(f1*x,f1*y,noiseseed)
    noise2 = noise.snoise3(f2*x,f2*y,noiseseed)
    noise3 = noise.snoise3(f3*x,f3*y,noiseseed)
    noisevalue = a1*noise1 + a2*noise2 + a3*noise3
    #normalise to 0-1
    noisevalue = noisevalue + (a1 + a2 + a3)
    noisevalue = noisevalue*0.5/(a1 + a2 + a3)
    return noisevalue

def extract_regionshapes(vor):
    #like vor to class but without the class bit
    finite_regions = []
    for region in vor.regions: #clip non-finite regions
        if region != [] and not -1 in region:
            finite_regions.append(region)
    region_shapes = []
    for region in finite_regions:
        coords = []
        for index in region:
            coords.append(vor.vertices[index])
        region_shapes.append(coords)
    return region_shapes

def vor_to_class(vor):
    #this also extracts the regionshapes coordinates
    noiseseed = vor.seed
    ocean_threshold = vor.ocean_threshold
    finite_regions = []
    for region in vor.regions: #clip non-finite regions
        if region != [] and not -1 in region:
            finite_regions.append(region)
    region_shapes = []
    for region in finite_regions:
        coords = []
        for index in region:
            coords.append(vor.vertices[index])
        regionlist.append(region_object(coords,noiseseed,ocean_threshold))
        
    generate_borderlist(vor)
    return region_shapes

def generate_borderlist(vor):
    for line in vor.ridge_vertices:
        if line != [] and not -1 in line:
            line_coords = []
            line_coords = [ vor.vertices[line[0]],vor.vertices[line[1]] ]
            borderlist.append(line_coords)
    return

def regenerate():
    global regionlist, borderlist
    regionlist = []
    borderlist = []
    
    min_ocean_threshold = makedict.constant_dictionary['min_ocean_threshold']
    avg_ocean_threshold = makedict.constant_dictionary['avg_ocean_threshold']
    ocean_spread = makedict.constant_dictionary['ocean_spread']
    
    t0 = time.time()
    print("\n \n \n --- Regenerating... --- \n \n")
    regionlist.clear()
    borderlist.clear()
    vor,points = generate_voronoi()
    vor,points = improve_voronoi(vor,points)
    vor.seed = 1000*(random.random() - 0.5)
    vor.ocean_threshold = max(min_ocean_threshold,np.random.normal(avg_ocean_threshold,ocean_spread))

    vor_to_class(vor)   
    print("\n--- Debug Info ---")
    print("Ocean strength ~",round(vor.ocean_threshold,3)*100,"%")
    print("Noise seed:",round(vor.seed,8))
    print("Polygons generated:",len(regionlist))
    print("Time taken:",round(time.time()-t0,5),"seconds")
    return regionlist, borderlist

