#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

# Шаблон для домашнѣго задания
# Рѣализуйте мѣтоды с raise NotImplementedError


class Scope:

    """Scope - представляет доступ к значениям по именам
    (к функциям и именованным константам).
    Scope может иметь родителя, и если поиск по имени
    в текущем Scope не успешен, то если у Scope есть родитель,
    то поиск делегируется родителю.
    Scope должен поддерживать dict-like интерфейс доступа
    (см. на специальные функции __getitem__ и __setitem__)
    """

    def __init__(self, parent=None):
        self.dic = {}
        self.parent = parent

    def __getitem__(self, key):
        if key in self.dic:
            return self.dic[key]
        elif self.parent:
            return self.parent[key]

    def __setitem__(self, key, value):
        self.dic[key] = value


class Number:

    """Number - представляет число в программе.
    Все числа в нашем языке целые."""

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:

    """Function - представляет функцию в программе.
    Функция - второй тип поддерживаемый языком.
    Функции можно передавать в другие функции,
    и возвращать из функций.
    Функция состоит из тела и списка имен аргументов.
    Тело функции это список выражений,
    т. е.  у каждого из них есть метод evaluate.
    Во время вычисления функции (метод evaluate),
    все объекты тела функции вычисляются последовательно,
    и результат вычисления последнего из них
    является результатом вычисления функции.
    Список имен аргументов - список имен
    формальных параметров функции."""

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        res = Number(0)
        for expr in self.body:
            res = expr.evaluate(scope)
        return res


class FunctionDefinition:

    """FunctionDefinition - представляет определение функции,
    т. е. связывает некоторое имя с объектом Function.
    Результатом вычисления FunctionDefinition является
    обновление текущего Scope - в него
    добавляется новое значение типа Function."""

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    """
    Conditional - представляет ветвление в программе, т. е. if.
    """

    def __init__(self, condtion, if_true, if_false=None):
        self.condition = condtion
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        cond = self.condition.evaluate(scope)
        res = Number(0)
        if cond.value:
            expr = self.if_true
        else:
            expr = self.if_false
        if expr:
            for term in expr:
                res = term.evaluate(scope)
            return res
        else:
            return Number(0)


class Print:

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        print(res.value)
        return res


class Read:

    """Read - читает число из стандартного потока ввода
     и обновляет текущий Scope.
     Каждое входное число располагается на отдельной строке
     (никаких пустых строк и лишних символов не будет).
     """

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        inp = int(input())
        scope[self.name] = Number(inp)
        return Number(inp)


class FunctionCall:

    """
    FunctionCall - представляет вызов функции в программе.
    В результате вызова функции должен создаваться новый объект Scope,
    являющий дочерним для текущего Scope
    (т. е. текущий Scope должен стать для него родителем).
    Новый Scope станет текущим Scope-ом при вычислении тела функции.
    """

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for name, arg in zip(function.args, self.args):
            call_scope[name] = arg.evaluate(scope)
        return function.evaluate(call_scope)


class Reference:

    """Reference - получение объекта
    (функции или переменной) по его имени."""

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    """BinaryOperation - представляет бинарную операцию над двумя выражениями.
    Результатом вычисления бинарной операции является объект Number.
    Поддерживаемые операции:
    “+”, “-”, “*”, “/”, “%”, “==”, “!=”,
    “<”, “>”, “<=”, “>=”, “&&”, “||”."""
    operation = {'+': lambda x, y: x.value + y.value,
                 '-': lambda x, y: x.value - y.value,
                 '*': lambda x, y: x.value * y.value,
                 '/': lambda x, y: x.value // y.value,
                 '%': lambda x, y: x.value % y.value,
                 '==': lambda x, y: int(x.value == y.value),
                 '!=': lambda x, y: int(x.value != y.value),
                 '<': lambda x, y: int(x.value < y.value),
                 '<=': lambda x, y: int(x.value <= y.value),
                 '>=': lambda x, y: int(x.value >= y.value),
                 '>': lambda x, y: int(x.value > y.value),
                 '&&': lambda x, y: int(x.value and y.value),
                 '||': lambda x, y: int(x.value or y.value)}

    def __init__(self, lhs, op, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, scope):
        left = self.lhs.evaluate(scope)
        right = self.rhs.evaluate(scope)
        return Number(self.operation[self.op](left, right))


class UnaryOperation:

    """UnaryOperation - представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: “-”, “!”."""
    operation = {'-': lambda x: -x.value,
                 '!': lambda x: int(not x.value)}

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        return Number(self.operation[self.op](self.expr.evaluate(scope)))
