from sys import argv
from re import compile

class Parser_Buba():

	neg = None
	number = 0
	x = 0
	pwr = 0

	def __init__(self, m, neg = None, number = 0.0, x = 0, pwr = 0):
		self.neg = neg
		self.number = number
		self.x = x
		self.pwr = pwr
		if m != None:
			if len(m.group(1)) > 0:
				self.neg = m.group(1)
				if self.neg == '=':
					raise
			if m.group(2) == None:
				self.number = 1.0
			else:
				self.number = float(m.group(2))
			if m.group(3) != None:
				self.x = True
				if m.group(4) != None:
					self.pwr = int(m.group(4))
				else:
					self.pwr = 1
		if self.number < 0.0:
			self.neg = "+" if self.neg == "-" else "-"
			self.number = -self.number
		if self.x and self.pwr == 0:
			self.x = False

	def equmbr(self):
		if self.neg == "-":
			return -self.number
		return self.number

	def tostr(self):
		s = ""
		if self.neg != None:
			s += self.neg
			s += " "
		if self.x and (self.number == 1 or self.number == -1) and self.pwr != 0:
			if self.pwr == 1:
				s += "X"
			else:
				s += "X^%d" % (self.pwr)
		elif self.x and self.number != 0 and self.pwr != 0:
			if self.pwr == 1:
				s += "%sX" % str(self.number)
			else:
				s += "%sX^%d" % (str(self.number), self.pwr)
		else:
			s += str(self.number)
		return s

class Computer():

	left = []
	right = []

	def __init__(self):
		self.left = []
		self.right = []

	def parse(self, eq):
		pos = 0
		left = True
		while pos < len(eq):
			if eq[pos:pos + 1] == "=" and left and len(self.left) > 0:
				left = False
				pos += 1
			m = re_space.match(eq, pos)
			if m != None:
				pos += len(m.group(0))
				continue
			m = re_polynom.match(eq, pos)
			if m == None or len(m.group(0)) <= 0:
				print("\033[31mUnexpected syntax: '%s'\033[39m" % (eq[pos:pos + 5]))
				return False
			try:
				p = Parser_Buba(m)
				if p.neg == None:
					if left and len(self.left) > 0:
						p.neg = "+"
					elif not left and len(self.right) > 0:
						p.neg = "+"
			except:
				print("\033[31mInvalid syntax: '%s'\033[39m" % (eq[pos:pos + 5]))
				return False
			if left:
				self.left.append(p)
			else:
				self.right.append(p)
			pos += len(m.group(0))
		if len(self.left) == 0:
			if len(self.right) == 0:
				print("\033[31mBad argument\033[39m")
				return False
			self.left.append(Parser_Buba(None))
		if len(self.right) == 0:
			self.right.append(Parser_Buba(None))
		print("Equation: " + self.tostr() + "\033[39m")
		return True

	def formereduite(self):
		tmp = {}
		for p in self.left:
			if not p.pwr in tmp:
				tmp[p.pwr] = 0.0
			tmp[p.pwr] += p.number if p.neg != "-" else -p.number
		for p in self.right:
			if not p.pwr in tmp:
				tmp[p.pwr] = 0.0
			tmp[p.pwr] -= p.number if p.neg != "-" else -p.number
		self.left = []
		for pwr in sorted(tmp):
			if tmp[pwr] != 0:
				self.left.append(Parser_Buba(None, "+" if len(self.left) > 0 else None, tmp[pwr], True, pwr))
		self.right = [Parser_Buba(None)]
		if len(self.left) == 0:
			self.left.append(Parser_Buba(None))
		print("Reduced form: \033[36m" + self.tostr() + "\033[39m")
		return True

	def calculatrice(self):
		degree = 0
		for p in self.left:
			if p.pwr > degree:
				degree = p.pwr
		print("Polynomial degree: %d" % degree)
		if degree == 0:
			a = self.left[0].equmbr()
			if a == 0:
				print("Every real number are solution")
			else:
				print("No solution")
			return False
		elif degree == 1:
			if len(self.left) > 1:
				b = self.left[0].equmbr()
				a = self.left[1].equmbr()
			else:
				b = 0
				a = self.left[0].equmbr()
			print("\033[90ma = " + str(a) + "\033[39m")
			print("\033[90mb = " + str(b) + "\033[39m")
			print("The solution is:")
			print("\033[90m-b / a = \033[32m" + str(-b / a) + "\033[39m")
		elif degree == 2:
			if len(self.left) > 2:
				c = self.left[0].equmbr()
				b = self.left[1].equmbr()
				a = self.left[2].equmbr()
			elif len(self.left) > 1:
				c = 0
				b = self.left[0].equmbr()
				a = self.left[1].equmbr()
			else:
				c = 0
				b = 0
				a = self.left[0].equmbr()
			print("\033[90ma = " + str(a) + "\033[39m")
			print("\033[90mb = " + str(b) + "\033[39m")
			print("\033[90mc = " + str(c) + "\033[39m")
			d = b ** 2 - (4 * a * c)
			print("\033[90md = " + str(d) + "\033[39m")
			if d > 0:
				print("Discriminant is strictly positive, the two solutions are:")
				print("\033[90m(-b - (d ** 0.5)) / (2 * a) = \033[32m" + str((-b - (d ** 0.5)) / (2 * a)) + "\033[39m")
				print("\033[90m(-b + (d ** 0.5)) / (2 * a) = \033[32m" + str((-b + (d ** 0.5)) / (2 * a)) + "\033[39m")
			else:
				if d == 0:
					print("Discriminant is 0, the solution is:")
					print("\033[90m-b / (2 * a) = \033[32m" + str(-b / (2 * a)))
				else:
					print("Discriminant is strictly negative, the two solutions are:")
					print("\033[90m(-b - (d ** 0.5)) / (2 * a) = \033[32m" + str((-b - (abs(d) ** 0.5)) / (2 * a)) + "i\033[39m")
					print("\033[90m(-b + (d ** 0.5)) / (2 * a) = \033[32m" + str((-b + (abs(d) ** 0.5)) / (2 * a)) + "i\033[39m")
		else:
			print("The polynom degree is not [0;2]")
			return False
		return True

	def tostr(self):
		s = ""
		for p in self.left:
			s += p.tostr()
			s += " "
		s += "="
		for p in self.right:
			s += " "
			s += p.tostr()
		return s

re_polynom = compile('([-+=]?)\s*([0-9\.]+)?(\s*\*?\s*[xX](?:\s*\^\s*([0-9]+))?)?\s*')
re_space = compile('\s+')

if len(argv) <= 1:
	print("Argument error, please write polynom with 2 degree")
else:
	print(argv[1])
	com = Computer()
	if not com.parse(argv[1]):
		exit(1)
	if not com.formereduite():
		exit(1)
	if not com.calculatrice():
		exit(1)