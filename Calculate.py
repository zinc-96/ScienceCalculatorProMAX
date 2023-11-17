'''
计算模块
设计模式：策略模式、桥接模式
功能：计算格式化算式
'''
from decimal import Decimal, getcontext
from math import *

'''
计算策略
'''


class CalculateStrategy(object):
    def __init__(self, a: str | list = None, b: str|list = '') -> None:
        self.num1 = a
        self.num2 = b

    def calculate(self):
        pass


# 加
class Add(CalculateStrategy):
    def calculate(self) -> float | list:
        if type(self.num1) == list:
            self.num1 = BigNum(self.num1)
            self.num2 = BigNum(self.num2)
            sign=[0,0]
            X = self.num1.calculate()[2] - self.num1.calculate()[1] + self.num2.calculate()[2]
            if X>=0:
                sign[1]=1
            else:
                X = X + self.num1.calculate()[1]
            Y = self.num1.calculate()[0] - self.num1.calculate()[1] + self.num2.calculate()[0] + sign[1]
            if Y>=0:
                sign[0]=1
            else:
                Y = Y + self.num1.calculate()[1]
            if sign[0] == 1:
                return ['1',
                        str(Y),
                        str(X),
                        str(self.num1.calculate()[1])]
            else:
                return [str(Y),
                        str(X),
                        str(self.num1.calculate()[1])]
        else:
            self.num1 = SmallNum(self.num1)
            self.num2 = SmallNum(self.num2)
            return self.num1.calculate() + self.num2.calculate()


# 减
class Minus(CalculateStrategy):
    def calculate(self) -> float | list:
        if type(self.num1) == list:
            self.num1 = BigNum(self.num1)
            self.num2 = BigNum(self.num2)
            sign = [0,0]
            X = self.num1.calculate()[2] - self.num2.calculate()[2]
            if X < 0:
                sign[1] = 1
                X = X + self.num1.calculate()[1]
            Y = self.num1.calculate()[0] - self.num2.calculate()[0] - sign[1]
            if Y < 0:
                sign[0] = 1
                Y = Y + self.num1.calculate()[1]
            if sign[0] == 1:
                return ['-1',
                        str(Y),
                        str(X),
                        str(self.num1.calculate()[1])]
            else:
                return [str(Y),
                        str(X),
                        str(self.num1.calculate()[1])]
        else:
            self.num1 = SmallNum(self.num1)
            self.num2 = SmallNum(self.num2)
            return self.num1.calculate() - self.num2.calculate()


# 乘
class Mul(CalculateStrategy):
    def calculate(self) -> float | list:
        if type(self.num1) == list:
            self.num1 = BigNum(self.num1)
            self.num2 = BigNum(self.num2)
            sign = [0,0,0]
            X = self.num1.calculate()[2] * self.num2.calculate()[2]
            if X > self.num1.calculate()[1]:
                sign[2] = X // self.num1.calculate()[1]
                X = X % self.num1.calculate()[1]
            Y = self.num1.calculate()[0]*self.num2.calculate()[2]+self.num1.calculate()[2]*self.num2.calculate()[0]+sign[2]
            if Y > self.num1.calculate()[1]:
                sign[1] = Y // self.num1.calculate()[1]
                Y = Y % self.num1.calculate()[1]
            Z = self.num1.calculate()[0]*self.num2.calculate()[0]+sign[1]
            if Z > self.num1.calculate()[1]:
                sign[0] = Z // self.num1.calculate()[1]
                Z = Z % self.num1.calculate()[1]
            if sign[0]!=0:
                return [str(sign[0]),
                        str(Z),
                        str(Y),
                        str(X),
                        str(self.num1.calculate()[1])]
            else:
                return [str(Z),
                        str(Y),
                        str(X),
                        str(self.num1.calculate()[1])]
        else:
            self.num1 = SmallNum(self.num1)
            self.num2 = SmallNum(self.num2)
            return self.num1.calculate() * self.num2.calculate()


# 除
class Div(CalculateStrategy):
    def calculate(self) -> float:
        self.num1 = SmallNum(self.num1)
        self.num2 = SmallNum(self.num2)
        return self.num1.calculate() / self.num2.calculate()


# 取余
class Mod(CalculateStrategy):
    def calculate(self) -> float:
        self.num1 = SmallNum(self.num1)
        self.num2 = SmallNum(self.num2)
        return self.num1.calculate() % self.num2.calculate()


# 幂
class Pow(CalculateStrategy):
    def calculate(self) -> float:
        self.num1 = SmallNum(self.num1)
        self.num2 = SmallNum(self.num2)
        return (-1 if self.num1.calculate() < 0 else 1) * abs(self.num1.calculate() ** self.num2.calculate())


# 根
class Root(CalculateStrategy):
    def calculate(self) -> float:
        self.num1 = SmallNum(self.num1)
        return sqrt(self.num1.calculate())


# sin
class Sin(CalculateStrategy):
    def calculate(self) -> float:
        self.num1 = SmallNum(self.num1)
        return sin(self.num1.calculate())


# arcsin
class Arcsin(CalculateStrategy):
    def calculate(self) -> float:
        self.num1 = SmallNum(self.num1)
        return asin(self.num1.calculate())


