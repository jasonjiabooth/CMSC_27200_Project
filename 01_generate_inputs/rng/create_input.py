import random
import csv
import os

num_attr_sm = [15, 25]
num_attr_me = [40, 60]
num_attr_lg = [150, 200]

coords = [0, 400]
open_close = [0, 1440]
utility = [1, 27200]
durations = [1, 1440]

d_path = './data'

file_name_dict = {
  15: 'small',
  40: 'medium',
  150: 'large',
}

def main():
  for size in [num_attr_sm, num_attr_me, num_attr_lg]:
    for i in range(1,4): # for different inputs
      num_attr = random.randint(*size)
      file_name = os.path.join(d_path, file_name_dict[size[0]] + f'{i}.in')

      lines = [[num_attr]]
      for _ in range(num_attr):
        x, y = random.randint(*coords), random.randint(*coords)
        o = random.randint(*open_close)
        c = random.randint(o, open_close[1])
        u = random.randint(*utility)
        t = random.randint(*durations)

        lines.append([x,y,o,c,u,t])


      with open(file_name, 'w+') as data_file:
        writer = csv.writer(data_file, delimiter=' ')
        writer.writerows(lines)

if __name__ == '__main__':
  if not os.path.isdir(d_path):
    os.mkdir(d_path)
  main()