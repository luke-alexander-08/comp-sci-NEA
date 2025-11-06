from perlinNoise import perlin
import time 
import random
import numpy as np


gradients = [(1, 0), (0.707, 0.707), (0, 1), (-0.707, 0.707), (-1, 0), (-0.707, -0.707), (0, -1), (0.707, -0.707)] # 8 pseudorandom gradient vectors which will be assigned to each point

start = time.time()

def hash_func(ix, iy): # hash function using large primes
    # print()
    return (ix * 1836311903 ^ iy * 2971215073) & 0xffffffff

def get_gradient(ix,iy):
        y = (hash_func(ix,iy) % 8)
        return gradients[y]  # indexed from 0,7

for _ in range(1000000):
    ix, iy = (random.randint(1,10000), random.randint(1,10000))
    nearby_corners = [(ix,iy), (ix+1,iy), (ix,iy+1), (ix+1,iy+1)]
    gradients2 = [get_gradient(a,b) for a,b in nearby_corners] 



end = time.time()
# print(end)
print(end-start)

start = time.time()
perm_table = np.arange(0, 255, dtype=int) # start, stop, data type. returns nums from 0-255
np.random.shuffle(perm_table)
perm_table = np.stack([perm_table, perm_table]).flatten() # duplicate elements of the table, then turns it one dimensional using flatten(). apparently therefore making it more efficient to perform operations, as no need for modulo fucntion. 

x, y = np.meshgrid(np.arange(100, dtype=float), np.arange(100, dtype=float))

x /= 100
y /= 100

scaled_x = x 
scaled_y = y

xi = scaled_x.astype(int) # cast numpy array to integer parts. 
xf = scaled_x - xi # get fraction parts

yi = scaled_y.astype(int) # cast numpy array to integer parts. 
yf = scaled_y - yi # get fraction parts

# find hash values for each corner and then find gradients

h_ul = perm_table[perm_table[xi & 255] + (yi&255)] # using AND operations to ensure all elements are held within the array. Array was doubled earlier, so that modulo isn't used now - instead simple AND is sure to be constrained to the set. 
h_ur = perm_table[perm_table[(xi+1) & 255] + (yi&255)]
h_bl = perm_table[perm_table[xi & 255] + ((yi+1)&255)]
h_br = perm_table[perm_table[(xi+1) & 255] + ((yi+1)&255)]

g_ul = gradients[h_ul % 8]
g_ur = gradients[h_ur % 8]
g_bl = gradients[h_bl % 8]
g_br = gradients[h_br % 8]

end=time.time()

print(end-start)