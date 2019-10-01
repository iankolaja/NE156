from os import chdir, mkdir, system

d_radius = 0.01

def gen_input(isotope_name,isotope_ID,isotope_density,isotope_radius,reflector_ID = None,reflect_density=0,reflector_radius = 0, reflector_name = "water"):
    if reflector_ID == None:
        bReflector = False
        input_s = "Bare {0} sphere \n".format(isotope_name)
    else:
        bReflector = True
        input_s = "{0} sphere with {1} reflector\n".format(isotope_name,reflector_name)
    # Cells
    input_s += "1   1   -{0}   -1  tmp=2.530100E-08 imp:n=1  $ fis mat sphere\n".format(isotope_density)
    if bReflector:
        input_s += "2   2   -{0}  1 -2  tmp=2.530100E-08 imp:n=1 $ reflector mat\n".format(reflect_density)
        input_s += "3   0             2   imp:n=0  $ external\n"
    else:
        input_s += "3   0             1   imp:n=0  $ external\n"
    input_s += "\n"
    # Surfaces
    input_s += "1   so   {0}\n".format(isotope_radius)
    if bReflector:
        input_s += "2   so   {0}\n".format(isotope_radius+reflector_radius)
    input_s += "\n"
    # Materials
    input_s += "m1  {0} \n".format(isotope_ID)
    if bReflector:
        input_s += "m2  {0} \n".format(reflector_ID)     
    # Calc Params
    input_s += "kcode 3000 1. 100 300\n"
    input_s += "ksrc 0.0 0.0 0.0\n"
    input_s += "mode n\nc"
    return input_s

def parse_out(output_file):
    with open (output_file,"r") as f:
        for line in f:
            line = line.split()
            try:
                if line[5] == 'collision/absorption/track-length':
                    keff = float(line[8])
                    keffunc = float(line[15])
            except:
                pass
    return (keff, keffunc)

# Problem 1

fuel1_table = {"233U":["92233.70c 1.0","18.82",5.819,0,0],
    "235U":["92235.70c 1.0","18.82",8.41,0,0],
    "239Pu":["94239.70c 1.0","19.85",4.934,0,0],
    "241Pu":["94241.70c 1.0","19.85",5.39,0,0]}

try:
    chdir("P1")
except:
    mkdir("P1")
    chdir("P1")

for isotope in [*fuel1_table.items()]:
    isotope_name = isotope[0]
    isotope_ID = isotope[1][0]
    isotope_density = isotope[1][1]
    try:
        chdir(isotope_name)
    except:
        mkdir(isotope_name)
        chdir(isotope_name)
    radius = isotope[1][2]
    dkeff = 10000
    iters = 1
    while dkeff > 0.001:
        last_radius = radius
        input_s = gen_input(isotope_name,isotope_ID,isotope_density,radius)
        input_file = "iter{0}.inp".format(iters)
        output_file = "iter{0}.out".format(iters)
        print("Running {0} with radius {1}".format(isotope_name,radius))
        with open(input_file,'w') as f:
            f.write(input_s)
        system("mcnp6 n={0} o={1} tasks 10".format(input_file,output_file))
        (keff,keffunc) = parse_out(output_file)
        dkeff = abs(keff - 1.0000)
        if keff > 1.0:
            radius -= d_radius*0.6
        elif keff >= 0.97:
            radius += d_radius
        elif keff >= 0.8:
            radius += d_radius*5
        elif keff >= 0.5:
            radius += d_radius*15
        else:
            radius += d_radius*100
        iters += 1
    fuel1_table[isotope_name][2] = last_radius
    fuel1_table[isotope_name][3] = keff
    fuel1_table[isotope_name][4] = keffunc
    chdir('..')

chdir('..')

# Problem 2

try:
    chdir("P2")
except:
    mkdir("P2")
    chdir("P2")

fuel2_table = {"233U":["92233.70c 1.0","18.82",4.513,0,0],
    "235U":["92235.70c 1.0","18.82",6.474,0,0],
    "239Pu":["94239.70c 1.0","19.85",4.02,0,0],
    "241Pu":["94241.70c 1.0","19.85",4.16,0,0]}
reflector_ID = "1001.70c 2. 8016.70c 1. \nMT2 lwtr.20t"
reflect_density = 1.0
reflector_radius = 100

for isotope in [*fuel2_table.items()]:
    isotope_name = isotope[0]
    isotope_ID = isotope[1][0]
    isotope_density = isotope[1][1]
    try:
        chdir(isotope_name)
    except:
        mkdir(isotope_name)
        chdir(isotope_name)
    radius = isotope[1][2]
    dkeff = 10000
    iters = 1
    while dkeff > 0.001:
        last_radius = radius
        input_s = gen_input(isotope_name,isotope_ID,isotope_density,radius,reflector_ID,
            reflect_density,reflector_radius)
        input_file = "iter{0}.inp".format(iters)
        output_file = "iter{0}.out".format(iters)
        print("Running {0} with radius {1}".format(isotope_name,radius))
        with open(input_file,'w') as f:
            f.write(input_s)
        system("mcnp6 n={0} o={1} tasks 10".format(input_file,output_file))
        (keff,keffunc) = parse_out(output_file)
        dkeff = abs(keff - 1.0000)
        if keff > 1.0:
            radius -= d_radius*0.6
        elif keff >= 0.97:
            radius += d_radius
        elif keff >= 0.8:
            radius += d_radius*5
        elif keff >= 0.5:
            radius += d_radius*15
        else:
            radius += d_radius*100
        iters += 1
    fuel2_table[isotope_name][2] = last_radius
    fuel2_table[isotope_name][3] = keff
    fuel2_table[isotope_name][4] = keffunc
    chdir('..')


