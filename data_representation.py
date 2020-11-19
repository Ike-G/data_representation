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
        return self.__class__(inverted)

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
        leading_one = len(self)
        while leading_one != "1" and leading_one > 0:
            leading_one -= 1

        flipped_bits = ~BinaryString(self.value[:leading_one])
        unflipped_bits = BinaryString(self.value[leading_one:])

        return flipped_bits + unflipped_bits

    @property
    def sign_bit(self):
        return self.msb

    def __add__(self, other) : 
        pass

    # def toBin(self, dec) : 
    #     l = 0 
    #     while 2**(l-1) <= dec : 
    #         l+=1
    #     [str(int(dec%(2**i) >= 0)) for i in range(l-1, 0, -1)]
    def convert(self, bits) : 
        pass 

    def __neg__(self):
        return self._convert()

    def __int__(self):
        return super(TwosComplementNumber, self).__int__()-int(self[0])*2**len(self)


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
        expRepr = ''.join([supVal[i] for i in str(int(self.exponent))])
        try : 
            point = self.mantissa.index(str(int(not(self.mantissa[0]))))-1 # Find the index of the value before the first change
            c = True 
        except : 
            c = False # If the value never changes then there should be no point
        return f'{self.mantissa[point]}.{self.mantissa[point+1:]}\u2082\u00d72{expRepr}' if c else f'{self.mantissa[-1]}\u2082\u00d72{expRepr}'

    def __repr__(self) : 
        return str((str(self.mantissa), str(self.exponent)))

    def __int__(self):
        return int(float(self))

    def __float__(self) : 
        return float(int(self.mantissa)*(2**int(self.exponent)))

    def __invert__(self) : 
        return FloatingPointNumber(str(~self.mantissa), str(~self.exponent))

    def __add__(self, other) : 
        # Normalise both to same exponent
        # Subsequently convert to the same size through appending to the front. If not(msb) append 0 to front, if msb append 1 to front. 
        pass 
        
        #print(self.addition(s,o))
        # subsequently use min(self.exponent, other.exponent) to return to the smaller exponent. 
        #return FloatingPointNumber(1, )

    def addition(self, s, o, acc = '', c = 0, i = None) : 
        if len(acc) == len(s) : 
            return acc 
        else : 
            # ((a xor b) and not c) or ((a nor b) and c)
            # (a and b or c) or (b and c)
            i = max(len(s),len(o))-len(acc)-1 if i is None else i
            a, b = int(s[i]), int(o[i])
            acc = str(((a^b)&int(not c)) | (int(not a|b)&c))+acc
            return self.addition(s, o, acc, ((a&b|c)|(b&c)), i-1)

    def __neg__(self) : 
        return FloatingPointNumber((~self.mantissa)+1, self.exponent)
        

def unitTest(f, inp, out) : 
    outs = [f(i) for i in inp]
    if outs == out : 
        print("Success")
    else : 
        print(f"Returned outputs: {outs}\nDesired outputs: {out}\nAccuracy: {sum([(outs[i] == out[i]) for i in range(len(out))])/len(out)}")
        print("Failure")

if __name__ == '__main__':
    x = FloatingPointNumber("1101101", "10")
    print(int(x))
    print(int(~x))
    print(float(x))
    print(float(~x))
    print(x)
    print(~x)
    print(repr(x))
    print(repr(~x))
    


