# A stage one only implementation of ECM. Not for practical use


n = int(input("MOD(thing to factor):"))
acurve = int(input("a(0 for rand): "))
b = int(input("b(0 for rand): "))

baseP = [0, 0]
baseP[0] = (int(input("P_x(0 for rand):")) + n) % n
baseP[1] = (int(input("P_y(0 for rand):")) + n) % n
k = int(input("B1 of B1P:"))
userIterations = int(input("Iterations to do(-1 for forever):"))

print("")
print("")

#Calculates the extended euclidean aglorithm
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

#Returns the inverse of a number in mod m
#Upon failure, we have a factor.
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        
        print("After " + str(numIterations+1) + " iterations")
        print("Final Curve Params: a: " + str(acurve) + " b: " + str(b))
        print("With base point: x: " + str(baseP[0]) + " y: " + str(baseP[1]))
        print('p is: ' + str(g))
        print('q is: ' + str(n//g))
        print('n is: ' + str(g) + '*' + str(n//g))

        print("")
        exit()
        raise Exception('modular inverse does not exist')
    else:
        return x % m


#Calculates the slope of a single point added to itself
def calcSlope(p):
    top = 3*(p[0]**2) + acurve
    bottom = 2*p[1]
    if (top/bottom % 1 != 0):
        bottom = modinv((bottom +n)%n, n)
        return ((top * bottom)+n) % n
    else:
        return ((top//bottom)+n) % n

#Calculates the newX value from the slope and two points (or the same point for both params)
def newX(s, p, q):
    return(pow(s, 2, n) - p[0] - q[0])

#Calculates a new y value
def newY(s, p, newP):
    return((s*(p[0]-newP[0]))-p[1])

#Calculates the slope of two points in mod n
def calcSlope2(p, q):
    top = q[1] - p[1]
    bottom = q[0] - p[0]
    if (top/bottom % 1 != 0):
        bottom = modinv((bottom + n) %n, n)
        return ((top * bottom)+n) % n
    else:
        return ((top//bottom)+n) % n


from random import randint
from math import sqrt, ceil

zero = [0, 0]
firstRun = True
numIterations = 0
saveK = k

#Loop and compute new points and curves, attempt to compute kP and find a factor
while numIterations < userIterations or userIterations == -1:

    z = 1
    k = saveK

    #Generate new points and an a value
    if (baseP == zero or not firstRun):
        #random point
        baseP = [ceil(sqrt(n - randint(1, n-1))), ceil(sqrt(n - randint(1, n-1)))]

    if (acurve == 0 or not firstRun):
        #random a
        acurve = ceil(sqrt(n - randint(1, n-1)))

    #calc b so we have good curve
    b = pow(baseP[1], 2, n) - pow(baseP[0], 3, n) - (acurve * baseP[0])

    p = baseP
    results = []

    #Calculate powers of two of p
    while z <= k:
        s = calcSlope(p)
        newP = [0, 0]
        newP[0] = (newX(s, p, p) + n) %n
        newP[1] = (newY(s, p, newP) + n) %n   
        p = newP
        results.insert(0, (z, p))

        z = z + z

    curP = [0, 0]

    #Pull powers of 2 out of the k, add them together
    while k != 0:
        if results[0]:
            if k-results[0][0] >= 0:
                k = k - results[0][0]
                if (curP == zero):
                    curP = results[0][1]
                else:
                    s = calcSlope2(curP, results[0][1])
                    xnew = (newX(s, curP, results[0][1]) + n) %n
                    ynew = (newY(s, curP, [xnew]) + n) %n
                    curP[0] = xnew
                    curP[1] = ynew

            del results[0]
        else:
            break

    firstRun = False
    numIterations += 1



