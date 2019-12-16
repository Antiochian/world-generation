# -*- coding: utf-8 -*- python3
"""
Created on Mon Dec 16 18:39:42 2019

@author: Antiochian

Pack all the constants required into 2 dictionaries
"""

bordercolor = (0,0,0,50)
borderthickness = 2
centroidcolor = (0,0,0,0)

debugcolor = (224, 101, 214)

oceancolor = (47, 137, 160)
deepoceancolor = (39, 70, 135)
lightgreen = (54, 138, 57)
darkgreen = (108, 171, 79)

beachcolor = (207, 205, 85)
mountaincolor = (140, 148, 136)
snowcolor = (215, 224, 211)

#misc
image_border = 3#cutoff amount (in form of N*avg_cell_size)
FPS = 12

#voronoi constants
avgpoints = 10000
pointspread = 0.3*avgpoints
graphscalex = 5
graphscaley = 5
windowscale = 100 #total window size = graphscale*windowscale

voronoi_repeats = 2

#shader constants
avg_ocean_threshold = 0.5
min_ocean_threshold = 0.2
ocean_spread = 0.1
beach_threshold = 0.05 #ie: if height/oceanthreshold is between 1 and this, paint beach
mountain_threshold = 0.55
snow_threshold = 0.65

#simplex noise constants
basefreq = 0.005 #1/Nx
f1 = basefreq
a1 = 1
f2 = basefreq*2
a2 = 0.5
f3 = basefreq*4
a3 = 0.25

constant_dictionary = {}
color_dictionary = {}

#color constants packing
color_dictionary['borderthickness'] = borderthickness
color_dictionary['bordercolor'] = bordercolor
color_dictionary['centroidcolor'] = centroidcolor    
color_dictionary['debugcolor'] = debugcolor
color_dictionary['oceancolor'] = oceancolor
color_dictionary['deepoceancolor'] = deepoceancolor
color_dictionary['lightgreen'] = lightgreen
color_dictionary['darkgreen'] = darkgreen
color_dictionary['beachcolor'] = beachcolor
color_dictionary['mountaincolor'] = mountaincolor
color_dictionary['snowcolor'] = snowcolor

#other constants packing
#misc
constant_dictionary['FPS'] = FPS
constant_dictionary['image_border'] = image_border
#voronoi constants
constant_dictionary['avgpoints'] = avgpoints 
constant_dictionary['pointspread'] = pointspread
constant_dictionary['graphscalex'] = graphscalex
constant_dictionary['graphscaley'] = graphscaley
constant_dictionary['windowscale'] = windowscale
constant_dictionary['voronoi_repeats'] = voronoi_repeats
#shader constants
constant_dictionary['avg_ocean_threshold'] = avg_ocean_threshold
constant_dictionary['min_ocean_threshold'] = min_ocean_threshold
constant_dictionary['ocean_spread'] = ocean_spread
constant_dictionary['beach_threshold'] = beach_threshold
constant_dictionary['mountain_threshold'] = mountain_threshold
constant_dictionary['snow_threshold'] = snow_threshold
#simplex noise constants
constant_dictionary['basefreq'] = basefreq
constant_dictionary['f1'] = f1
constant_dictionary['a1'] = a1
constant_dictionary['f2'] = f2
constant_dictionary['a2'] = a2
constant_dictionary['f3'] = f3
constant_dictionary['a3'] = a3