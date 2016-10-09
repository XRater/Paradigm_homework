from yat.model import *
from yat.printer import *

class ConstantFolder:             

	def visit(self, tree):
		return tree.visit(self)             

	def visitNumber(self, number):            
		return number                         	
	
	def visit_list(self, args):
		return list(map(lambda expr: expr.visit(self), args))

	def visitBinaryOperation(self, binary):
		left_part = binary.ihs.visit(self)
		right_part = binary.rhs.visit(self)
		if isinstance(right_part, Number):
			if (right_part.value == 0) and (isinstance(left_part, (Number, Reference))) and (binary.op == '*'):
				return Number(0)
			if isinstance(left_part, Number):
				return BinaryOperation(left_part, binary.op, right_part).evaluate(None)
		if isinstance(left_part, Number):
			if (left_part.value == 0) and (isinstance(right_part, (Number, Reference))) and (binary.op == '*'):
				return Number(0)
		if (isinstance(left_part, Reference)) and (isinstance(right_part, Reference)) and (binary.op == '-'):
			if right_part.name == left_part.name:
				return Number(0)
		return BinaryOperation(left_part, binary.op, right_part);
	
	def visitUnaryOperation(self, unary):
		un_expr = unary.expr.visit(self)
		if isinstance(un_expr, Number):
			return(UnaryOperation(unary.op, un_expr).evaluate(None))
		return UnaryOperation(unary.op, un_expr)

	def visitConditional(self, cond):
		new_cond = cond.condition.visit(self)
		new_if_true = []
		new_if_false = []
		if cond.if_true:                      
		    new_if_true = self.visit_list(cond.if_true)
		if cond.if_false:
		    new_if_false = self.visit_list(cond.if_false)
		return Conditional(new_cond, new_if_true, new_if_false)

	def visitFunctionCall(self, funcall):
		new_fun_expr = funcall.fun_expr.visit(self)
		new_args = self.visit_list(funcall.args)
		return FunctionCall(new_fun_expr, new_args)

	def visitFunctionDefinition(self, definition):
		new_body = self.visit_list(definition.function.body)
		new_function = Function(definition.function.args, new_body)
		return FunctionDefinition(definition.name, new_function)

	def visitPrint(self, p):
		print_expr = p.expr.visit(self)
		return Print(print_expr)

	def visitRead(self, read):
		return read

	def visitReference(self, ref):
		return ref      

if __name__ == '__main__':   
	print('Greatest common division')
	scope = Scope()
	ra = Read('a')
	rb = Read('b')
	Cmp_ab = BinaryOperation(Reference('a'), '<=', Reference('b'))
	evl_bma = BinaryOperation(Reference('b'), '-', Reference('a'))
	btest = BinaryOperation(Number(-1), '+', Number(1))
	utest = UnaryOperation('!', Number(124))
	Eq_a0 = BinaryOperation(Reference('a'), '==', btest)
	ca = Conditional(Eq_a0, [Print(Reference('b'))], [FunctionCall(Reference('GCD'), [Reference('a'), evl_bma])])
	c = Conditional(Cmp_ab,[ca],[FunctionCall(Reference('swap_gcd'), [Reference('a'), Reference('b')])])
	swap_gcd = Function(['a', 'b'], [FunctionCall(Reference('GCD'),[Reference('b'), Reference('a')])])
	GCD = Function(['a', 'b'], [c])
	GCD_def = FunctionDefinition('GCD', GCD)
	swap_gcd_def = FunctionDefinition('swap_gcd', swap_gcd)
	printer = PrettyPrinter()
	printer.visit(ra)
	printer.visit(rb)
	printer.visit(GCD_def)
	printer.visit(swap_gcd_def)
	printer.visit(FunctionCall(Reference('GCD'), [Reference('a'), Reference('b')]))
	folder = ConstantFolder()
	nra = folder.visit(ra)
	nrb = folder.visit(rb)
	ngcd = folder.visit(GCD_def)
	nswap = folder.visit(swap_gcd_def)
	ncall = folder.visit(FunctionCall(Reference('GCD'), [Reference('a'), Reference('b')]))
	printer = PrettyPrinter()
	printer.visit(nra)
	printer.visit(nrb)
	printer.visit(ngcd)
	printer.visit(nswap)
	printer.visit(ncall)
