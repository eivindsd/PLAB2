"""module to represent a calculator"""
import numbers
import re
import numpy


class Container:
    """superklasse"""

    def __init__(self):
        self.items = []

    def size(self):
        """return number of elements in self._items"""
        return len(self.items)

    def is_empty(self):
        """check if self._items is empty"""
        return len(self.items) == 0

    def push(self, item):
        """add item to end of self._items"""
        self.items.append(item)

    def pop(self):
        """pop off the correct element of self._items, and return it"""
        raise NotImplementedError

    def peek(self):
        """return the top element without removing it"""
        raise NotImplementedError


class Queue(Container):
    """subklasse som arver fra Container"""

    def __init__(self):
        super(Queue, self).__init__()

    def peek(self):
        """return the *first* element of the list, do not delete it"""
        assert not self.is_empty()
        return self.items[0]

    def pop(self):
        """pop off the first element"""
        assert not self.is_empty()
        return self.items.pop(0)


class Stack(Container):
    """subklasse som arver fra Container"""

    def __init__(self):
        super(Stack, self).__init__()

    def peek(self):
        """return the *first* element of the list, do not delete it"""
        assert not self.is_empty()
        return self.items[-1]

    def pop(self):
        """pop off the first element"""
        assert not self.is_empty()
        return self.items.pop(-1)


def unit_test():
    """teste korrekt oppførsel"""

    stack = Stack()
    queue = Queue()

    stack.push(0), stack.push(1), stack.push(2), stack.push(3), stack.push(4)

    queue.push(0), queue.push(1), queue.push(2), queue.push(3), queue.push(4)

    print(str(stack.items))
    print(str("Det er " + str(stack.size()) + " elementer i stacken. "))
    print("\n")
    while not stack.is_empty():
            stack.pop()
            print(stack.items)
            print("Det er " + str(stack.size()) + " elementer igjen i stacken. ")
            print("\n")

    print(str(queue.items))
    print(str("Det er " + str(queue.size()) + " elementer i queuen"))
    print("\n")
    while not queue.is_empty():
        queue.pop()
        print(queue.items)
        print("Det er " + str(queue.size()) + " elementer igjen i queuen. ")
        print("\n")


class Function:
    """class to operate functions"""

    def __init__(self, func):
        self.func = func

    def execute(self, element, debug=True):
        """check type"""
        if not isinstance(element, numbers.Number):
            raise TypeError("Cannot execute func if element is not a number")
        result = self.func(element)
        if debug:
            print("Function: " + self.func.__name__ +
                  "({:f}) = {:f}".format(element, result))
        return result


def func_test():
    """test that Function class works"""
    exponential_func = Function(numpy.exp)
    sin_func = Function(numpy.sin)
    print(exponential_func.execute(sin_func.execute(0)))


class Operator:
    """class to operate arithmetic operations"""

    def __init__(self, operator, strength):
        self.operator = operator
        self.strength = strength

    def execute(self, num1, num2, debug=True):
        """check type of elements"""
        if not isinstance(num1, numbers.Number) or not isinstance(num2, numbers.Number):
            raise TypeError("Cannot execute func if element is not a number")
        result = self.operator(num1, num2)
        if debug:
            print("Operation: " + self.operator.__name__
                  + "({:f}, {:f}) = {:f}".format(num1, num2, result))
        return result


def operator_test():
    """test that Operation class works"""
    add_op = Operator(operator=numpy.add, strength=0)
    multiply_op = Operator(operator=numpy.multiply, strength=1)
    print(add_op.execute(1, multiply_op.execute(2, 3)))


