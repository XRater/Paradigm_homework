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
		return self;
	def __bool__(self):
		return bool(self.value)
	def __add__(self, other):
		return Number(self.value + other.value)
	def __sub__(self, other):
		return Number(self.value - other.value)
	def __mul__(self, other):
		return Number(self.value * other.value)
	def __floordiv__(self, other):
		return Number(self.value // other.value)
	def __mod__(self, other):
		return Number(self.value % other.value)
	def __eq__(self, other):
		return Number(int(self.value == other.value))
	def __ne__(self, other):
		return Number(int(self.value != other.value))
	def __lt__(self, other):
		return Number(int(self.value < other.value))
	def __gt__(self, other):
		return Number(int(self.value > other.value))
	def __le__(self, other):
		return Number(int(self.value <= other.value))
	def __ge__(self, other):
		return Number(int(self.value >= other.value))
	def __and__(self, other):
		return Number(int(bool(self.value)*bool(other.value)))
	def __or__(self, other):
		return Number(int(bool(self.value) + bool(other.value)))
	def __neg__(self):
		return Number(-self.value)
	def __or__(self, other):
		return Number(int(bool(self.value) + bool(other.value)))
	def logical_not(self):
		return Number(int(not(self.value)))

class BinaryOperation:
	def __init__(self, ihs, op, rhs):
		self.ihs = ihs
		self.rhs = rhs
		self.op = op
	def evaluate(self, scope):
		left_part = self.ihs.evaluate(scope)
		right_part = self.rhs.evaluate(scope)
		if self.op == '+':
			return left_part + right_part
		if self.op == '-':
			return left_part - right_part
		if self.op == '*':
			return left_part * right_part
		if self.op == '/':
			return left_part // right_part
		if self.op == '%':
			return left_part % right_part
		if self.op == '==':
			return left_part == right_part
		if self.op == '!=':
			return left_part != right_part
		if self.op == '<':
			return left_part < right_part
		if self.op == '>':
			return left_part > right_part
		if self.op == '<=':
			return left_part <= right_part
		if self.op == '>=':
			return left_part >= right_part
		if self.op == '&&':
			return left_part & right_part
		if self.op == '||':
			return left_part | right_part

class UnaryOperation:
	def __init__(self, op, expr):
		self.expr = expr
		self.op = op
	def evaluate(self, scope):
		expr_result = self.expr.evaluate(scope)
		if self.op == '-':
			return -expr_result
		if self.op == '!':
			return expr_result.logical_not()

class Function:
	def __init__(self, args, body):
		self.args = args
		self.body = body
	def evaluate(self, scope):
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
	def __init__(self, condition, if_true, if_false = None):
		self.condition = condition
		self.if_true = if_true
		self.if_false = if_false
	def evaluate(self, scope):
		condition = self.condition.evaluate(scope)
		result = 0;
		if (condition):
			for expr in self.if_true:
				result = expr.evaluate(scope)
		else:
			for expr in self.if_false:
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
	print('a^2 - b^2 calculation')
	scope = Scope()     #a^2 - b^2 (with function)
	r1 = Read('a')
	r2 = Read('b')

	rf1 = Reference('p')
	rf2 = Reference('q')
	b1 = BinaryOperation(rf1, '*', rf1)
	b2 = BinaryOperation(rf2, '*', rf2)
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
	scope = Scope()                                                                           #Recurtion Test (But I cant realize it, cause I have to declarate variables successively)
	r1 = Read('n')
	minus_minus = Function('n', BinaryOperation(Reference('n'), '-', Number(1)))
	FunctionDefinition('--', minus_minus).evaluate(scope)


	c = Conditional(BinaryOperation(Reference('n'), '>=', Number(0)), [FunctionCall(f, Reference('--'))])
	f = Function(['n'], [Print(Reference('n')), c]) 
	fc = FunctionCall(f, [r1])
	fc.evaluate(scope)

def _model_main_tests():         #May I call it like this? 
	if len(sys.argv) != 2:
		print('Enter number of the test')
		sys.exit()
	test_number = int(sys.argv[1])
	d = [Test0, Test1, Test2, Test3];
	d[test_number]()

		   	
if __name__ == '__main__':
	_model_main_tests()

                 
