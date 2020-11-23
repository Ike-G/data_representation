import math as m 
import re

class BinaryString:
    def __init__(self, binary):
        if type(binary) is str : 
            if re.match(r'\b[01]+\b', binary) : 
                self.value = binary
            else : 
                raise ValueError("Invalid binary string")
        else : 
            raise ValueError("Binary string given must be a string")
    
    def display(self) : 
        print("Int: ",int(self))
        print("Float: ",float(self))
        print("Inverse int: ",int(~self))
        print("Inverse float: ",float(~self))
        print("Repr: ",repr(self))
        print("String: ",str(self))
        print("Inverse repr: ",repr(~self))
        print("Inverse string: ",str(~self))
        print(self)
        print(~self)

    @property
    def value(self):
        return self._value 

    @property
    def msb(self):
        return self._value[0]

    @property
    def lsb(self):
        return self._value[-1]

    @value.setter
    def value(self, value):
        if type(value) != str:
            raise ValueError("Binary string given must be a string")
        if not re.match(r'\b[01]+\b', value) : 
            raise ValueError("Invalid binary string")
        self._value = value

    def __add__(self, other) : 
        s = max(len(other)-len(self),0)*'0'+self.value
        o = max(len(self)-len(other),0)*'0'+other.value
        acc = ''
        c = 0 
        for i, j in zip(s[::-1], o[::-1]) : 
            a, b = int(i), int(j)
            acc = str(a^b^c)+acc
            c = ((c&(a|b))|(a&b))
        return BinaryString(str(c)+acc if c else acc)

    def __str__(self):
        return self.value

    def __getitem__(self, key) : 
        return self._value[key]

    def __len__(self):
        return len(self.value)

    def __invert__(self):
        inverted = ''.join([str(int(not bool(int(bit)))) for bit in self.value])
        return BinaryString(inverted)

    def __int__(self) : 
        return sum([2**(len(self)-i-1) for i in range(len(self)) if int(self[i])]) # CHANGE

    def __iter__(self) : 
        return self.value

    def index(self, char) : 
        return self.value.index(char)

    def hex(self) : 
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        # Currently dysfunctional
        # return str([digits[int(self.value[max(0,i-4):i])] for i in range(len(self.value), 0, -4)][::-1])

    def __lshift__(self, shiftVal) : 
        if type(shiftVal) is not int or shiftVal < 0: 
            raise Exception("Invalid shift value. Must be of type positive integer.")
        return self.value+str(0)*shiftVal



class FixPointNumber(BinaryString):
    def __init__(self, binary, point):
        if type(point) != int:
            raise ValueError("The argument <point> must be a whole number")
        self._binary_point = point
        super(FixPointNumber, self).__init__(binary)

    def __float__(self):
        total = int(super()) * (2**(self._binary_point-len(self)))
        return total

    def __int__(self):
        return int(float(self))

    def __str__(self):
        if self._binary_point < len(self):
            return '.'.join((self.value[:self._binary_point], self.value[self._binary_point:]))
        else:
            return self.value

    def __add__(self, other) : 
        raise NotImplementedError("Addition yet to be implemented for fixed point binary objects.")


class TwosComplementNumber(BinaryString):
    def __init__(self, binary) : 
        self.value = binary

    def __abs__(self):
        """ Returns whole number part of twos complement number as BinaryString"""
        if self.value[0]:
            self = self._convert()
        return self

    def _convert(self):
        try : 
            leading_one = self.index('1')
        except : 
            leading_one = 0

        flipped_bits = ~BinaryString(self.value[:leading_one])
        unflipped_bits = BinaryString(self.value[leading_one:])

        return flipped_bits + unflipped_bits

    @property
    def sign_bit(self):
        return self.msb

    def display(self) : 
        super(TwosComplementNumber, self).display()

    def __add__(self, other) : 
        s = max(len(other)-len(self),0)*self.value[0]+self.value
        o = max(len(self)-len(other),0)*other.value[0]+other.value
        acc = ''
        c = 0 
        ofCheck, fixOF = len(self)-1, False
        for i, j in zip(s[::-1], o[::-1]) : 
            a, b = int(i), int(j)
            acc = str(a^b^c)+acc
            c = (c&(a|b))|(a&b)
            ofCheck -= 1 
            if not ofCheck and ((c and (not int(s[0]) and not int(o[0]))) or (not c and (int(s[0]) and int(o[0])))) :
                fixOF = True # Overflow will never be more than a single extra bit
        return TwosComplementNumber(s[0]+acc) if fixOF else TwosComplementNumber(acc)

    # def toBin(self, dec) : 
    #     l = 0 
    #     while 2**(l-1) <= dec : 
    #         l+=1
    #     [str(int(dec%(2**i) >= 0)) for i in range(l-1, 0, -1)]
    def convert(self, bits) : 
        pass 

    def __neg__(self):
        temp = TwosComplementNumber(''.join([str(int(not(int(self[i])))) for i in range(len(self))]))
        return TwosComplementNumber(str(temp+TwosComplementNumber('01')))

    def __int__(self):
        return super(TwosComplementNumber, self).__int__()-int(self[0])*2**len(self)

    def __sub__(self, other) : 
        return self+(-other)
    
    def __le__(self, other) : 
        pass

    def __invert__(self) : 
        return TwosComplementNumber(str(super().__invert__()))


