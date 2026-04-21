'''
valuatepostfix method:

Time complexity: O(n)
Reason: The method iterates over each character in the expression once. The operations within each iteration (checking if a character is a digit, pushing to or popping from the stack
Class Definition:

Evaluate: A class designed to evaluate postfix expressions.
Constructor - __init__(self, capacity):

Initializes the instance with a capacity (size of the expression), top as -1 (used as a pointer to the top element in the stack), and an empty list array to store operands.
Method - isempty(self):

Checks if the stack (array) is empty. However, it incorrectly uses capacity instead of checking the size of array or the value of top.
Method - pop(self):

Removes and returns the top element from the stack. If the stack is empty, it returns "empty expression". The method also decrements capacity, which is not the typical behavior for a stack's pop operation.
Method - push(self, operand):

Adds an operand to the top of the stack.
Method - evaluatepostfix(self, exp):

Evaluates the given postfix expression.
Iterates through each character in the expression.
If the character is a digit, it is pushed onto the stack.
If the character is an operator (+, -, *, /), it pops two values from the stack, applies the operator, and pushes the result back onto the stack.
After processing the entire expression, the result is popped from the stack and returned.
Postfix Expression Evaluation:

An instance of the Evaluate class is created with the capacity equal to the length of the postfix expression.
The evaluatepostfix method is called with the expression, and the result is printed.
Example Usage:

The code demonstrates the usage with the expression '2823*+2/+1-', which is evaluated and printed.
Issue with isempty Method:

The isempty method should ideally check if the top index is -1 or if the array is empty, rather than using capacity.
'''
class Evaluate:
    def __init__(self,capacity):
        self.top = -1
        self.capacity = capacity
        self.array = [] # empty array to store the operands.
    def isempty(self): # whether the array is empty or not
        return True if self.capacity == 0 else False
    def pop(self):
        if not self.isempty():
            self.capacity -= 1
            return self.array.pop()
        else:
            return "empty expression"
    def push(self, operand):
        self.array.append(operand)
    def evaluatepostfix(self,exp):
        for i in exp:
            if i.isdigit(): # character is a number(operand)
                self.push(i)
            else:
                val1 = float(self.pop())
                val2 = float(self.pop())
                if i == '+':
                    self.push(str(val2 + val1))
                elif i == '-':
                    self.push(str(val2 - val1))
                elif i == '*':
                    self.push(str(val2 * val1))
                elif i == '/':
                    self.push(str(val2 / val1))
        return self.pop()
# exp = '231*+9-'
exp = '2823*+2/+1-'
obj = Evaluate(len(exp))
print("postfix evaluation : ", (obj.evaluatepostfix(exp)))