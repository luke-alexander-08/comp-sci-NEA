from perlinNoise import perlin
from collections import deque # deque has more efficient time complexity. 
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
        self.DEEP_OCEAN_LEVEL = 0.45
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

        #rivers
        self.SOURCE_HEIGHT = 0.6
        self.SOURCE_MOISTURE = 0.55
        self.NUMBER_OF_RIVERS = 3
        self.MAX_LAKE_SIZE = 5000000

rules = BiomeRules()

def noise_map_to_biome_map(altitude_map, moisture_map, temperature_map, perlin_width, perlin_height, SEED):
    print(altitude_map)
    print(rules.HILL_LEVEL)
    #need to mask
    #start by assigning biome map to all sea. then move on from there. assigning heights first then moving onto to override into other biomes. slowly build up layers. 
    biome_map = np.full_like(altitude_map, rules.DEEP_OCEAN_ID, dtype=np.uint8) # restricts values to 8 bit integers which is probably more efficient
    np.random.seed(SEED)
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

    paths, sinks = calculate_river_sources(altitude_map, moisture_map, temperature_map, biome_map)

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

    for sink in sinks:
        for node in sink:
                map_array[node[0], node[1]] = rules.biome_colours[rules.OCEAN_ID]


    print(map_array.ndim, "dims")
    print(map_array)

    return map_array, biome_map.transpose()

def calculate_river_sources(altitude_map, moisture_map, temperature_map, biome_map):
    height_mask = altitude_map >= rules.SOURCE_HEIGHT
    moisture_mask = moisture_map >= rules.SOURCE_MOISTURE

    source_map = np.full_like(altitude_map, False, dtype=np.uint8) # Set all values to false initially
    source_map[height_mask & moisture_mask] = True

    coords = np.transpose(np.nonzero(source_map))
    if len(coords) == 0:
        return None
    # print(list(coords))

    random_sample_coords = np.random.choice(len(coords), rules.NUMBER_OF_RIVERS)

    random_coords = coords[random_sample_coords]

    paths = []
    sink_nodes = []
    for y,x in random_coords:
        global sink 
        sink = set()
        path, sinks = calculate_river_flow(altitude_map, coord = [y,x])
        # print(path, "print")
        paths.append(path)
        sink_nodes += (sinks)

    return paths, sink_nodes
    
surrounding = [[1, 0], [0, 1], [-1, 0],[0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

def calculate_river_flow(altitude_map, coord): # while loop
    path = []
    sinks = []
    y, x = coord
    
    while True:
        path.append((y,x))
        print((y,x), "current coord. ")
        lowest_neighbour = next_lowest_neighbour(y, x, altitude_map=altitude_map)

        if lowest_neighbour == None:
            # print("Sink!")   
            # print(sinks) 
            lowest_neighbour, sink_nodes = fill_sink(y, x, altitude_map=altitude_map)
            sinks += sink_nodes
            if lowest_neighbour==None:
                break
        elif altitude_map[lowest_neighbour[0], lowest_neighbour[1]] <= rules.OCEAN_LEVEL: 
            break

        y, x = lowest_neighbour

    return path, sinks

def next_lowest_neighbour(y, x, altitude_map):
    rows, columns = np.shape(altitude_map)
    lowest_neighbour = None
    current_coord_height = altitude_map[y,x]

    for dy, dx in surrounding:
        ny = y + dy
        nx = x + dx
        if 0 <= ny < rows and 0 <= nx < columns: # in array bounds. 
            if altitude_map[ny, nx] < current_coord_height and (ny,nx) not in sink:
                current_coord_height = altitude_map[ny, nx]
                lowest_neighbour = [ny, nx]

    return lowest_neighbour


def fill_sink(y, x, altitude_map):
    print("Called! on ", (y,x))
    sink.add((y,x))
    current_sink_set = set()
    rows, columns = np.shape(altitude_map) # map boundaries
    # check which coordinates are flooded. 
    edges = set() # coordinates higher than the water level
    search_queue = deque([(y,x)]) # tiles to search
    # print(search_queue, [y,x], "node1")
    sink_height = altitude_map[y,x]

    while len(search_queue) > 0 and len(current_sink_set) < rules.MAX_LAKE_SIZE:
        print(len(search_queue) > 0,  len(current_sink_set) < rules.MAX_LAKE_SIZE)
        node = search_queue.popleft()
        # print(node, "Node")
        y, x = node
        for dy, dx in surrounding: # observe neighbours
            ny = y + dy
            nx = x + dx
            if 0 <= ny < rows and 0 <= nx < columns and (ny,nx) not in sink:
                neighbour_height = altitude_map[ny,nx] #compare to neighbour height
                if neighbour_height > sink_height:
                    edges.add((ny,nx))
                    print("edge add!")
                else:
                    current_sink_set.add((ny,nx))
                    sink.add((ny,nx))
                    search_queue.append([(ny,nx)])

    spill_node = None # spill node will the node on the edge with lowest vlaue 
    lowest_altitude = 2 # impossibly high so overwritten instantly
    
    if edges == []:
        print(current_sink_set)
        edges = find_sink_edges(current_sink_set, altitude_map)


    for rim in edges: 
        rim_altitude = altitude_map[rim[0], rim[1]]
        if rim_altitude < lowest_altitude:
            spill_node = rim
            lowest_altitude = rim_altitude


    if spill_node == None:
        print("No edges? ")
    # print(spill_node, "spill")
    # print(sink, "sink")
    # print(edges, "edges")
    return spill_node, sink
    
def find_sink_edges(current_sink_set, altitude_map):
    rows, columns = np.shape(altitude_map) # map boundaries
    print("Called!")
    sink_edges = set()
    surrounding = [[1,0], [0,1], [-1,0], [0,-1]] # only 4 for now don't really want weird diagonal artifacts maybe. 
    for tile in sink: 
        for dy, dx in surrounding:
            ny  = dy + tile[0]
            nx = dx + tile[1]
            if (ny,nx) not in sink and (0 <= ny < rows and 0 <= nx < columns):
                sink_edges.add((ny,nx))
    print(sink_edges, "sinks")

    return sink_edges



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
