from math import sin, cos, log, log10, tan, sqrt, e, pi
from collections import deque

class Function:
    class _Operation:
        NON = 100
        _SAMEPRIORITYRANGE = 10
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
        RETURNER = 13

    class _Error(Exception):
        FUNC = f'Викликається функція без аргументів.'
        BINAROPERATION = f"Виконується операція без достатньої кількості операндів."
        BADFUNC = "Функцію задано не коректно."
    function = None
    oper_map = {
        _Operation.COS : "cos", _Operation.LN : "ln", _Operation.LB : "lb",
        _Operation.LG : "lg", _Operation.TG : "tg", _Operation.CTG : "ctg",
        _Operation.SIN : "sin", _Operation.SQRT : "sqrt", _Operation.RETURNER : "",
        _Operation.ADD : "+", _Operation.DIF : "-", 
        _Operation.DIV : "/", _Operation.MULT : "*", _Operation.POW : "^"
    }

    func_map = {
        "cos": _Operation.COS, "ln": _Operation.LN, "lb": _Operation.LB,
        "lg": _Operation.LG, "tg": _Operation.TG, "ctg": _Operation.CTG,
        "sin": _Operation.SIN, "sqrt": _Operation.SQRT, "": _Operation.RETURNER,
        '+': _Operation.ADD, '-': _Operation.DIF,
        '*': _Operation.MULT, '/': _Operation.DIV, '^': _Operation.POW
    }
    def __init__(self):
        self.__f = []

    def get_rpn(self):
        if self.function:
            s = ''
            for el in self.__f:
                if type(el) is str:
                    s += el
                elif type(el) is float:
                    s += str(el)
                else:
                    s += self.oper_map.get(el)
                s += ' '
            return s

    def __is_operator(self, o):
        return o in  '+-*/^'

    def __less_or_same_priority(self, a, b):
        return a < b + self._Operation._SAMEPRIORITYRANGE

    def __get_func(self, func):
        res = self.func_map.get(func, self._Operation.NON)
        if res == self._Operation.NON:
            raise ValueError(f'Використано функцію, що не підтримується - {func}')
        return res

    def __make_binar_operation(self, a, oper, b):
        try:
            if oper == self._Operation.ADD:
                return a + b
            elif oper == self._Operation.DIF:
                return a - b
            elif oper == self._Operation.MULT:
                return a * b
            elif oper == self._Operation.DIV:
                return a / b
            elif oper == self._Operation.POW:
                return a**b
        except:
            return float('nan')

    def __make_unar_operation(self, a, oper):
        try:
            if oper == self._Operation.SIN:
                return sin(a)
            elif oper == self._Operation.COS:
                return cos(a)
            elif oper == self._Operation.LG:
                return log10(a)
            elif oper == self._Operation.LN:
                return log(a)
            elif oper == self._Operation.LB:
                return log(a, 2)
            elif oper == self._Operation.TG:
                return tan(a)
            elif oper == self._Operation.CTG:
                return cos(a) / sin(a)
            elif oper == self._Operation.SQRT:
                return sqrt(a)
        except:
            return float('nan')

    def __parce(self, s):
        try:
            self.__f.clear()
            operators = deque()
            func = deque()
            temp = ""
            for char in s:
                if char == '(':
                    operators.append('(')
                    func.append(self.__get_func(temp))
                    temp = ""
                elif char == ')':
                    if temp:
                        if temp == "x":
                            self.__f.append(temp)
                        else:
                            self.__f.append(float(temp))
                        temp = ""
                    while operators and operators[-1] != '(':
                        self.__f.append(operators.pop())
                    if func[-1] != self._Operation.RETURNER:
                        self.__f.append(func.pop())
                    else:
                        func.pop()
                    operators.pop()
                elif self.__is_operator(char):
                    if temp:
                        if temp == "x":
                            self.__f.append(temp)
                        else:
                            self.__f.append(float(temp))
                        temp = ""
                    cur_operator = self.__get_func(char)
                    while operators and operators[-1] != '(' and self.__less_or_same_priority(operators[-1], cur_operator):
                        self.__f.append(operators.pop())
                    operators.append(cur_operator)
                else:
                    temp += char
        except:
            raise self._Error(self._Error.BADFUNC)

    def __get_value(self, value):
        try:
            val_stack = deque()
            for cur in self.__f:
                if cur == "x":
                    val_stack.append(value)
                elif type(cur) is float:
                    val_stack.append(cur)
                elif cur < 15:
                    if not val_stack:
                        raise self._Error(self._Error.FUNC)
                    val_stack.append(self.__make_unar_operation(val_stack.pop(), cur))
                else:
                    if not len(val_stack) > 1:
                        raise self._Error(self._Error.BINAROPERATION)
                    b, a = val_stack.pop(), val_stack.pop()
                    val_stack.append(self.__make_binar_operation(a, cur, b))
            if val_stack:
                return val_stack.pop()
            raise self._Error(self._Error.BADFUNC)
        except self._Error as e:
            self.function = None
            raise e
        except Exception as e:
            return float('nan')

    def __make_beautiful(self, s):
        s = "(" + s + ")"
        s = s.replace(" ", "")
        temp = ""
        for i in range(len(s)):
            if s[i] in '-+' and s[i - 1] in '(':
                temp += "0"
            if i > 0 and s[i] in '(xcltsep' and s[i - 1] in '0123456789)x':
                temp += "*"
            temp += s[i]
        s = temp
        s = s.replace("e", str(e))
        s = s.replace("pi", str(pi))
        return s

    def set_function(self, s):
        self.__f = []
        self.function = self.__make_beautiful(s)
        try:
            self.__parce(self.function)
        except self._Error as e:
            self.function = None
            raise e
    
    def __call__(self, value):
        if self.function == None:
            raise self._Error.BADFUNC
        return self.__get_value(value)