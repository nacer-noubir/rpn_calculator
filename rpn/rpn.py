

class stack:
    def __init__(self, stack) :
        self.stack = stack

    def __add__(self, iteration):
        if len(self.stack) < 2:
            raise ValueError("stack must contain at least 2 elements")
        else:
            last_element = self.stack.pop()

        self.stack[-1]+=last_element
        return self.stack
    
    def __sub__(self, iteration):
        if len(self.stack) < 2:
            raise ValueError("stack must contain at least 2 elements")
        else:
            last_element = self.stack.pop()

        self.stack[-1]-=last_element
        return self.stack

    def __mul__(self, iteration):
        if len(self.stack) < 2:
            raise ValueError("stack must contain at least 2 elements")
        else:
            last_element = self.stack.pop()

        self.stack[-1]*=last_element
        return self.stack
    
    def __floordiv__(self, iteration):
        if len(self.stack) < 2:
            raise ValueError("stack must contain at least 2 elements")
        else:
            last_element = self.stack.pop()
        if last_element == 0:
            raise ValueError("last element must be different than 0")
        self.stack[-1]//=last_element
        return self.stack