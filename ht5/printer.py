class PrettyPrinter():
	def __init__(self):
		self.tab = 0;	

	def print_tab(self, expr):
		print('    '*self.tab, end='')
		print(expr);


	def visit(self, expr):
		expr.visit(self)
		print(';')

	def visitBinaryOperation(self, binary):
		print('(', end = '')
		binary.ihs.visit(self)
		print(' ' + binary.op + ' ', end='')
		binary.rhs.visit(self)
		print(')', end = '')

	def visitUnaryOperation(self, unary):
		print('(' + unary.op, end='')
		unary.expr.visit(self)
		print(')')

	def visitNumber(self, number):
		print(number.value, end='')

	def visitPrint(self, Print):
		print('print', end=' ')
		Print.expr.visit(self)

	def visitRead(self, Read):
		print('read ' + Read.name, end='')

	def visitReference(self, ref):
		print(ref.name, end='')

	def visitFunctionDefinition(self, definition):
		print('def ' + definition.name + '(' + ', '.join(definition.function.args) + '){')
		self.tab += 1;
		for expr in definition.function.body:
			print('    '*self.tab, end='')
			expr.visit(self)
			print(';')
		self.tab -= 1;
		print('    '*self.tab, end='')
		print('}', end='')	

	def visitFunctionCall(self, call):
		call.fun_expr.visit(self)
		print('(', end='')
		flag = 0
		for arg in call.args:
			if flag == 1:
				print(', ', end='')
			arg.visit(self)
			flag = 1
		print(')', end='')

	def visitConditional(self, cond):
		print('if (', end='')
		cond.condition.visit(self)
		print(') {')
		if cond.if_true:
			self.tab += 1;
			for expr in cond.if_true:
				print('    '*self.tab, end='')   
				expr.visit(self)
				print(';')
			self.tab -= 1;
		print('    '*self.tab, end='')
		print('} else {')
		if cond.if_false:
			self.tab += 1;
			for expr in cond.if_false:
				print('    '*self.tab, end='')
				expr.visit(self)
				print(';')
			self.tab -= 1;
		print('    '*self.tab, end='')
		print('}', end='')
