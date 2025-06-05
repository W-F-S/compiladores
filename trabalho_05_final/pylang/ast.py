class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class Assign(Node):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

