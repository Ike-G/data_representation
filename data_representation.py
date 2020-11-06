xclass BinaryString:
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
        return self.value[key]

    def __add__(self, other):
        return BinaryString(str(self) + str(other)) # Converts both values to a binary string

    def __len__(self):
        return len(self.value)

    def __invert__(self):
        inverted = ''.join([str(int(not bool(int(bit)))) for bit in self.value])
        return self.__class__(inverted)

    def __int__(self) : 
        return sum([2**(len(self)-i-1) for i in range(len(self)) if self[i]])
        

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
            return self.value[:self._binary_point] + "." + self.value[self._binary_point:]
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

    def to_positive(self):
        return abs(self)

    def __neg__(self):
        return self._convert()

    def is_positive(self):
        if self.sign_bit == "1":
            return False
        else:
            return True

    def is_negative(self):
        if self.sign_bit == "0":
            return False
        else:
            return True

    def __int__(self):
        bitCalc = lambda a, b: int(a[b])*(2**(len(a)-b-1)) 
        twoComp = lambda x : sum([bitCalc(x, i) if i else -bitCalc(x, i) for i in range(len(x))])
        return twoComp(self)


class FloatingPointNumber(TwosComplementNumber):
    def __init__(self, mantissa, exponent):
        self.mantissa = BinaryString(mantissa)
        self.exponent = BinaryString(exponent)

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

    def __str__(self):
        return str(self.mantissa + self.exponent)

    def __int__(self):
        bitCalc = lambda a, b: int(a[b])*(2**(len(a)-b-1)) 
        twoComp = lambda x : sum([bitCalc(x, i) if i else -bitCalc(x, i) for i in range(len(x))]) # Defines twos complement conversion
        exp = twoComp(self.exponent) # Convert exponent from twos complement
        mantissa = twoComp(self.mantissa) # Convert mantissa from twos complement
        return mantissa*(2**exp)

def unitTest(f, inp, out) : 
    outs = [f(i) for i in inp]
    if outs == out : 
        print("Success")
    else : 
        print(f"Returned outputs: {outs}\nDesired outputs: {out}\nAccuracy: {sum([(outs[i] == out[i]) for i in range(len(out))])/len(out)}")
        print("Failure")

if __name__ == '__main__':
    x = FloatingPointNumber("01011101", "1011")
    print(int(x))
    print(int(~x))
    print(x)
    print(~x)
    


