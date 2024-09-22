import picar_4wd as fc
import numpy as np
import sys
from PIL import Image


speed = 0


def scan_surroundings(angle): # half of angle we want surveyed
    angle_dist = []
    angles = list(range(-angle, angle, 5))
    for curr_angle in angles:
        angle_dist.append(fc.get_distance_at(curr_angle))
    print(angles)
    print(angle_dist)

    surrounding_map = np.zeros((100, 100))
    for i in range(len(angles)):
        r, theta = angle_dist[i], angles[i]
        y, x = int(r * np.cos(np.radians(theta))), int(r * np.sin(np.radians(theta))+50)
        if (x < 100 and y < 100):
            surrounding_map[y][x] = 1
    print(surrounding_map)

    array_image = (1-surrounding_map)*255
    img = Image.fromarray(array_image.astype(np.uint8), mode='L')
    img.save('img.png')
    img.show()

def main():
    np.set_printoptions(threshold=sys.maxsize)
    #while True:
    scan_surroundings(90)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
