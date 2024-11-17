from math import sin, cos, log, log10, tan, sqrt, e, pi
from collections import deque

class _Operation:
    NON = 100
    ADD = 86
    DIF = 85
    MULT = 66
    DIV = 65
    POW = 35
    SIN = 5
    COS = 6
    LG = 7
    LB = 8
    LN = 9
    TG = 10
    CTG = 11
    SQRT = 12

class _Part:
    def __init__(self, val, oper, is_x):
        self.val = val
        self.oper = oper
        self.is_x = is_x

class Function:
    function = None

    def __init__(self):
        self.__f = []

    def __is_operator(self, o):
        return o in  '+-*/^'

    def __get_func(self, func):
        func_map = {
            "cos": _Operation.COS, "ln": _Operation.LN, "lb": _Operation.LB,
            "lg": _Operation.LG, "tg": _Operation.TG, "ctg": _Operation.CTG,
            "sin": _Operation.SIN, "sqrt": _Operation.SQRT
        }
        res = func_map.get(func, _Operation.NON)
        if res == _Operation.NON:
            raise ValueError(f'Використано функцію, що не підтримується - {func}')
        return res

    def __get_priority(self, o):
        priority_map = {
            '+': _Operation.ADD, '-': _Operation.DIF,
            '*': _Operation.MULT, '/': _Operation.DIV, '^': _Operation.POW
        }
        return priority_map.get(o, _Operation.NON)

    def __make_binar_operation(self, a, oper, b):
        try:
            if oper == _Operation.ADD:
                return a + b
            elif oper == _Operation.DIF:
                return a - b
            elif oper == _Operation.MULT:
                return a * b
            elif oper == _Operation.DIV:
                return a / b
            elif oper == _Operation.POW:
                return a**b
        except:
            return float('nan')

    def __make_unar_operation(self, a, oper):
        try:
            if oper == _Operation.SIN:
                return sin(a)
            elif oper == _Operation.COS:
                return cos(a)
            elif oper == _Operation.LG:
                return log10(a)
            elif oper == _Operation.LN:
                return log(a)
            elif oper == _Operation.LB:
                return log(a, 2)
            elif oper == _Operation.TG:
                return tan(a)
            elif oper == _Operation.CTG:
                return cos(a) / sin(a)
            elif oper == _Operation.SQRT:
                return sqrt(a)
        except:
            return float('nan')

    def __parce(self, s):
        try:
            self.__f.clear()
            operation_mod = 100
            operators = deque()
            brackets = deque()
            cur_coef = 1e6
            cur_priority = 0
            temp = ""
            func = ""
            ind = 0
            for i, char in enumerate(s):
                if char == '(':
                    cur_coef -= operation_mod
                    brackets.append(i)
                    if temp:
                        func = temp
                        temp = ""
                elif char == ')':
                    cur_coef += operation_mod
                    if temp:
                        if temp != "x":
                            self.__f.append(_Part(float(temp), _Operation.NON, False))
                        else:
                            self.__f.append(_Part(0, _Operation.NON, True))
                        temp = ""
                    while operators and brackets[-1] < operators[-1][1]:
                        oper = operators.pop()[0] % operation_mod
                        self.__f.append(_Part(0, oper, False))
                    if func:
                        self.__f.append(_Part(0, self.__get_func(func), False))
                        func = ""
                    brackets.pop()
                elif self.__is_operator(char):
                    if temp:
                        if temp != "x":
                            self.__f.append(_Part(float(temp), _Operation.NON, False))
                        else:
                            self.__f.append(_Part(0, _Operation.NON, True))
                        temp = ""
                    cur_priority = self.__get_priority(char) + cur_coef
                    while operators and operators[-1][0] - operation_mod / 10 <= cur_priority:
                        oper = operators.pop()[0] % operation_mod
                        self.__f.append(_Part(0, oper, False))
                    operators.append((cur_priority, i))
                else:
                    temp += char

            while operators:
                oper = operators.pop()[0] % operation_mod
                self.__f.append(_Part(0, oper, False))
        except Exception as e:
            raise ValueError(e)

    def __get_value(self, value):
        try:
            val_stack = deque()
            for cur in self.__f:
                if cur.is_x:
                    val_stack.append(value)
                elif cur.oper == _Operation.NON:
                    val_stack.append(cur.val)
                elif cur.oper < 15:
                    if not val_stack:
                        return float('nan')
                    temp = val_stack.pop()
                    temp = self.__make_unar_operation(temp, cur.oper)
                    if temp != temp:
                        return float('nan')
                    val_stack.append(temp)
                else:
                    if not val_stack:
                        return float('nan')
                    temp = val_stack.pop()
                    if not val_stack:
                        return float('nan')
                    temp = self.__make_binar_operation(val_stack.pop(), cur.oper, temp)
                    val_stack.append(temp)
            return val_stack.pop() if val_stack else float('nan')
        except:
            return float('nan')

    def __make_beautiful(self, s):
        s = "(" + s + ")"
        s = s.replace(" ", "")
        temp = ""
        for i in range(len(s)):
            if s[i] in '-+' and s[i - 1] in '(+-*/^':
                temp += "0"
            if i > 0 and s[i] in '(xcltsep' and s[i - 1] in '0123456789)x':
                temp += "*"
            temp += s[i]
        s = temp
        s = s.replace("e", str(e))
        s = s.replace("pi", str(pi))
        return s

    def set_function(self, s):
        if not s:
            self.function = None
            return False
        self.__f = []
        self.function = self.__make_beautiful(s)
        try:
            self.__parce(self.function)
        except Exception as e:
            self.function = None
            raise ValueError(e)

    def __call__(self, value):
        if self.function == None:
            return float('nan')
        return self.__get_value(value)