class Calculator:
    """class to represent the calculator"""

    def __init__(self):
        """define the functions supported by linking them to Python
        functions. These can be made elsewhere in the program,
        or imported (e.g., from numpy"""
        self.functions = {'EXP': Function(numpy.exp),
                          'LOG': Function(numpy.log),
                          'SIN': Function(numpy.sin),
                          'COS': Function(numpy.cos),
                          'SQRT': Function(numpy.sqrt)}
        """Define the operators supported. Link them to Python functions"""
        self.operators = {'PLUSS': Operator(numpy.add, 0),
                          'GANGE': Operator(numpy.multiply, 1),
                          'DELE': Operator(numpy.divide, 1),
                          'MINUS': Operator(numpy.subtract, 0)}
        """define the output-queue. The parse_text method fills this with RPN.
        The evaluate_output_queue method evaluates it"""
        self.output_queue = Queue()

    def rpn(self):
        """method to evaluate reverse polish notation"""
        stack = Stack()
        while not self.output_queue.is_empty():
            element = self.output_queue.peek()
            if isinstance(element, numbers.Number):
                stack.push(self.output_queue.pop())
            elif isinstance(element, Function):
                self.output_queue.pop()
                result = element.execute(stack.pop())
                stack.push(result)
            elif isinstance(element, Operator):
                self.output_queue.pop()
                num1 = stack.pop()
                num2 = stack.pop()
                result = element.execute(num2, num1)
                stack.push(result)
        return stack.peek()

    def shunting_yard(self, inputqueue):
        """method to build rpn-queue with shunting-yard algorithm"""
        operatorstack = Stack()
        while inputqueue.size() > 0:
            elem = inputqueue.peek()
            if isinstance(elem, numbers.Number):
                self.output_queue.push(elem)
                inputqueue.pop()
            elif isinstance(elem, Function):
                operatorstack.push(elem)
                inputqueue.pop()
            elif elem == '(':
                operatorstack.push(elem)
                inputqueue.pop()
            elif elem == ')':
                while not operatorstack.peek() == '(':
                    self.output_queue.push(operatorstack.pop())
                operatorstack.pop()
                inputqueue.pop()
            elif isinstance(elem, Operator):
                while not operatorstack.is_empty() and \
                        (isinstance(operatorstack.peek(), Function) or
                         (isinstance(operatorstack.peek(), Operator) and
                          operatorstack.peek().strength >= elem.strength)):
                    self.output_queue.push(operatorstack.pop())
                operatorstack.push(elem)
                inputqueue.pop()
        while not operatorstack.is_empty():
            self.output_queue.push(operatorstack.pop())

    def txt_parse(self, text):
        """method to parse text into a queue"""
        output = Queue()
        text = text.replace(" ", "").upper()

        floats = "^[−0123456789.]+"
        paranthesis = "^[()]"
        functions = "|".join(["^" + func for func in self.functions.keys()])
        operators = "|".join(["^" + op for op in self.operators.keys()])

        while len(text) > 0:
            if re.search(floats, text):
                check = re.search(floats, text)
                output.push(float(check.group(0)))
                text = text[check.end(0):]
            elif re.search(paranthesis, text):
                check = re.search(paranthesis, text)
                output.push(str(check.group(0)))
                text = text[check.end(0):]
            elif re.search(functions, text):
                check = re.search(functions, text)
                output.push(self.functions.get(check.group(0)))
                text = text[check.end(0):]
            elif re.search(operators, text):
                check = re.search(operators, text)
                output.push(self.operators.get(check.group(0)))
                text = text[check.end(0):]
        return output


def calc_test():
    """test that Calculator class works"""
    calc = Calculator()
    print(calc.functions['EXP'].execute(calc.operators['PLUSS']
        .execute(1, calc.operators['GANGE'].execute(2, 3))))


def rpn_test():
    """test that rpn method works"""
    calc = Calculator()
    calc.output_queue.push(1), calc.output_queue.push(2),\
    calc.output_queue.push(3),
    calc.output_queue.push(calc.operators['GANGE']),\
    calc.output_queue.push(calc.operators['PLUSS']),
    calc.output_queue.push(calc.functions['EXP'])
    print(calc.rpn())


def shunting_yard_test():
    """test that shunting yard method works"""
    calc = Calculator()
    queue = Queue()
    queue.push(calc.functions['EXP']), queue.push('('),\
    queue.push(1), queue.push(calc.operators['PLUSS']),
    queue.push(2), queue.push(calc.operators['GANGE']),\
    queue.push(3), queue.push(")")
    calc.shunting_yard(queue)
    print(calc.rpn())


def calculate_expression(text):
    """method to check that everything works"""
    calc = Calculator()
    queue = calc.txt_parse(text)
    calc.shunting_yard(queue)
    print(calc.rpn())


calculate_expression("EXP(((15 DELE (7 MINUS (1 PLUSS 1))) GANGE 3) MINUS (2 PLUSS (1 PLUSS 1)))")
