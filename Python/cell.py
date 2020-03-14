import numpy as np
import matplotlib.pyplot as plt

# world size
length = 10
width = 10
# birth rank
world = np.random.randint(0, 100, [length, width]) < 50
world_cope = np.zeros([length, width])
# stop when world not change
while not (world_cope == world).all():
    world_cope = world.copy()
    # update world
    for x in range(length):
        for y in range(width):
            # statistic around cell number
            count = sum(sum(world_cope[max(0, x - 1):min(length, x + 2),
                            max(0, y - 1):min(width, y + 2)])) - world_cope[x, y]
            world[x, y] = 2 < count < 5
    # show image
    plt.imshow(world, 'gray')
    # grow speed
    plt.pause(0.1)
