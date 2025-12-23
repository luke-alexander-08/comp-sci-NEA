# from perlinNoise import perlin
from old.perlinNoiseold import fractal_noise
import time

# fractal_noise(2,2,0.6,2.0,12,(1024,512))

start = time.time()
fractal_noise(2,2,0.6,2.0,octaves=12,dimensions=(1024,512))
print(time.time()-start)



