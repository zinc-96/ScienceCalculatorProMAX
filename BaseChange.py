# 字母与数字相互转换
def trans(num) -> str | int:
    if type(num) == int:
        if num < 10:
            return str(num)
        else:
            return chr(ord('A') + num - 10)
    else:
        if num.isdigit():
            return int(num)
        else:
            return ord(num) - ord('A') + 10


# 检查输入是否有误
def Check(num, base: int, target: int) -> bool | str:
    if type(base) is not int or base < 2 or base > 36 or type(target) is not int or target < 2 or target > 36:
        print('非法进制数！')
        return False
    if type(num) is int or type(num) is float:
        num = str(num).upper()
    elif type(num) is str and len(num) != 0:
        num = num.upper()
    else:
        print('非数字输入！')
        return False

    if num.count('.') > 1:
        print('多个小数点！')
        return False

    if not num.replace('.', '').isalnum():
        print('含有其他字符！')
        return False

    for c in num.replace('.', ''):
        if trans(c) >= base:
            print('字符超过进制允许！')
            return False

    while len(num) > 1:
        if num[0] == '0' and num[1] != '.':
            num = num[1:]
        else:
            break
    return num


# 待转换数字，当前进制，目标进制，精度
def BaseChange(num, base: int, target: int, precision=100) -> str | None:
    if (len(num) == 2 and num[0] == '-' and num[1] == '0'):
        return "0"
    isfu = (num[0] == '-')
    if isfu:
        num = num[1:]
    num = Check(num, base, target)
    if num is False:
        return None
    point = num.find('.')
    if point == -1:
        point = len(num)
    radix = num.replace('.', '')
    if target == 10:
        int_part = radix[:point][::-1]
        frac_part = radix[point:]
        s = 0
        ss = 0
        for i in range(len(int_part)):
            s += trans(int_part[i]) * base ** i
        for i in range(len(frac_part)):
            ss += trans(frac_part[i]) / base ** (i + 1)
        return isfu * "-" + str(s) + str(ss)[1:]
    elif base == 10:
        int_part = int(radix[:point])
        frac_part = float('0.' + radix[point:])
        s = ''
        while True:
            s += trans(int_part % target)
            int_part //= target
            if int_part == 0:
                break
        s = s[::-1]
        if frac_part != 0:
            s += '.'
            ct = 0
            while frac_part != 0 and ct < precision:
                frac_part *= target
                s += trans(int(frac_part))
                frac_part -= int(frac_part)
                ct += 1
        return isfu * "-" + s
    else:
        return BaseChange(BaseChange(num, base, 10, precision=precision), 10, target, precision=precision)
