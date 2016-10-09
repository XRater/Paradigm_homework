from yat.model import *
#from printer import *

class ConstantFolder:             

	def visit(self, tree):
		return tree.visit(self)

	def visitNumber(self, number):            
		return number                         	
	
	def visitBinaryOperation(self, binary):
		left_part = binary.ihs.visit(self)
		right_part = binary.rhs.visit(self)
		if right_part.Type == 'Number':
			if (right_part.value == 0) and (left_part.Type == 'Number' or left_part.Type == 'Reference') and (binary.op == '*'):
				return Number(0)
			if (left_part.Type == 'Number'):
				return(BinaryOperation(left_part, binary.op, right_part).evaluate(None))
		if left_part.Type == 'Number':
			if (left_part.value == 0) and (right_part.Type == 'Number' or right_part.Type == 'Reference') and (binary.op == '*'):
				return Number(0)
		if (right_part.Type == 'Reference') and (left_part.Type == 'Reference') and (binary.op == '-'):
			if right_part.name == left_part.name:
				return Number(0)
		return BinaryOperation(left_part, binary.op, right_part);
	
	def visitUnaryOperation(self, unary):
		un_expr = unary.expr.visit(self)
		if un_expr.Type == 'Number':
			return(UnaryOperation(unary.op, un_expr).evaluate(None))
		return UnaryOperation(unary.op, un_expr);

	def visitConditional(self, cond):
		new_cond = cond.condition.visit(self)
		new_if_true = []
		new_if_false = []
		if cond.if_true:                      
			for expr in cond.if_true:
				new_if_true.append(expr.visit(self))
		if cond.if_false:
			for expr in cond.if_false:
				new_if_false.append(expr.visit(self))
		return Conditional(new_cond, new_if_true, new_if_false)

	def visitFunctionCall(self, funcall):
		new_fun_expr = funcall.fun_expr.visit(self)
		new_args = []
		for arg in funcall.args:
			new_args.append(arg.visit(self))
		return FunctionCall(new_fun_expr, new_args)

	def visitFunctionDefinition(self, definition):
		new_body = []
		for expr in definition.function.body:
			new_body.append(expr.visit(self))
		new_function = Function(definition.function.args, new_body)
		return FunctionDefinition(definition.name, new_function)

	def visitPrint(self, p):
		print_expr = p.expr.visit(self)
		return Print(print_expr)

	def visitRead(self, read):
		return read

	def visitReference(self, ref):
		return ref      

 '''
if __name__ == '__main__':
#	_model_main_tests()
	n1 = Number(0)
	n2 = Number(2)
	r1 = Read('a')
	r2 = Read('b')
	b1 = BinaryOperation(n1 , '-', n2)
	b2 = BinaryOperation(b1, '+', r2)
	u1 = UnaryOperation('-', n2)
	folder = ConstantFolder()
	newb = folder.visit(u1)
	printer = PrettyPrinter()
	printer.visit(newb)            '''

