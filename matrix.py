import fractions


class Matrix:
    height = 1
    width = 1
    __data = None

    def __init__(self, defValue, height=1, width=1):
        if isinstance(defValue, Matrix) and (defValue.height != 1 or defValue.width != 1):
            self.height = defValue.height
            self.width = defValue.width
            self.__data = defValue.__data.copy()
        else:
            if isinstance(defValue, Matrix): defValue = defValue[0]
            self.height = height
            self.width = width
            self.__data = [0] * (height * width)
            for i in range(min(height, width)): self[i, i] = defValue

    def isScalar(self):
        return self.height == 1 and self.width == 1

    def rowAdd(self, i, j, ratio):
        for k in range(self.width):
            self[i, k] += ratio * self[j, k]

    def columnAdd(self, i, j, ratio):
        for k in range(self.height):
            self[k, i] += ratio * self[k, j]

    def __add__(self, other):
        other = Matrix(other, self.height, self.width)
        self = Matrix(self, other.height, other.width)

        if self.height != self.height or self.width != other.width:
            raise MatrixException("Addition of matrices of different sizes")

        for i in range(len(self)): self[i] += other[i]

        return self

    def __radd__(self, other):
        return Matrix(other) + self

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return Matrix(other) - self

    def __mul__(self, other):
        if not isinstance(other, Matrix): other = Matrix(other)

        if self.isScalar(): self, other = other, self

        if other.isScalar():
            m = Matrix(self)
            for i in range(len(m)):
                m[i] *= other[0]
            return m

        if self.width != other.height:
            raise MatrixException("Произведение матриц с разным размером")

        m = Matrix(0, self.height, other.width)

        for i in range(m.width):
            for j in range(m.height):
                s = None
                for k in range(self.width):
                    t = self[i, k] * other[k, j]
                    s = (t if k == 0 else s + t)
                m[i, j] = s

        return m

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * other ** -1

    def __rtruediv__(self, other):
        return self ** -1 * other

    def __pow__(self, power):
        if isinstance(power, Matrix):
            if not power.isScalar():
                raise MatrixException("Возведение матрицы в степень матрицы")
            power = power[0]

        power = fractions.Fraction(power)

        if power.denominator != 1:
            raise MatrixException("Возведение матрицы в нецелую степень")

        if self.width != self.height:
            raise MatrixException("Возведение не квадратной матрицы в степень")

        if power == -1:
            self = Matrix(self)
            m = Matrix(1, self.height, self.width)

            for i in range(self.width):
                if self[i, i] == 0:
                    for j in range(i + 1, self.height):
                        if self[j, i] != 0:
                            self.rowAdd(i, j, 1)
                            m.rowAdd(i, j, 1)
                            break
                    else:
                        raise MatrixException("Возведение вырожденной матрицы в отрицательную степень")

                ratio = 1 / self[i, i] - 1
                self.rowAdd(i, i, ratio)
                m.rowAdd(i, i, ratio)

                for j in range(0, self.height):
                    if j == i: continue
                    ratio = -self[j, i] / self[i, i]
                    self.rowAdd(j, i, ratio)
                    m.rowAdd(j, i, ratio)
            return m
        elif power == 2:
            return self * self
        elif power == 1:
            return Matrix(self)
        elif power == 0:
            return Matrix(1, self.height, self.width)
        elif power < 0:
            return (self ** -1) ** -power
        elif power % 2 == 1:
            return self ** (power - 1) * self
        else:
            return (self ** (power // 2)) ** 2

    def __rpow__(self, other):
        return Matrix(other) ** self

    def __pos__(self):
        return Matrix(self)

    def __neg__(self):
        return self * -1

    def __bool__(self):
        return any(self.__data)

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, key):
        return self.__data[key if isinstance(key, int) else key[0] * self.width + key[1]]

    def __setitem__(self, key, value):
        self.__data[key if isinstance(key, int) else key[0] * self.width + key[1]] = fractions.Fraction(value)

    def __iter__(self):
        return self.__data.__iter__();

    def __reversed__(self):
        return self.__data.__reversed__();

    def __contains__(self, item):
        return item in self.__data;

    def __str__(self):
        maxlen = max(map(lambda a: len(str(a)), self))
        return '\n'.join(' '.join(map(lambda a: '{:>{}}'.format(str(a), maxlen),
                                      self.__data[i * self.width:(i + 1) * self.width])) for i in range(self.height))


class MatrixException(Exception): pass
