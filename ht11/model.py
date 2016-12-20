import sys                                        
    
class Scope(object):
    def __init__(self, parent = None):
        self.variables = {}
        self.parent = parent
    def __setitem__(self, key, value):
        self.variables[key] = value;
    def __getitem__(self, key):
        if self.parent:
            return self.variables.get(key, self.parent[key])
        else:
            return self.variables.get(key, None)
            

class Number:
    def __init__(self, value):
        self.value = value  
    def evaluate(self, scope):
        return self
    def __bool__(self):
        return bool(self.value)

class BinaryOperation:
    def __init__(self, ihs, op, rhs):
        self.ihs = ihs
        self.rhs = rhs
        self.op = op
        self.operation_dictionary = {'+': lambda x, y: x.value + y.value, '-': lambda x, y: x.value - y.value,
                                     '*': lambda x, y: x.value * y.value, '/': lambda x, y: x.value // y.value,
                                     '%': lambda x, y: x.value % y.value, '==': lambda x, y: int(x.value == y.value),
                                     '!=': lambda x, y: int(x.value != y.value), '>': lambda x, y: int(x.value > y.value),
                                     '<': lambda x, y: int(x.value < y.value), '>=': lambda x, y: int(x.value >= y.value),
                                     '<=': lambda x, y: int(x.value <= y.value), '&&': lambda x, y: int(bool(x.value) * bool(y.value)),
                                     '||': lambda x, y: int(bool(x.value) + bool(y.value))}
    def evaluate(self, scope):
        left_part = self.ihs.evaluate(scope)
        right_part = self.rhs.evaluate(scope)  
        return Number(self.operation_dictionary[self.op](left_part, right_part))

class UnaryOperation:
    def __init__(self, op, expr):
        self.expr = expr
        self.op = op
        self.operation_dictionary = {'-': lambda x: -x.value, '!': lambda x: int(not(bool(x.value)))}
    def evaluate(self, scope):
        expr_result = self.expr.evaluate(scope) 
        return Number(self.operation_dictionary[self.op](expr_result))

class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body
    def evaluate(self, scope):
        result = Number(0)
        for expr in self.body:
            result = expr.evaluate(scope)
        return result

class FunctionCall:
    def __init__(self, fun_expr, args):
        self.args = args
        self.fun_expr = fun_expr
        
    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for arg, name in zip(self.args, function.args):
            call_scope[name] = arg.evaluate(scope)
        return function.evaluate(call_scope)


class Conditional:
    def __init__(self, condition, if_true = None, if_false = None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false
        
    def evaluate(self, scope):
        condition = self.condition.evaluate(scope)
        result = Number(0)
        body = []
        if condition and self.if_true:
            body = self.if_true
        elif self.if_false:
            body = self.if_false
        for expr in body:
            result = expr.evaluate(scope)
        return result


class Reference:
    def __init__(self, name):
        self.name = name
    def evaluate(self, scope):
        return scope[self.name] 

class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function
    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function 

class Read:
    def __init__(self, name):
        self.name = name
    def evaluate(self, scope):
        value = Number(int(input()))
        scope[self.name] = value
        return value
        
class Print:
    def __init__(self, expr):
        self.expr = expr
    def evaluate(self, scope):
        result = self.expr.evaluate(scope)
        print(result.value)
        return result

def Test0():            #Simple print
    print('Simple print')
    scope = Scope()
    n1 = Number(-156)
    p1 = Print(n1)
    p1.evaluate(scope)

def Test1():            # a + b
    print('a + b calculation')
    scope = Scope()
    r1 = Read('a')
    r2 = Read('b')
    b1 = BinaryOperation(r1, '+', r2)
    p1 = Print(b1)
    p1.evaluate(scope)

def Test2():
    print('a^2 - (-b)^2 calculation')
    scope = Scope()     #a^2 - (-b)^2 (with function)
    r1 = Read('a')
    r2 = Read('b')

    rf1 = Reference('p')
    rf2 = Reference('q')
    b1 = BinaryOperation(rf1, '*', rf1)
    b2 = BinaryOperation(UnaryOperation('-', rf2), '*', UnaryOperation('-', rf2))
    b3 = BinaryOperation(b1, '-', b2)
    f1 = Function(['p', 'q'], [b1, b2, b3])
    fd = FunctionDefinition('square_sub', f1)
    fd.evaluate(scope)

    fc = FunctionCall(Reference('square_sub'), [r1, r2])

    p = Print(fc)
    p.evaluate(scope)

def Test3():
    print('Maximum of two integers')
    scope = Scope()                                                                                                  #Maximum of 2
    r1 = Read('a')
    r2 = Read('b')
    c1 = Conditional(BinaryOperation(Reference('a'), '>=', Reference('b')), [Print(Reference('a'))], [Print(Reference('b'))])
    main_function = Function([],[r1, r2, c1])
    main_function.evaluate(scope)

def Test4():
    print('All integers from n to 1')
    scope = Scope()                                                                           #Recurtion Test (All integers from n to 1)
    r1 = Read('n')
    minus_minus = Function('n', [BinaryOperation(Reference('n'), '-', Number(1))])
    c = Conditional(BinaryOperation(Reference('n'), '>', Number(1)), [ FunctionCall(Reference('f'), [FunctionCall(Reference('--'), [Reference('n')])] ) ]) 
    f = Function(['n'], [Print(Reference('n')), c]) 
    main_function = Function([], [FunctionDefinition('--', minus_minus), FunctionDefinition('f', f), r1, FunctionCall(Reference('f'), [Reference('n')])])
    main_function.evaluate(scope)

def Test5():
    print('Greatest common division')
    scope = Scope()
    ra = Read('a')
    rb = Read('b')
    Cmp_ab = BinaryOperation(Reference('a'), '<=', Reference('b'))
    evl_bma = BinaryOperation(Reference('b'), '-', Reference('a'))
    Eq_a0 = BinaryOperation(Reference('a'), '==', Number(0))
    ca = Conditional(Eq_a0, [Print(Reference('b'))], [FunctionCall(Reference('GCD'), [Reference('a'), evl_bma])])
    c = Conditional(Cmp_ab,[ca],[FunctionCall(Reference('swap_gcd'), [Reference('a'), Reference('b')])])
    swap_gcd = Function(['a', 'b'], [FunctionCall(Reference('GCD'),[Reference('b'), Reference('a')])])
    GCD = Function(['a', 'b'], [c])
    GCD_def = FunctionDefinition('GCD', GCD)
    swap_gcd_def = FunctionDefinition('swap_gcd', swap_gcd)
    main_function = Function([], [ra, rb, GCD_def, swap_gcd_def, FunctionCall(Reference('GCD'), [Reference('a'), Reference('b')])])
    main_function.evaluate(scope)

def _model_main_tests():         #May I call it like this? 
    if len(sys.argv) != 2:
        print('Enter number of the test')
        sys.exit()
    test_number = int(sys.argv[1])
    d = [Test0, Test1, Test2, Test3, Test4, Test5];
    d[test_number]()

            
if __name__ == '__main__':
    _model_main_tests()

                 
