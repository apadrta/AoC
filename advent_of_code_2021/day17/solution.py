#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2021 - Day 17
"""


def get_max_pos(initvel):
    """
    Compute max distance (height for y)
    """
    # print(initvel)
    lastpos = -1
    pos = 0
    vel = initvel
    while lastpos < pos:
        lastpos = pos
        pos += vel
        vel -= 1
    return lastpos


class ElfProbes():
    """
    Class for firing probes to target
    """

    def __init__(self, topleft, bottomright):
        """
        Constructor
        """
        self.left = topleft
        self.right = bottomright

    def get_possible_velx(self):
        """
        Precompute possible velx to end in x-interval
        """
        vels = []
        start_vel = 1
        while True:
            vel = start_vel
            pos = 0
            while vel > 0:
                pos += vel
                if self.left[0] <= pos <= self.right[0]:
                    vels.append(start_vel)
                vel -= 1
            start_vel += 1
            if start_vel > self.right[0]:
                break
        return vels

    def get_possible_vely(self):
        """
        Precompute possible vels to end in y-interval
        """
        vels = []
        start_vel = 0
        while True:
            vel = start_vel
            pos = 0
            while pos >= self.right[1]:
                pos += vel
                if self.left[1] >= pos >= self.right[1]:
                    vels.append(start_vel)
                vel -= 1
            start_vel += 1
            if start_vel > 1000:
                break
        return vels

    def compute_highest(self):
        """
        Compute parameters
        """
        vels = self.get_possible_vely()
        return get_max_pos(vels[-1])

    def compute_max(self):
        """
        Compute parameters
        """
        sols = 0
        start_velx = 1
        while True:
            start_vely = self.right[1]
            while True:
                vely = start_vely
                velx = start_velx
                posy = 0
                posx = 0
                # print(f"velocity = ({start_velx}, {start_vely})")
                while posy > self.right[1]:
                    posx += velx
                    posy += vely
                    velx -= 1
                    if velx < 0:
                        velx = 0
                    vely -= 1
                    if self.left[0] <= posx <= self.right[0] and self.left[1] >= posy >= self.right[1]:
                        sols += 1
                        break
                start_vely += 1
                if start_vely > 1000:
                    break
            start_velx += 1
            if start_velx > self.right[0]:
                break
        return sols


def main():
    """
    Main function
    """

    # read data
    obj = ElfProbes([195, -67], [238, -93])
    obj = ElfProbes([20, -5], [30, -10])

    # part 1
    print(f"Part 1 solution: {obj.compute_highest()}")

    # part 2
    print(f"Part 2 solution: {obj.compute_max()}")


if __name__ == '__main__':
    main()

# EOF
