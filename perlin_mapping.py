from perlinNoise import perlin
import numpy as np
# biome definitions

class BiomeRules():
    def __init__(self):
        
        self.biomes = { # ID:BIOME
            1: "OCEAN",
            2: "GRASSLAND",
            3: "FOREST",
            4: "SWAMP",
            5: "DESERT",
            6: "HILLS",
            7: "MOUNTAINS", 
            8: "BEACH"
        }

        self.biome_colours = {
            1: (0,0,128),          #OCEAN
            2: (34,139,34),       #GRASSLAND
            3: (0,100,0),         #FOREST
            4: (47,79,79),        #SWAMP
            5: (210,180,140),     #DESERT
            6: (65,89,23),       #HILLS
            7: (139,137,137),     #MOUNTAINS
            8: (238,214,175)      #BEACH

        }

        #ID assignment
        self.OCEAN_ID = 1
        self.GRASSLAND_ID = 2
        self.FOREST_ID = 3
        self.SWAMP_ID = 4
        self.DESERT_ID = 5
        self.HILLS_ID = 6
        self.MOUNTAINS_ID = 7
        self.BEACH_ID = 8

        # noise maps will be normalised to 0->1 range 
        # noise maps for altiude, temperature, and moisture

        #altitude
        self.OCEAN_LEVEL = 0.5
        self.BEACH_LEVEL = 0.51
        self.HILL_LEVEL = 0.6
        self.MOUNTAIN_LEVEL = 0.65

        #moisture
        self.DESERT_MOISTURE = 0.4
        self.GRASSLAND_MOISTURE = 0.5
        self.FOREST_MOISTURE = 0.55
        self.SWAMP_MOISTURE = 0.65

        #temperature   
        self.MOUNTAINS_TEMP = 0.2
        self.SWAMP_TEMP = 0.3
        self.FOREST_TEMP = 0.4
        self.GRASSLAND_TEMP = 0.5
        self.DESERT_TEMP = 0.7

rules = BiomeRules()

def noise_map_to_biome_map(altitude_map, moisture_map, temperature_map, perlin_width, perlin_height):
    print(rules.HILL_LEVEL)
    #need to mask
    #start by assigning biome map to all sea. then move on from there. assigning heights first then moving onto to override into other biomes. slowly build up layers. 
    biome_map = np.full_like(altitude_map, rules.OCEAN_ID, dtype=np.uint8) # restricts values to 8 bit integers which is probably more efficient or something
    
    # create maps then overlay them onto the biome map

    land_mask = altitude_map >= rules.OCEAN_LEVEL # should return array of booleans where this applies
    hill_mask = altitude_map >= rules.HILL_LEVEL
    mountain_mask = altitude_map >= rules.MOUNTAIN_LEVEL
    
    # apply masks

    biome_map[land_mask] = rules.GRASSLAND_ID
    biome_map[hill_mask] = rules.HILLS_ID
    biome_map[mountain_mask] = rules.MOUNTAINS_ID

    # for more specialised biomes perhaps I should use if statements?!? Deciding, i.e. near sea for beach, wet and hot for swamp? 
    # need to do swamp, desert, forest, beach. apply beach first perhaps because not all coastlines have a beach idk? 
    # numpy uses bitwise operators. AND &, OR | , NOT~

    is_swamp = (temperature_map >= rules.SWAMP_TEMP) & ~hill_mask & land_mask & (moisture_map >= rules.SWAMP_MOISTURE)   # swamps are cold, not hills but on land, and very moist. 
    is_desert = (temperature_map >= rules.DESERT_TEMP) & land_mask & (moisture_map < rules.DESERT_MOISTURE) # deserts are rather warm, on any land, and rather dry
    is_forest = (temperature_map >= rules.FOREST_TEMP) & ~hill_mask & land_mask & (moisture_map >= rules.FOREST_MOISTURE) 
    is_beach = (altitude_map<rules.BEACH_LEVEL) & land_mask & ~hill_mask & ~is_swamp & ~is_desert & (temperature_map>= 0.5) & (moisture_map<0.6) 

    #apply specialised biome masks
    biome_map[is_swamp] = rules.SWAMP_ID
    biome_map[is_desert] = rules.DESERT_ID
    biome_map[is_forest] = rules.FOREST_ID
    biome_map[is_beach] = rules.BEACH_ID

    # apply colours
    map_array = np.zeros((perlin_height, perlin_width,3), dtype=np.uint8) # 3 deep for RGB, unit provides range from 0-255
    
    map_array[biome_map==rules.OCEAN_ID] = rules.biome_colours[rules.OCEAN_ID]
    map_array[biome_map==rules.GRASSLAND_ID] = rules.biome_colours[rules.GRASSLAND_ID]
    map_array[biome_map==rules.FOREST_ID] = rules.biome_colours[rules.FOREST_ID]
    map_array[biome_map==rules.SWAMP_ID] = rules.biome_colours[rules.SWAMP_ID]
    map_array[biome_map==rules.DESERT_ID] = rules.biome_colours[rules.DESERT_ID]
    map_array[biome_map==rules.HILLS_ID] = rules.biome_colours[rules.HILLS_ID]
    map_array[biome_map==rules.MOUNTAINS_ID] = rules.biome_colours[rules.MOUNTAINS_ID]
    map_array[biome_map==rules.BEACH_ID] = rules.biome_colours[rules.BEACH_ID]

    return map_array, biome_map

