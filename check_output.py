import sys
import numpy as np


GRID_SIZE = 400
TIME = 1440


def check_score_output(N, rides, M, visits):
    """First check that the output is correct for this input
    and also return a score."""
    if M != len(visits):
        return ValueError(f'Expected to find {M} points, found {len(visits)}.'), 0, 0
    total_time = 0
    score = 0
    last = np.array([GRID_SIZE // 2, GRID_SIZE // 2, 0, TIME, 0, 0])
    visited_set = set()
    for point in visits:
        if not (1 <= point <= N):
            return ValueError(f'Point index {point} is out of bounds {{1, ..., {N}}}.'), 0, 0
        if point in visited_set:
            return ValueError(f'Visited point {point} more than once.'), 0, 0
        visited_set.add(point)
        dist = np.ceil(np.linalg.norm(rides[point-1, 0:2] - last[0:2]))
        o, _, u, t = rides[point-1, 2:]
        last = rides[point-1]
        total_time = max(total_time + dist, o) + t
        score += u
    dist = np.ceil(np.linalg.norm(np.array([GRID_SIZE // 2, GRID_SIZE // 2]) - last[0:2]))
    total_time += dist
    if total_time > TIME:
        return ValueError(f'Total travel time t = {total_time} is greater than {TIME}.'), 0, 0
    return None, score, total_time


def usage():
    print('Input file checker. Usage:')
    print(f'{sys.argv[0]} {{small,medium,large}}{{1,2,3}}.in {{small,medium,large}}{{1,2,3}}.out')


def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    filename_in = sys.argv[1]
    filename_out = sys.argv[2]
    sizes = ['small', 'medium', 'large']
    s = None
    for i in sizes:
        if filename_out.startswith(i):
            s = i
            break
    if s is None:
        print(f'Filename {filename_out} has unknown size.', file=sys.stderr)
        usage()
        sys.exit(1)
    for i in range(3):
        if filename_out == f'{s}{i+1}.out':
            break
    else:
        print(f'Filename {filename_out} has wrong name', file=sys.stderr)
        usage()
        sys.exit(1)
    with open(filename_in) as f:
        n = int(f.readline())
        rides = np.array([[int(i) for i in line.split()] for line in f])
    with open(filename_out) as f:
        m = int(f.readline())
        visits = [int(i) for i in f.readline().split()]
        e_out, score, total_time = check_score_output(n, rides, m, visits)
        if e_out is not None:
            print(e_out, file=sys.stderr)
        else:
            print(f'Time = {total_time:.0f} Score = {score:.0f}')


if __name__ == '__main__':
    main()