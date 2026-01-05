from perlinNoise import perlin
from collections import deque 
import numpy as np
# biome definitions

class BiomeRules():
    def __init__(self,DEEP_OCEAN_LEVEL, OCEAN_LEVEL, BEACH_LEVEL, HILL_LEVEL, MOUNTAIN_LEVEL,
                        DESERT_MOISTURE, GRASSLAND_MOISTURE, FOREST_MOISTURE, SWAMP_MOISTURE,    
                        MOUNTAINS_TEMP, SWAMP_TEMP, FOREST_TEMP, GRASSLAND_TEMP, DESERT_TEMP,       
                        SOURCE_HEIGHT, SOURCE_MOISTURE, NUMBER_OF_RIVERS, MAX_RIVER_DISTANCE):
        
        self.biomes = { # ID:BIOME
            1: "OCEAN",
            2: "GRASSLAND",
            3: "FOREST",
            4: "SWAMP",
            5: "DESERT",
            6: "HILLS",
            7: "MOUNTAINS", 
            8: "BEACH",
            9: "DEEP OCEAN"
        }

        self.biome_colours = {
            1: (0,0,128),          #OCEAN
            2: (34,139,34),       #GRASSLAND
            3: (0,100,0),         #FOREST
            4: (47,79,79),        #SWAMP
            5: (210,180,140),     #DESERT
            6: (65,89,23),       #HILLS
            7: (139,137,137),     #MOUNTAINS
            8: (238,214,175),      #BEACH
            9: (0,0,110)            #DEEP OCEAN
            
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
        self.DEEP_OCEAN_ID = 9

        # noise maps will be normalised to 0->1 range 
        # noise maps for altiude, temperature, and moisture

        #altitude
        self.DEEP_OCEAN_LEVEL = DEEP_OCEAN_LEVEL
        self.OCEAN_LEVEL = OCEAN_LEVEL
        self.BEACH_LEVEL = BEACH_LEVEL
        self.HILL_LEVEL = HILL_LEVEL
        self.MOUNTAIN_LEVEL = MOUNTAIN_LEVEL

        #moisture
        self.DESERT_MOISTURE = DESERT_MOISTURE
        self.GRASSLAND_MOISTURE = GRASSLAND_MOISTURE
        self.FOREST_MOISTURE = FOREST_MOISTURE
        self.SWAMP_MOISTURE = SWAMP_MOISTURE

        #temperature   
        self.MOUNTAINS_TEMP = MOUNTAINS_TEMP
        self.SWAMP_TEMP = SWAMP_TEMP
        self.FOREST_TEMP = FOREST_TEMP
        self.GRASSLAND_TEMP = GRASSLAND_TEMP
        self.DESERT_TEMP = DESERT_TEMP

        #rivers
        self.SOURCE_HEIGHT = SOURCE_HEIGHT
        self.SOURCE_MOISTURE = SOURCE_MOISTURE
        self.NUMBER_OF_RIVERS = NUMBER_OF_RIVERS
        self.MAX_RIVER_DISTANCE = MAX_RIVER_DISTANCE

def biome_rule_args(
        DEEP_OCEAN_LEVEL= 0.45,
        OCEAN_LEVEL= 0.5,
        BEACH_LEVEL= 0.51,
        HILL_LEVEL= 0.6,
        MOUNTAIN_LEVEL= 0.65,
        DESERT_MOISTURE= 0.4,
        GRASSLAND_MOISTURE= 0.5,
        FOREST_MOISTURE= 0.55,
        SWAMP_MOISTURE= 0.65,
        MOUNTAINS_TEMP= 0.2,
        SWAMP_TEMP=0.3,
        FOREST_TEMP= 0.4,
        GRASSLAND_TEMP= 0.5,
        DESERT_TEMP= 0.7,
        SOURCE_HEIGHT= 0.6,
        SOURCE_MOISTURE= 0.55,
        NUMBER_OF_RIVERS= 10,
        MAX_RIVER_DISTANCE= 100):
    
    rules = BiomeRules(DEEP_OCEAN_LEVEL, OCEAN_LEVEL, BEACH_LEVEL, HILL_LEVEL, MOUNTAIN_LEVEL,
                        DESERT_MOISTURE, GRASSLAND_MOISTURE, FOREST_MOISTURE, SWAMP_MOISTURE,    
                        MOUNTAINS_TEMP, SWAMP_TEMP, FOREST_TEMP, GRASSLAND_TEMP, DESERT_TEMP,       
                        SOURCE_HEIGHT, SOURCE_MOISTURE, NUMBER_OF_RIVERS, MAX_RIVER_DISTANCE)

    return rules

rules = biome_rule_args()

def noise_map_to_biome_map(altitude_map, moisture_map, temperature_map, perlin_width, perlin_height, SEED):
    np.random.seed(SEED)
    print(altitude_map)
    print(rules.HILL_LEVEL)
    #need to mask
    #start by assigning biome map to all sea. then move on from there. assigning heights first then moving onto to override into other biomes. slowly build up layers. 
    biome_map = np.full_like(altitude_map, rules.DEEP_OCEAN_ID, dtype=np.uint8) # restricts values to 8 bit integers which is probably more efficient
    paths, flow_map = calculate_river_sources(altitude_map, moisture_map)

    # create maps then overlay them onto the biome mapnoise
    ocean_mask = altitude_map >= rules.DEEP_OCEAN_LEVEL
    land_mask = altitude_map >= rules.OCEAN_LEVEL # should return array of booleans where this applies
    hill_mask = altitude_map >= rules.HILL_LEVEL
    mountain_mask = altitude_map >= rules.MOUNTAIN_LEVEL
    
    # apply masks
    biome_map[ocean_mask] = rules.OCEAN_ID
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
    

    # print(path, "path")
    # apply colours
    map_array = np.zeros((perlin_height, perlin_width,3), dtype=np.uint8) # 3 deep for RGB, unit provides range from 0-255
    map_array[biome_map==rules.DEEP_OCEAN_ID] = rules.biome_colours[rules.DEEP_OCEAN_ID]
    map_array[biome_map==rules.OCEAN_ID] = rules.biome_colours[rules.OCEAN_ID]
    map_array[biome_map==rules.GRASSLAND_ID] = rules.biome_colours[rules.GRASSLAND_ID]
    map_array[biome_map==rules.FOREST_ID] = rules.biome_colours[rules.FOREST_ID]
    map_array[biome_map==rules.SWAMP_ID] = rules.biome_colours[rules.SWAMP_ID]
    map_array[biome_map==rules.DESERT_ID] = rules.biome_colours[rules.DESERT_ID]
    map_array[biome_map==rules.HILLS_ID] = rules.biome_colours[rules.HILLS_ID]
    map_array[biome_map==rules.MOUNTAINS_ID] = rules.biome_colours[rules.MOUNTAINS_ID]
    map_array[biome_map==rules.BEACH_ID] = rules.biome_colours[rules.BEACH_ID]
#etc
    if paths != None:
        for path in paths:
            for pixel in path:
                # print(pixel)
                map_array[pixel[0], pixel[1]] = rules.biome_colours[rules.OCEAN_ID]

    print(map_array.ndim, "dims")
    print(map_array)

    return map_array, biome_map.transpose(), flow_map

def calculate_river_sources(altitude_map, moisture_map):
    height_mask = altitude_map >= rules.SOURCE_HEIGHT # find sources
    moisture_mask = moisture_map >= rules.SOURCE_MOISTURE
    unaltered_altitude = altitude_map.copy()
    source_map = np.full_like(altitude_map, False, dtype=np.uint8) # set all values to false initially
    source_map[height_mask & moisture_mask] = True

    coords = np.transpose(np.nonzero(source_map))
    if len(coords) == 0:
        return None, None
    print(list(coords))

    random_sample_coords = np.random.choice(len(coords), rules.NUMBER_OF_RIVERS)

    random_coords = coords[random_sample_coords]
    
    flow_map = np.zeros_like(altitude_map)
    paths = []
    for y,x in random_coords:
        path = calculate_river_flow(unaltered_altitude, coord = [y,x], original_altitude=altitude_map)
        carve_map(path, altitude_map)
        print(path)
        for y, x in path:
            flow_map[y,x] += 1
        paths.append(path)

    
    for path in paths:
        for i, river_tile in enumerate(path):
            flow = flow_map[river_tile[0], river_tile[1]]
            carve_map([river_tile], altitude_map, strength=0.02*flow, radius=int(np.sqrt(2*(flow+i))))

    return paths, flow_map
    
surrounding = [[1, 0], [0, 1], [-1, 0],[0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

def calculate_river_flow(altitude_map, coord, original_altitude): # while loop
    path = []
    y, x = coord
    
    while True:
        path.append((y,x))

        lowest_neighbour = next_lowest_neighbour(y, x, altitude_map=altitude_map)

        if lowest_neighbour == None:
            print("Sink")
            path_to_drain, is_lake = find_nearest_drain(y, x, altitude_map=altitude_map)
            if is_lake:
                carve_map([(y,x)],original_altitude,strength=0.1, radius=np.random.randint(10,25))
                break
            print(path_to_drain, "returns")
            path.extend(path_to_drain)
            lowest_neighbour = path_to_drain[-1]
        if altitude_map[lowest_neighbour[0], lowest_neighbour[1]] <= rules.OCEAN_LEVEL:  # current issue is carving goes below ocean level and stops. 
            break
        y, x = lowest_neighbour

        print(f"Current neighbour: {lowest_neighbour}")

    return path

def next_lowest_neighbour(y, x, altitude_map):
    rows, columns = np.shape(altitude_map)
    lowest_neighbour = None
    current_coord_height = altitude_map[y,x]
    for dy, dx in surrounding:
        ny = y + dy
        nx = x + dx
        if 0 <= ny < rows and 0 <= nx < columns: # in array bounds. 
            if altitude_map[ny, nx] < current_coord_height:
                current_coord_height = altitude_map[ny, nx]
                lowest_neighbour = [ny, nx]

    return lowest_neighbour 

def find_nearest_drain(y,x, altitude_map):
    rows, columns = altitude_map.shape
    starting_altitude = altitude_map[y,x]

    search_queue = deque([(y,x)])
    visited = {(y,x): None} # dictionary storing each pos and the pos behind it, for backtracking
    distance_away = None
    while search_queue: 
        current_y, current_x = search_queue.popleft()
        distance_away = ((x- current_x)**2 + (y - current_y)**2)**0.5
        if distance_away > rules.MAX_RIVER_DISTANCE:
            return distance_away, True
        if altitude_map[current_y, current_x] < starting_altitude: 
            # drain found
            sink_path = []
            while True:
                print(current_y, current_x)
                parent = visited[(current_y, current_x)]
                if parent != None:
                    sink_path.append((current_y, current_x))
                    current_y, current_x = visited[(current_y, current_x)]
                else:
                    break
            print(sink_path)
            return sink_path[::-1], False # reverse path so it is from sink to drain
        
        surrounding = [[1, 0], [0, 1], [-1, 0],[0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        np.random.shuffle(surrounding) # shuffling makes rivers more jagged and therefore natural. 

        for dy,dx in surrounding:
            ny = current_y + dy
            nx = current_x + dx
            if 0 <= ny < rows and 0 <= nx < columns and (ny,nx) not in visited: # in array bounds. 
                visited[(ny,nx)] = (current_y ,current_x)
                search_queue.append((ny,nx))

    return [], False

def carve_map(path, altitude_map, strength=0.001, radius=1):
    rows, columns = np.shape(altitude_map)
    for y, x in (path): 
        for dx in range(-radius, radius + 1): # radius around each path. 
            for dy in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= ny < rows and 0 <= nx < columns:
                    distance_to_river = (dx**2 + dy**2)**0.5 # pythagoras
                    reduce = strength * (1/ (distance_to_river+1))

                    altitude_map[ny,nx] -= reduce

# def calculate_river_flow(altitude_map, path, coord, biome_map): # recursive
#     surrounding = [[1, 0], [0, 1], [-1, 0],[0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
#     surrounding = map(np.array, surrounding)
#     # print(coord)
#     lowest_coord = [coord[0], coord[1]]
#     coord_height = altitude_map[coord[0], coord[1]]

#     for tile in surrounding:
#         # print(coord, tile, "Cord")
#         adjacent = tile + coord
#         # print(adjacent, "adjacent")
#         try:
#             if altitude_map[adjacent[0], adjacent[1]] < coord_height:
#                 coord_height = altitude_map[adjacent[0], adjacent[1]]
#                 lowest_coord = [adjacent[0], adjacent[1]]
#         except:
#             pass

#     path.append(lowest_coord)
#     print(path)
#     # print(lowest_coord, coord)
#     if lowest_coord == coord: # endless sink
#         # print("return, sink")
#         return path
#     elif biome_map[lowest_coord[0], lowest_coord[1]] == 1:
#         # print("return, sea")
#         return path
#     else:
#         # print("recursion")
#         return calculate_river_flow(altitude_map, path, lowest_coord, biome_map)
