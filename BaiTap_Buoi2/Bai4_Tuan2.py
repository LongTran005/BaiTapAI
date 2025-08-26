import math
x = float(input("Nhập x (radian): "))
epsilon = 1e-6
term = 1
cosx = term
n = 1
while abs(term) > epsilon:
    term *= -x**2 / ((2*n-1)*(2*n))
    cosx += term
    n += 1
print("cos(x) ≈", cosx)
print("cos(x) (math.cos) =", math.cos(x))
