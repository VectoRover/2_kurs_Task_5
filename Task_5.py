import math
eps = 0.0000000001


def distance(dot1, dot2):
     a = dot1[0]-dot2[0]
     b = dot1[1]-dot2[1]
     return math.sqrt(a*a + b*b)


def obt_ang(dots):
    x1 = dots[0][0]
    x2 = dots[1][0]
    x3 = dots[2][0]
    y1 = dots[0][1]
    y2 = dots[1][1]
    y3 = dots[2][1]
    a = distance(dots[0], dots[1])
    b = distance(dots[0], dots[2])
    c = distance(dots[1], dots[2])
    lst = []
    lst.append((b**2 + c**2 - a**2)/(2*c*b))
    lst.append((a**2 + c**2 - b**2)/(2*a*c))
    lst.append((a**2 + b**2 - c**2)/(2*a*b))
    for i in range(3):
        if abs(lst[i]) < eps:
            lst[i] = 0
    if  lst[0] < 0:
        return [0.5*(x1+x2), 0.5*(y1+y2), 0.5*distance(dots[0], dots[1])]
    if  lst[1] < 0:
        return [0.5*(x1+x3), 0.5*(y1+y3), 0.5*distance(dots[0], dots[2])]
    if  lst[2] < 0:
        return [0.5*(x2+x3), 0.5*(y2+y3), 0.5*distance(dots[1], dots[2])]
    lst.clear()
    return lst


def xtrgl(dots):
    x1 = dots[0][0]
    x2 = dots[1][0]
    x3 = dots[2][0]
    y1 = dots[0][1]
    y2 = dots[1][1]
    y3 = dots[2][1]
    p = 2 * (y1 - y3) * (x2 - x1) + 2 * (x3 - x1) * (y2 - y1)
    q = (y1 - y3) * (x2 ** 2 - x1 ** 2 + y2 ** 2 - y1 ** 2) + (y2 - y1) * (x3 ** 2 - x1 ** 2 + y3 ** 2 - y1 ** 2)
    try:
        res = q / p
    except ZeroDivisionError:
        res = 0
        exit(-4)
    return res


def ytrgl(dots):
    x1 = dots[0][0]
    x2 = dots[1][0]
    x3 = dots[2][0]
    y1 = dots[0][1]
    y2 = dots[1][1]
    y3 = dots[2][1]
    p = 2 * (x1 - x3) * (y2 - y1) + 2 * (y3 - y1) * (x2 - x1)
    q = (x1 - x3) * (x2 ** 2 - x1 ** 2 + y2 ** 2 - y1 ** 2) + (x2 - x1) * (x3 ** 2 - x1 ** 2 + y3 ** 2 - y1 ** 2)
    try:
        res = q / p
    except ZeroDivisionError:
        res = 0
        exit(-5)
    return res


def calculator(dots, count):
    if count == 1:
        return [dots[0][0], dots[0][1], 0]
    if count == 2:
        return [(dots[0][0] + dots[1][0])*1/2, (dots[0][1] + dots[1][1])*1/2, 0.5*distance(dots[0], dots[1])]
    for i in range(count-1):
        if dots[0] == dots[i+1]:
            return [dots[0][0], dots[0][1], 0]
    if count == 3:
            x = xtrgl(dots)
            y = ytrgl(dots)
            r = distance(dots[0], [x, y])
            res = obt_ang(dots)
            if len(res) != 0:
                return res
            else:
                res.append(x)
                res.append(y)
                res.append(distance(dots[0], [x, y]))
                return res
    dots_1st = [dots[0], dots[1], dots[2]]
    x = xtrgl(dots)
    y = ytrgl(dots)
    r = distance(dots[0], [x, y])
    res = obt_ang(dots_1st)
    if len(res) != 0:
        x = res[0]
        y = res[1]
        r = res[2]
    for i in range(3, count):
        k = dots[i]
        d = distance(k, [x, y])
        if d == r:
            dots_1st.append(k)
        if d > r:
            dot_a = []
            dot_b = []
            for p in range(len(dots_1st)):
                dot_a.append(distance(k, dots_1st[p]))
            ind_1 = dot_a.index(max(dot_a))
            for q in range(len(dots_1st)):
                dot_b.append(distance(k, dots_1st[q]) + distance(dots_1st[ind_1], dots_1st[q]))
            ind_2 = dot_b.index(max(dot_b))
            dots_1st.clear()
            dots_1st.append(k)
            dots_1st.append(dots[ind_1])
            dots_1st.append(dots[ind_2])
            x = xtrgl(dots_1st)
            y = ytrgl(dots_1st)
            r = distance(dots_1st[0], [x, y])

            for k in range(len(dots_1st)):
                if k != i and k != ind_1 and k != ind_2:
                    if distance(dots[k], [x, y]) == r:
                        dots_1st.append(dots[k])
    res = obt_ang(dots_1st)
    if len(res) != 0:
        return res
    else:
        res.append(x)
        res.append(y)
        res.append(r)
        return res


def autotest():
    a = [[-1, 1], [1, 1], [1, -1], [-1, -1]]
    b = [[-1000, 0], [0, 2], [1000, 0]]
    c = [[0, 2], [2, 0], [2, 2], [0, 0]]
    res1 = calculator(a, len(a))
    res2 = calculator(b, len(b))
    res3 = calculator(c, len(c))
    fl1 = True
    fl2 = True
    fl3 = True
    if res1[0] != 0 or res1[1] != 0 or abs(res1[2] - math.sqrt(2)) > eps:
        fl1 = False
    if res2[0] != 0 or res2[1] != 0 or abs(res2[2] - 1000) > eps:
        fl2 = False
    if res3[0] != 1 or res3[1] != 1 or abs(res3[2] - math.sqrt(2)) > eps:
        fl3 = False

    if fl1 == False or fl2 == False or fl3 == False:
        print("Автотест провален")
    else:
        print("Автотест сдан")


autotest()
try:
    count = int(input("Введите количество точек: "))
except ValueError:
    print("Вы ввели некорректные данные")
    exit(-2)
if count <= 0:
    print("Вы ввели некорректное значение")
    exit(-1)
dots = []
for i in range (count):
    print("Ввод", i + 1, "-й точки")
    try:
        a = float(input("Введите абсциссу: "))
        b = float(input("Введите ординату: "))
    except ValueError:
        print("Вы ввели некорректные данные")
        exit(-3)
    dots.append([a, b])
res = calculator(dots, count)
print("Координаты центра: (",res[0],",",res[1], ") R =", f'{res[2]:.3f}')

