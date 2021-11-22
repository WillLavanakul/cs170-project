import random

file = open("100.in","r+")
file.truncate(0)

n = random.randint(76, 100)
file.write(str(n) + "\n")
for i in range(1, n+1):
    file.write(str(i) + " " + str(random.randint(1, 1440)) + " " + str(random.randint(1, 60)) + " " +  str(round(random.uniform(1, 99), 3)) + "\n")
file.close()

file = open("150.in","r+")
file.truncate(0)

n = random.randint(101, 150)
file.write(str(n) + "\n")
for i in range(1, n+1):
    file.write(str(i) + " " + str(random.randint(1, 1440)) + " " + str(random.randint(1, 60)) + " " +  str(round(random.uniform(1, 99), 3)) + "\n")
file.close()

file = open("200.in","r+")
file.truncate(0)

n = random.randint(151, 200)
file.write(str(n) + "\n")
for i in range(1, n+1):
    file.write(str(i) + " " + str(random.randint(1, 1440)) + " " + str(random.randint(1, 60)) + " " +  str(round(random.uniform(1, 99), 3)) + "\n")
file.close()