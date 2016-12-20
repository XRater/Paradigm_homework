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
                    if op == '+' or op == '-' or op == '*' or op == '/' or op == '%':
                        check_number(res, self.op_dict[op](l, r))
                    else :
                        isinstance(res, Number)
                        assert bool(get_value(res)) == bool(self.op_dict[op](l, r))

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
        foo1 = Function([], body)
        res = foo1.evaluate(None)
        check_number(res, 10)
    
    def test_funcvtion_empty(self):
        foo1 = Function([], [])
        res = foo1.evaluate(None)
        
    def test_function_empty_with_args(self):
        scope = Scope()
        make_scope(scope, {'a' : Number(1), 'b' : Number(2)})
        foo1 = Function(['a', 'b'], [])
        res = foo1.evaluate(scope)    
    
    def test_function(self):
        old = sys.stdin
        sys.stdin = StringIO(str(-3))
        scope = Scope()
       
        make_scope(scope, {'a' : Number(-5), 'b' : Number(1)})
        body = [Read('a'), BinaryOperation(Reference('a'), '+', Reference('b'))]
        foo1 = Function(['a', 'b'], body)
       
        res = foo1.evaluate(scope)
        sys.stdin = old
        check_number(res, -2)
    
class TestFunctionDefinition:

    def test_definition(self):
        scope = Scope()
        make_scope(scope, {'a' : Number(5)})
        foo1 = Function([], [])
        res = FunctionDefinition('foo', foo1).evaluate(scope)
        assert isinstance(res, Function)
        check_scope(scope, {'a' : 5, 'foo' : foo1})
        

class TestFunctionCall:

    def test_call(self):
        scope = Scope()
        make_scope(scope, {'a' : Number(1), 'b' : Number(2)})
        body = [BinaryOperation(Reference('a'), '+', Reference('b'))]
       
        foo1 = Function(['a', 'c'], body)
        deffoo1 = FunctionDefinition('func1', foo1)
        deffoo1.evaluate(scope)
        
        res1 = FunctionCall(Reference('func1'), [UnaryOperation('-', Number(1000)), Number(6)]).evaluate(scope)
        check_number(res1, -998)
        check_scope(scope, {'a' : 1, 'b' : 2, 'func1' : 0, 'c' : None})

        foo2 = Function(['a', 'b'], body)
        deffoo2 = FunctionDefinition('func2', foo2)
        deffoo2.evaluate(scope)

        res2 = FunctionCall(Reference('func2'), [UnaryOperation('-', Number(1000)), Number(6)]).evaluate(scope)
        check_number(res2, -994)
        check_scope(scope, {'a' : 1, 'b' : 2, 'func2' : 0, 'c' : None})


class TestConditional:

    def test_cond_allempty(self):
        Conditional(Number(0), [], []).evaluate(None)
        Conditional(Number(1), [], []).evaluate(None)    
        Conditional(Number(0), None, None).evaluate(None)
        Conditional(Number(1), None, None).evaluate(None)    
        Conditional(Number(0), None, []).evaluate(None)
        Conditional(Number(1), None, []).evaluate(None)    
        Conditional(Number(0), [], None).evaluate(None)
        Conditional(Number(1), [], None).evaluate(None)    

    def test_cond_false(self):
        cond = BinaryOperation(Number(1), '*', Number(0))
        res = Conditional(cond, [Number(6)], [Number(-15)]).evaluate(None)
        check_number(res, -15)

    def test_cond_true(self):
        cond = BinaryOperation(Number(1), '+', Number(5))
        res = Conditional(cond, [Number(6)], [Number(-15)]).evaluate(None)
        check_number(res, 6)

    def test_cond_true_emptyfalse(self):
        cond = Number(1)
        res = Conditional(cond, [Number(6)], []).evaluate(None)
        check_number(res, 6)
        res = Conditional(cond, [Number(6)], None).evaluate(None)
        check_number(res, 6)

    def test_cond_false_emptytrue(self):
        cond = Number(0)
        res = Conditional(cond, [], [Number(6)]).evaluate(None)
        check_number(res, 6)
        res = Conditional(cond, None, [Number(6)]).evaluate(None)
        check_number(res, 6)

    def test_cond_comp_false(self):
        scope = Scope()
        old = sys.stdin
        cond = Number(0)
        sys.stdin = StringIO(str(-5))
        res = Conditional(cond, [], [Read('a'), Number(3)]).evaluate(scope)
        check_number(res, 3)
        check_scope(scope, {'a' : -5})
        sys.stdin = old

    def test_cond_comp_false(self):
        scope = Scope()
        old = sys.stdin
        cond = Number(1)
        sys.stdin = StringIO(str(-5))
        res = Conditional(cond, [Read('a'), Number(3)], []).evaluate(scope)
        check_number(res, 3)
        check_scope(scope, {'a' : -5})
        sys.stdin = old
                                                                          



