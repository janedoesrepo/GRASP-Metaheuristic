import numpy as np
from copy import deepcopy

# define processing times
t = [20, 25, 20, 43, 11, 72, 64, 3, 4]
n = '9'
mean = sum(t)/len(t)

# create cycle times
c = np.random.randint(75, 150, 10)

# create instances
instances1 = []
for i in range(10):
    instance = [i, c[i], t]
    instances1.append(instance)

# define settings
variances = [0.25, 0.75]
variants = [3, mean]

names = []
for i in range(1, 11):
    name1 = "FALLBEISPIEL.IN2_TS0.25_EJ" + str(i)
    name2 = "FALLBEISPIEL.IN2_TS0.25-med_EJ" + str(i)
    name3 = "FALLBEISPIEL.IN2_TS0.75_EJ" + str(i)
    name4 = "FALLBEISPIEL.IN2_TS0.75-med_EJ" + str(i)
    names.append(name1)
    names.append(name2)
    names.append(name3)
    names.append(name4)

# generate setup times
instances2 = []
for instance in instances1:
    for var in variances:
        for func in variants:
            a = 0                       # untere Intervallgrenze
            b = np.ceil(var * func)     # obere Intervallgrenze
            tsu = np.random.randint(a, b+1, (9, 9))
            for i in range(len(t)):
                for j in range(len(t)):
                    tsu[i][j] = int(tsu[i][j])
            instance2 = deepcopy(instance)
            instance2.append(tsu)
            instances2.append(instance2)

print('-'*25)
x = 0
for filename in names:
    with open(filename + ".txt", 'w') as file:
        instance = deepcopy(instances2[x])
        file.write('9\n')
        file.write('9\n')
        file.write(str(instance[1])+'\n')

        for j in range(len(t)):
            file.write(str(j) + ',' + str(t[j]) + '\n')

        file.writelines(["0,1\n", "0,2\n", "1,6\n", "2,6\n", "3,4\n", "4,6\n", "5,6\n", "6,7\n", "6,8\n"])

        item = instance[3]
        for i in range(9):
            string = ''
            for j in range(9):
                if j == 8 and i == 8:
                    string = string + '0'
                elif j == 8:
                    string = string + str(int(item[i][j])) + '\n'
                elif i == j:
                    string = string + '0' + ','
                else:
                    string = string + str(int(item[i][j])) + ','
            file.write(string)
    x += 1
