import numpy as np

class Calculator(object):
    def __init__(self, val=0):
        """initiates the calculation with a starting value, default is 0"""
        self.val = val
        
    def add(self, num):
        """adds a number 'num' to the previous number"""
        self.val = self.val + num
        return self

    def sub(self, num):
        """subtracts a number 'num' from previous number"""
        self.val = self.val - num
        return self

    def mul(self, num):
        """multiplies a number 'num' by the previous number"""
        self.val = self.val * num
        return self

    def div(self, num):
        """divides the previous number by the input 'num'"""
        self.val = self.val / num
        return self
    
    def clr(self):
        """clears the calculator by setting the result to 0"""
        self.val = 0
        return self
    def result(self):
        return self.val
