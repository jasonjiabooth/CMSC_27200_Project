import sys
import numpy as np


GRID_SIZE = 400
TIME = 1440


def check_input(n, rides, size='small'):
    limits = {
        'small': (15, 25),
        'medium': (40, 60),
        'large': (150, 200),
    }
    try:
        if not (limits[size][0] <= n <= limits[size][1]):
            raise ValueError(f'Wrong number of nodes = {n}.')
        if n != len(rides):
            raise ValueError(f'N = {n}, but {len(rides)} rides were found in the file.')
        if not ((0 <= rides[:, 0:2]).all() and (rides[:, 0:2] <= GRID_SIZE).all()):
            raise ValueError(f'Rides coordinates are not in [0, {GRID_SIZE}].')
        if not ((0 <= rides[:, 2]).all() and
                (rides[:, 2] <= rides[:, 3]).all() and
                (rides[:, 3] <= TIME).all()):
            raise ValueError(f'Opening and closing times are wrong.')
        if not ((0 <= rides[:, 4]).all() and (rides[:, 4] <= 27200).all()):
            raise ValueError(f'Profits values are wrong.')
        if not ((0 <= rides[:, 5]).all() and (rides[:, 5] <= 1440).all()):
            raise ValueError(f'Visit times are wrong')
    except Exception as e:
        return e
    return None


def usage():
    print('Input file checker. Usage:')
    print(f'{sys.argv[0]} {{small,medium,large}}{{1,2,3}}.in')


def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    filename = sys.argv[1]
    sizes = ['small', 'medium', 'large']
    s = None
    for i in sizes:
        if filename.startswith(i):
            s = i
            break
    if s is None:
        print(f'Filename {filename} has unknown size.', file=sys.stderr)
        usage()
        sys.exit(1)
    for i in range(3):
        if filename == f'{s}{i+1}.in':
            break
    else:
        print(f'Filename {filename} has wrong name', file=sys.stderr)
        usage()
        sys.exit(1)
    with open(filename) as f:
        n = int(f.readline())
        rides = np.array([[int(i) for i in line.split()] for line in f])
        e_in = check_input(n, rides, size=s)
        if e_in is not None:
            print(e_in, file=sys.stderr)


if __name__ == '__main__':
    main()