chdir('..')

# Problem 3


try:
    chdir("P3")
except:
    mkdir("P3")
    chdir("P3")

isotope = ("235U",["92235.70c 1.0","18.82",6.48,0,0])
reflector_ID = "1001.70c 2. 8016.70c 1. \nMT2 lwtr.20t"
reflect_density = 1.0
reflector_radii = [10,30,50,75,100,200]
critical_radii = [6.51,6.48,6.48,6.48,6.48,6.48]


for index in range(len(reflector_radii)):
    isotope_name = isotope[0]
    isotope_ID = isotope[1][0]
    isotope_density = isotope[1][1]
    reflector_radius = reflector_radii[index]
    try:
        chdir(str(reflector_radius)+"cm")
    except:
        mkdir(str(reflector_radius)+"cm")
        chdir(str(reflector_radius)+"cm")
    radius = isotope[1][2]
    dkeff = 10000
    iters = 1
    while dkeff > 0.001:
        last_radius = radius
        input_s = gen_input(isotope_name,isotope_ID,isotope_density,radius,reflector_ID,
            reflect_density,reflector_radius)
        input_file = "iter{0}.inp".format(iters)
        output_file = "iter{0}.out".format(iters)
        print("Running {0} with radius {1}".format(isotope_name,radius))
        with open(input_file,'w') as f:
            f.write(input_s)
        system("mcnp6 n={0} o={1} tasks 10".format(input_file,output_file))
        (keff,keffunc) = parse_out(output_file)
        dkeff = abs(keff - 1.0000)
        if keff > 1.0:
            radius -= d_radius*0.6
        elif keff >= 0.97:
            radius += d_radius
        elif keff >= 0.8:
            radius += d_radius*5
        elif keff >= 0.5:
            radius += d_radius*15
        else:
            radius += d_radius*100
        iters += 1
    critical_radii[index] = last_radius

    chdir('..')

chdir('..')

# Problem 4

try:
    chdir("P4")
except:
    mkdir("P4")
    chdir("P4")

reflector4_table = {"Water":["1001.70c 2. 8016.70c 1. \nMt2 lwtr.20t","1.0",6.474,0,0],
    "Heavy Water":["1002.70c 2. 8016.70c 1. \nMt2 hwtr.20t","1.1",5.552,0,0],
    "Beryllium":["4009.70c 1.0 \nMt2 be.20t","1.80",5.8,0,0],
    "Iron":["2656.70c -0.9175 2657.70c -0.0212 2654.70c -0.0585 \nMt2 fe56.22t","7.86",6.0,0,0],
    "Cadmium":["48110.70c -0.1247  48111.70c -0.1280  48112.70c -0.2411  48113.70c -0.1223  48114.70c -0.2875  48116.70c -0.0751","8.65",6.4,0,0],
    "U238":["92238.70c 1.0","18.82",5.8,0,0]}

isotope = ("235U",["92235.70c 1.0","18.82",6.48,0,0])
reflector_ID = "1001.70c 2. 8016.70c 1. \nMT2 lwtr.20t"
reflect_density = 1.0
reflector_radius = 100

for reflector in [*reflector4_table.items()]:
    reflector_name = reflector[0]
    reflector_ID = reflector[1][0]
    reflector_density = reflector[1][1]
    radius = reflector[1][2]
    try:
        chdir(reflector_name)
    except:
        mkdir(reflector_name)
        chdir(reflector_name)
    dkeff = 10000
    iters = 1
    while dkeff > 0.001:
        last_radius = radius
        input_s = gen_input(isotope_name,isotope_ID,isotope_density,radius,reflector_ID,
            reflect_density,reflector_radius)
        input_file = "iter{0}.inp".format(iters)
        output_file = "iter{0}.out".format(iters)
        print("Running {0} with radius {1}".format(isotope_name,radius))
        with open(input_file,'w') as f:
            f.write(input_s)
        system("mcnp6 n={0} o={1} tasks 10".format(input_file,output_file))
        (keff,keffunc) = parse_out(output_file)
        dkeff = abs(keff - 1.0000)
        if keff > 1.0:
            radius -= d_radius*0.6
        elif keff >= 0.97:
            radius += d_radius
        elif keff >= 0.8:
            radius += d_radius*5
        elif keff >= 0.5:
            radius += d_radius*15
        else:
            radius += d_radius*100
        iters += 1
    reflector4_table[reflector_name][2] = last_radius
    reflector4_table[reflector_name][3] = keff
    reflector4_table[reflector_name][4] = keffunc
    chdir('..')

chdir('..')




# Problem 5









# Results

print("Problem 1 answers:")
for isotope in [*fuel1_table.items()]:
    print("{0}: {1} [keff = {2} +- {3}".format(isotope[0],isotope[1][2],isotope[1][3],isotope[1][4]))
print("\n\n")

print("Problem 2 answers:")
for isotope in [*fuel2_table.items()]:
    print("{0}: {1} [keff = {2} +- {3}".format(isotope[0],isotope[1][2],isotope[1][3],isotope[1][4]))
print("\n\n")

print("Problem 3 answers:")
for index in range(len(reflector_radii)):
    print("{0}cm of water: {1}cm".format(reflector_radii[index],critical_radii[index]))
print("\n\n")

print("Problem 4 answers:")
for reflector in [*reflector4_table.items()]:
    print("{0}: {1} [keff = {2} +- {3}".format(reflector[0],reflector[1][2],reflector[1][3],reflector[1][4]))
print("\n\n")