class FloatingPointNumber(TwosComplementNumber):
    def __init__(self, mantissa, exponent):
        self.mantissa = TwosComplementNumber(mantissa)
        self.exponent = TwosComplementNumber(exponent)

    @classmethod
    def as_single_string(cls, binary, mantissa_size):
        return cls(binary[:mantissa_size], binary[mantissa_size:])

    @property
    def mantissa(self):
        return self._mantissa

    @mantissa.setter
    def mantissa(self, mantissa):
        self._mantissa = mantissa

    @property
    def exponent(self):
        return self._exponent

    @exponent.setter
    def exponent(self, exponent):
        self._exponent = exponent  

    def __str__(self) : # BUGGED - Returns 1.1*2**0 for FloatingPointNumber('1','0'), and returns nothing for FloatingPointNumber
        supVal = { 
            '0': '\u2070', 
            '1': '\u00b9', 
            '2': '\u00b2', 
            '3': '\u00b3', 
            '4': '\u2074', 
            '5': '\u2075', 
            '6': '\u2076', 
            '7': '\u2077', 
            '8': '\u2078', 
            '9': '\u2079', 
            '-': '\u207b' 
        }
        
        try : 
            point = self.mantissa.index(str(int(not(int(self.mantissa[0]))))) # Find the index of the first change
            c = True 
        except IndexError : 
            c = False # If the value never changes then there should be no point
        expRepr = ''.join([supVal[i] for i in str(len(self.mantissa[point:])+int(self.exponent))])
        return f'{self.mantissa[point-1]}.{self.mantissa[point:]}\u2082\u00d72{expRepr}' if c else f'{self.mantissa[-1]}\u2082\u00d72{expRepr}'

    def __repr__(self) : 
        return str((str(self.mantissa), str(self.exponent)))

    def __int__(self):
        return int(float(self))

    def __float__(self) : 
        return float(int(self.mantissa)*(2**int(self.exponent)))

    def __invert__(self) : 
        return FloatingPointNumber(str(~self.mantissa), str(~self.exponent))

    def __add__(self, other) : 
        # lshift the larger exponent by its exponent minus the other exponent
        s = self.mantissa << max(int(self.exponent)-int(other.exponent),0) # Error occurs here
        o = other.mantissa << max(int(other.exponent)-int(self.exponent),0)
        if int(self.exponent) <= int(other.exponent) : 
            e = str(self.exponent) 
        else : 
            e = str(other.exponent)
        return FloatingPointNumber(str(TwosComplementNumber(s)+TwosComplementNumber(o)),e)

    def __neg__(self) : 
        return FloatingPointNumber(str(-TwosComplementNumber(str(self.mantissa))), str(self.exponent))
        

def unitTest(f, inp, out) : 
    outs = [f(i) for i in inp]
    if outs == out : 
        print("Success")
    else : 
        print(f"Returned outputs: {outs}\nDesired outputs: {out}\nAccuracy: {sum([(outs[i] == out[i]) for i in range(len(out))])/len(out)}")
        print("Failure")

if __name__ == '__main__':
    a = FloatingPointNumber("0010010", "01")
    b = FloatingPointNumber("10", "10")
    a.display()
    b.display()
    print(int(a+b))
    print(float(a+b))
    print(int(a-b))
    print(float(a-b))
    


