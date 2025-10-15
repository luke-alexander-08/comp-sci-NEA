def hash_func(ix, iy): # hash function using large primes
    # print()
    return (ix * 1836311903 ^ iy * 2971215073) & 0xffffffff


print(hash_func(8,7))