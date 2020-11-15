import math as m 

class BinaryString:
    def __init__(self, binary):
        self.value = binary

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
        for digit in value:
            if digit not in ["1", "0"]:
                raise ValueError("Binary string given contains values that are not 1 or 0")
        self._value = value

    def __str__(self):
        return self.value

    def __getitem__(self, key) : 
        return int(self.value[key])

    def __add__(self, other):
        return BinaryString(str(self) + str(other)) # Converts both values to a binary string

    def __len__(self):
        return len(self.value)

    def __invert__(self):
        inverted = ''.join([str(int(not bool(int(bit)))) for bit in self.value])
        return self.__class__(inverted)

    def __int__(self) : 
        return sum([2**(len(self)-i-1) for i in range(len(self)) if self[i]])

    def __iter__(self) : 
        return self.value

    def index(self, char) : 
        return self.value.index(char)

    def hex(self) : 
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        # Currently dysfunctional
        # return str([digits[int(self.value[max(0,i-4):i])] for i in range(len(self.value), 0, -4)][::-1])

        

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


class TwosComplementNumber(BinaryString):
    def __init__(self, binary) : 
        self.value = binary

    def __abs__(self):
        """ Returns whole number part of twos complement number as BinaryString"""
        if self.is_negative():
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

    def __neg__(self):
        return self._convert()

    def __int__(self):
        return super(TwosComplementNumber, self).__int__()-self[0]*2**len(self)


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

    def __str__(self) :
        supVal = { '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3', '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079', '-': '\u207b' }
        expRepr = ''.join([supVal[i] for i in str(int(self.exponent))])
        try : 
            point = self.mantissa.index(str(int(not(self.mantissa[0]))))
        except : 
            point = len(self.mantissa)-2
        c1 = self.mantissa[point] 
        cend = self.mantissa[point+1:]
        return f'{c1}.{cend}\u2082\u00d72{expRepr}'

    def __repr__(self) : 
        return str((str(self.mantissa), str(self.exponent)))

    def __int__(self):
        return int(float(self))

    def __float__(self) : 
        return float(int(self.mantissa)*(2**int(self.exponent)))

    def __invert__(self) : 
        return FloatingPointNumber(str(~self.mantissa), str(~self.exponent))
        

def unitTest(f, inp, out) : 
    outs = [f(i) for i in inp]
    if outs == out : 
        print("Success")
    else : 
        print(f"Returned outputs: {outs}\nDesired outputs: {out}\nAccuracy: {sum([(outs[i] == out[i]) for i in range(len(out))])/len(out)}")
        print("Failure")

if __name__ == '__main__':
    x = FloatingPointNumber("1101", "10")
    print(int(x))
    print(int(~x))
    print(float(x))
    print(float(~x))
    print(x)
    print(~x)
    print(repr(x))
    print(repr(~x))
    


