# encoding=utf-8
passline = 60


def func(val):
    passline = 90
    if val >= passline:
        print("pass")
    else:
        print("fail")
    def in_func():
        print(val)
    return in_func


def Max(val1, val2):
    # max is a built-in fun
    return max(val1, val2)

f = func(89)
f()
print(f.__closure__)
print(Max(90, 100))
