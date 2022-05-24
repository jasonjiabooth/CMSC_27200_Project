import random

def generate_input(N, path):
    f = open(path, "w+") 
    # Print N
    f.write(str(N) + " \n")

    # Print N lines
    for i in range(N):
        # Generate x_i, y_i (between 0 and 400)
        x_i = random.randint(50, 350)
        y_i = random.randint(50, 350)
        # Generate o_i, c_i (between 0 and 1440, o_i <= c_i)
        o_i = random.randint(0, 1000)
        c_i = random.randint(o_i + 200, 1440)
        # Generate u_i (between 0 and 27200)
        u_i = random.randint(1000, 10000)
        # Generate t_i
        t_i = random.randint(50, c_i-o_i)

        line = " ".join([str(x_i), str(y_i), str(o_i), str(c_i), str(u_i), str(t_i), "\n"])
        f.write(line)

generate_input(25, "small1.in")
generate_input(25, "small2.in")
generate_input(25, "small3.in")
generate_input(60, "medium1.in")
generate_input(60, "medium2.in")
generate_input(60, "medium3.in")
generate_input(200, "large1.in")
generate_input(200, "large2.in")
generate_input(200, "large3.in")

