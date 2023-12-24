#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Advent of code 2023 - Day 24
"""

import argparse
import numpy as np
from skspatial.objects import Line
import z3


def get_args():
    """
    Cmd line argument parsing (preprocessing)
    """
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Advent of code 2023: Day 24'
        )

    # Add arguments
    parser.add_argument(
        '-i',
        '--infile',
        type=str,
        help='Inputfilename',
        required=True
        )

    # Array for all arguments passed to script
    args = parser.parse_args()

    # Return arg variables
    return args.infile


def read_data_struct(filename):
    """
    Read data from file and convert it to data structure
    """
    data = []
    with open(filename, "r", encoding="utf-8") as fileh:
        data = fileh.readlines()
    data = [x.strip() for x in data]

    hails = []
    for line in data:
        pos, vel = line.split(' @ ')
        hails.append([[int(x) for x in pos.split(', ')], [int(x) for x in vel.split(', ')]])

    return hails


def find_intersection_point(point1, vector1, point2, vector2):
    """
    find intersection on two lines defined by points and vectors
    """
    # Convert inputs to NumPy arrays for vector operations
    poi1 = np.array(point1, dtype=float)
    vec1 = np.array(vector1, dtype=float)
    poi2 = np.array(point2, dtype=float)
    vec2 = np.array(vector2, dtype=float)

    # Solve for t1 and t2
    try:
        pars = np.linalg.solve(np.vstack([vec1, -vec2]).T, poi2 - poi1)
    except np.linalg.LinAlgError:
        # Lines are parallel or coincident, no unique intersection point
        return None

    # Calculate the intersection point
    intersection_point = poi1 + pars[0] * vec1

    return intersection_point


def find_intersections_xy(hails):
    """
    Find number of intersections in given area after given time
    """
    mintest = 200000000000000
    maxtest = 400000000000000

    num = len(hails)
    sums = 0
    for idx in range(0, num):
        for jdx in range(idx+1, num):
            inter = find_intersection_point(hails[idx][0][0:2], hails[idx][1][0:2], hails[jdx][0][0:2], hails[jdx][1][0:2])
            if inter is None:
                continue
            past = False
            for kdx in range(0, 2):
                if hails[idx][1][kdx] > 0 and hails[idx][0][kdx] > inter[kdx]:
                    past = True
                    break
                if hails[idx][1][kdx] < 0 and hails[idx][0][kdx] < inter[kdx]:
                    past = True
                    break
                if hails[jdx][1][kdx] > 0 and hails[jdx][0][kdx] > inter[kdx]:
                    past = True
                    break
                if hails[jdx][1][kdx] < 0 and hails[jdx][0][kdx] < inter[kdx]:
                    past = True
                    break
            if past:
                continue
            if mintest <= inter[0] <= maxtest and mintest <= inter[1] <= maxtest:
                sums += 1

    return sums


def intersect_3d(rock, hail):
    """
    Find point of intersection
    """

    line_a = Line(point=rock[0], direction=rock[1])
    line_b = Line(point=hail[0], direction=hail[1])
    try:
        line_a.intersect_line(line_b)
    except Exception:
        return False
    return True


def find_init_pos(data):
    """
    find initial position for global intersection
    """
    init = []
    diff = {}
    for line in data:
        init.append(line[0][2])
        diff[line[0][2]] = line[1][2]

    # first hit in first second
    start_points = []
    for item in data:  # testing
        start_points.append([item[0][0] + item[1][0], item[0][1] + item[1][1], item[0][2] + item[1][2]])  # possible start points (at time 1)
    time = 0
    while True:
        time += 1
        print(f'\nTime to hit second hail = {time+1}')
        for rockpos in start_points:
            print('.', end='', flush=True)
            for idx, item in enumerate(data):
                # try to identify the vector
                hailpos = [0, 0, 0]
                delta = [0, 0, 0]
                for kdx in range(0, 3):
                    hailpos[kdx] = item[0][kdx] + (time+1) * item[1][kdx]
                    delta[kdx] = hailpos[kdx] - rockpos[kdx]
                # check the vector result
                check = True
                for jdx, checkline in enumerate(data):
                    res = intersect_3d([rockpos, delta], checkline)
                    if idx == jdx:
                        res = True
                    if not res:
                        check = False
                        break
                if check:
                    print(f'\nFINAL P={rockpos}, V={delta}')
                    return 1


def analytic_rock_position(data):
    """
    solve equations
    """
    # define solver
    solver = z3.Solver()

    # define variables for evaluating
    point_x = z3.Int("px")
    point_y = z3.Int("py")
    point_z = z3.Int("pz")
    vect_x = z3.Int("vx")
    vect_y = z3.Int("vy")
    vect_z = z3.Int("vz")

    # add formulas
    for idx, value in enumerate(data):
        time = z3.Int(f"t{idx}")
        solver.add(point_x + time * vect_x == value[0][0] + time * value[1][0])
        solver.add(point_y + time * vect_y == value[0][1] + time * value[1][1])
        solver.add(point_z + time * vect_z == value[0][2] + time * value[1][2])
        solver.add(time >= 0)

    # solve
    solver.check()
    model = solver.model()
    return model.evaluate(point_x).as_long() + model.evaluate(point_y).as_long() + model.evaluate(point_z).as_long()


def main():
    """
    Main function
    """

    # process args
    infile = get_args()

    # read data
    data = read_data_struct(infile)

    # part 1
    count = find_intersections_xy(data)
    print(f"Part 1 solution : {count}")

    # part 2
    # count = find_init_pos(data) # only for example data
    count = analytic_rock_position(data)
    print(f"Part 2 solution: {count}")


if __name__ == '__main__':
    main()

# EOF
