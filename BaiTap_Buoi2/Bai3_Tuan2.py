import math
heso = list(map(float, input("Nhập hệ số (2 để giải pt bậc 1 và 3 để giải pt bậc 2): ").split()))
if len(heso) == 2:
    a = heso[0]
    b = heso[1]
    if a == 0:
        if b == 0:
            print("Phương trình vô số nghiệm")
        else:
            print("Phương trình vô nghiệm")
    else:
        print("Nghiệm của phương trình bậc 1 là:", -b / a)
elif len(heso) == 3:
    a = heso[0]
    b = heso[1]
    c = heso[2]
    if a == 0:
        if b == 0:
            if c == 0:
                print("Phương trình vô số nghiệm")
            else:
                print("Phương trình vô nghiệm")
        else:
            print("Nghiệm của phương trình là:", -c / b)
    else:
        delta = b ** 2 - 4 * a * c
        if delta < 0:
            print("Phương trình vô nghiệm")
        elif delta == 0:
            print("Phương trình có nghiệm kép:", -b / (2 * a))
        else:
            x1 = (-b + math.sqrt(delta)) / (2 * a)
            x2 = (-b - math.sqrt(delta)) / (2 * a)
            print("Phương trình có 2 nghiệm:", x1, x2)
else:
    print("Phải nhập 2 hoặc 3 hệ số")