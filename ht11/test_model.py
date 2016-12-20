from model import *
#import pytest
import sys
from io import StringIO


input_values = list(range(-10, 10))  + [2342357715824, -1238979180023, -12157982649]

def get_value(num):
    old = sys.stdout 
    sys.stdout = StringIO()
    Print(num).evaluate(None)
    res = int(sys.stdout.getvalue())
    sys.stout = old
    return res    


def make_scope(scope, d):
    for key, value in d.items():
        scope[key] = value


def check_scope(scope, d):
    for key, value in d.items():
        if (scope[key] == None):
            assert scope[key] == value
        elif (isinstance(scope[key], Number)):
            assert get_value(scope[key]) == value
        else:
            assert isinstance(scope[key], Function)


def check_number(res, ans):
    assert isinstance(res, Number)
    assert get_value(res) == ans


class TestNumber:
    
    def test_number(self):
        for num in input_values:
            check_number(Number(num), num)

class TestPrint:
    
    def test_print(self):
        old = sys.stdout 
        for num in input_values:
            sys.stdout = StringIO()
            res = Print(Number(num)).evaluate(None)
            assert sys.stdout.getvalue() == (str(num) + '\n') 
            check_number(res, num)
            sys.stout = old
    
    
class TestScope:
    
    def test_scope(self):
        parent_scope = Scope()            
        make_scope(parent_scope, {"1" : Number(0), "var" : Number(5)})
        check_scope(parent_scope, {"1" : 0, "var" : 5, "0" : None})

        scope1 = Scope(parent_scope)
        make_scope(scope1, {"1" : Number(2), "0" : Number(4)})
        check_scope(scope1, {"1" : 2, "var" : 5, "0" : 4, "3" : None})    

        scope2 = Scope(parent_scope)
        make_scope(scope2, {"3" : Number(0)})
        check_scope(scope2, {"1" : 0, "var" : 5, "0" : None, "3" : 0, "7" : None})

        child_scope = Scope(scope1)
        make_scope(scope1, {"1" : Number(-11), "3" : Number(7), "12" : Number(10)})
        check_scope(scope1, {"1" : -11, "var" : 5, "3" : 7, "0" : 4, "12" : 10, "7" : None})   
            

class TestRead:

    def test_read(self):
        old = sys.stdin
        scope = Scope()
        input_scope = {"a" : 0, "b" : 1, "c" : -3, "a" : 4, "b" : 5, "a" : -8}
        actual_scope = {}
        for key, value in input_scope.items():
            actual_scope[key] = value
            sys.stdin = StringIO(str(value))
            res = Read(key).evaluate(scope)        
            check_number(res, value)
            check_scope(scope, actual_scope)
            sys.stdin = old


class TestReference:

    def test_reference(self):
        scope = Scope()
        input_scope = {'var1' : Number(1), "a" : Number(0), 'er' : Number(15), "foo" : Function([], [])}
        make_scope(scope, input_scope)        
        for key, value in input_scope.items():
            res = Reference(key).evaluate(scope)
            assert type(res) == type(value)
            if isinstance(res, Number):
                assert get_value(res) == get_value(value)
    

class TestBinary:

    op_dict = {'+':  lambda x, y: x + y,   '-': lambda x, y: x - y,
                    '*':  lambda x, y: x * y,   '/': lambda x, y: x // y,
                    '%':  lambda x, y: x % y,  '==': lambda x, y: x == y,
                    '!=': lambda x, y: x != y,  '>': lambda x, y: x > y,
                    '<':  lambda x, y: x < y,  '>=': lambda x, y: x >= y,
                    '<=': lambda x, y: x <= y, '&&': lambda x, y: bool(x) * bool(y),
                    '||': lambda x, y: bool(x) + bool(y)}
    
    def test_binary_evaluate(self):
        for op in self.op_dict.keys():
            for l in input_values:
                for r in input_values:
                    if (r == 0 and (op == '/' or op == '%')):
                        continue
                    res = BinaryOperation(Number(l), op, Number(r)).evaluate(None)
                    check_number(res, self.op_dict[op](l, r))

    def test_binary_comp(self):
        left = BinaryOperation(Number(4), '*', Number(5))
        right = BinaryOperation(Number(1), '+', Number(29))
        res = BinaryOperation(left, '-', right).evaluate(None)
        check_number(res, -10)


class TestUnary:

    op_dict = {'-': lambda x: -x, '!': lambda x: not(x)}

    def test_unary_evaluate(self):
        for op in self.op_dict.keys():
            for val in input_values:
                res = UnaryOperation(op, Number(val)).evaluate(None)
                check_number(res, self.op_dict[op](val))
    
    def test_unary_comp(self):
        expr = UnaryOperation('-', Number(5))
        res = UnaryOperation('-', expr).evaluate(None)
        check_number(res, 5)
    
class TestFunction:

    def test_function_no_args(self):   
        body = [BinaryOperation(Number(5), '+', Number(5))]
        foo = Function([], body)
        res = foo.evaluate(None)
        check_number(res, 10)
    
    def test_funcvtion_empty(self):
        foo = Function([], [])
        res = foo.evaluate(None)
        
    def test_function_empty_with_args(self):
        scope = Scope()
        make_scope(scope, {'a' : Number(1), 'b' : Number(2)})
        foo = Function(['a', 'b'], [])
        res = foo.evaluate(scope)    
    
    def test_function(self):
        old = sys.stdout
        sys.stdout = StringIO()
        scope = Scope()
       
        make_scope(scope, {'a' : Number(-5), 'b' : Number(1)})
        body = [Print(Number(1)), BinaryOperation(Reference('a'), '+', Reference('b'))]
        foo = Function(['a', 'b'], body)
       
        assert sys.stdout.getvalue() == (str(-5) + '\n')
        sys.stdout = StringIO()
        res = foo.evaluate(scope)
        check_number(res, -4)
    
class TestFunctionDefinition:

    def test_definition(self):
        pass
     
        
#TestBinary().test_binary_evaluate()    
#TestFunction().test_function()    
    