# 对数
class Ln(CalculateStrategy):
    def calculate(self) -> float:
        self.num1 = SmallNum(self.num1)
        return log(self.num1.calculate())


class CalculateInterface(object):
    def __init__(self, calculate_strategy: CalculateStrategy) -> None:
        self._calculate_strategy = calculate_strategy

    @property
    def calculate_strategy(self) -> CalculateStrategy:
        return self._calculate_strategy

    @calculate_strategy.setter
    def calculate_strategy(self, calculate_strategy: CalculateStrategy) -> None:
        self._calculate_strategy = calculate_strategy

    def calculate(self, op, a, b=None):
        match op:
            case '+':
                self.calculate_strategy = Add()
            case '-':
                self.calculate_strategy = Minus()
            case '*':
                self.calculate_strategy = Mul()
            case '/':
                self.calculate_strategy = Div()
            case '%':
                self.calculate_strategy = Mod()
            case '^':
                self.calculate_strategy = Pow()
            case '√':
                self.calculate_strategy = Root()
            case 'sin':
                self.calculate_strategy = Sin()
            case 'arcsin':
                self.calculate_strategy = Arcsin()
            case 'ln':
                self.calculate_strategy = Ln()
        self.calculate_strategy.__init__(a, b)
        return self.calculate_strategy.calculate()


'''
数字类型
'''


class AbstractNum(CalculateStrategy):
    def calculate(self):
        return self.num


class SmallNum(AbstractNum):
    def __init__(self, a: str = '') -> None:
        self.num = float(a)


class BigNum(AbstractNum):
    def __init__(self, a: list = []) -> None:
        self.num = [Decimal(a[0]),Decimal(a[1]),Decimal(a[2])]



# 运算符:优先级，越大越高
opers_rate = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '^': 3,
    '√': 3,
    'sin': 3,
    'arcsin': 3,
    'ln': 3,
    '(': 4,
    ')': 5
}


# 比较连续两个运算符来判断是压栈还是弹栈
def decision(tail_op, now_op):
    # return: 1代表弹栈运算，0代表弹出运算符栈最后一个元素'('，-1表示压栈
    match opers_rate[tail_op]:
        case 1:
            return -1 if opers_rate[now_op] in [2, 3, 4] else 1
        case 2:
            return -1 if opers_rate[now_op] in [3, 4] else 1
        case 3:
            return -1 if opers_rate[now_op] == 4 else 1
        case 4:
            return 0 if opers_rate[now_op] == 5 else -1


# 负责遍历算式列表中的字符，决定压入数字栈中或压入运算符栈中或弹栈运算
def Calculate(formula_list:list=None,precision=None,mode=None):
    calculateinterface = CalculateInterface(CalculateStrategy())
    if mode == 1:
        getcontext().prec = precision
        num_stack = []  # 数字栈
        op_stack = []  # 运算符栈
        for item in formula_list:
            if item not in opers_rate:
                match item:
                    case 'π':
                        num_stack.append(pi)
                    case '-π':
                        num_stack.append(-pi)
                    case 'e':
                        num_stack.append(e)
                    case '-e':
                        num_stack.append(-e)
                    case _:
                        num_stack.append(str(item))
            else:
                while True:
                    # 如果运算符栈为空，则无条件入栈
                    if len(op_stack) == 0:
                        op_stack.append(item)
                        break
                    # 决定压栈或弹栈
                    tag = decision(op_stack[-1], item)
                    # 如果是-1，则压入运算符栈并进入下一次循环
                    if tag == -1:
                        op_stack.append(item)
                        break
                    # 如果是0，则弹出运算符栈内最后一个'('并丢掉当前')'，进入下一次循环
                    elif tag == 0:
                        op_stack.pop()
                        # '('前是'√'、'sin'、'arcsin'、'ln'时，对括号内算式的计算结果作相应的运算
                        if op_stack[-1] in ['√', 'sin', 'arcsin', 'ln']:
                            num_stack.append(calculateinterface.calculate(op_stack.pop(), num_stack.pop()))
                        break
                    # 如果是1，则弹出运算符栈内最后一个元素和数字栈内最后两个元素
                    elif tag == 1:
                        if item in ['√', 'sin', 'arcsin']:
                            op_stack.append(item)
                            break
                        # 将计算结果压入数字栈并接着循环，直到遇到break跳出循环
                        num_stack.append(calculateinterface.calculate(op_stack.pop(), num_stack.pop(-2), num_stack.pop()))
        # 大循环结束后，数字栈和运算符栈中可能还有元素的情况
        while len(op_stack) != 0:
            num_stack.append(str(calculateinterface.calculate(op_stack.pop(), num_stack.pop(-2), num_stack.pop())))
        result = str(num_stack[0])
        # 去掉无效的0和小数点，例：1.0转换为1
        return result[0:-2] if result[len(result) - 1] == '0' and result[len(result) - 2] == '.' else result
    elif mode in [2, 3]:
        getcontext().prec=len(formula_list[4]) * 2
        return calculateinterface.calculate(formula_list[5],
                                        [formula_list[0],formula_list[4],formula_list[1]],
                                        [formula_list[2],formula_list[4],formula_list[3]])