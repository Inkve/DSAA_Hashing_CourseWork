from array import array
from random import randint
from math import sqrt, log10


class Data:
    def __init__(self, _size, _max_element):
        self.size = _size
        self.max_element = _max_element
        self.array = array("Q", [randint(0, self.max_element) for _ in range(self.size)])
        self.gaps = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85,
                     0.9, 0.95, 1]

    def test(self):
        return sum(self.array)


class DivideHashData(Data):
    def __init__(self, _size, _max_element):
        super().__init__(_size, _max_element)
        self.dividers = self.get_dividers()

    def hash(self, type_of_del=1):
        if type_of_del in [1, 2, 3, 4]:
            temp_arr_del = [-1] * int(self.size * 1.2)
            count_collisions = 0
            future_result = {}

            for i in range(self.size):
                index = self.array[i] % self.dividers[type_of_del - 1] + 1
                if (temp_arr_del[index] == -1) or (temp_arr_del[index] == self.array[i]):
                    temp_arr_del[index] = self.array[i]
                else:
                    count_collisions += 1
                if i / self.size in self.gaps:
                    future_result[i / self.size] = count_collisions
            future_result[1.00] = count_collisions

            return future_result
        else:
            raise Exception("Incorrect type of divide hash")

    def get_dividers(self):
        divs = [1, 1, 1, 1]
        for step in (range(1, self.size)):
            increased_number = self.size + step
            decreased_number = max(self.size - step, 1)

            if divs[0] == 1:
                if self.check_primary(increased_number):
                    divs[0] = increased_number
                elif self.check_primary(decreased_number):
                    divs[0] = decreased_number
            if divs[1] == 1:
                if not (self.check_primary(increased_number)) and self.min_divider(increased_number) > 20:
                    divs[1] = increased_number
                elif not (self.check_primary(decreased_number)) and self.min_divider(decreased_number) > 20:
                    divs[1] = decreased_number
            if divs[2] == 1:
                if increased_number % 2 == 1:
                    divs[2] = increased_number
                elif decreased_number % 2 == 1:
                    divs[2] = decreased_number
            if divs[3] == 1:
                if increased_number % 2 == 0:
                    divs[3] = increased_number
                elif decreased_number % 2 == 0:
                    divs[3] = decreased_number

            if divs[0] != 1 and divs[1] != 1 and divs[2] != 1 and divs[3] != 1:
                break

        return tuple(divs)

    def check_primary(self, _number):
        for i in range(2, int(sqrt(_number))):
            if _number % i == 0:
                return False
        return True

    def min_divider(self, _number):
        for i in range(2, _number // 2 + 1):
            if _number % i == 0:
                return i
        return 0


class MiddleSquareHashData(Data):
    def __init__(self, _size, _max_element):
        super().__init__(_size, _max_element)

    def hash(self, type_of_cutting=1):
        if type_of_cutting in [1, 2]:   
            temp_arr_cut = [-1] * self.size
            count_collisions = 0
            future_result = {}

            for i in range(self.size):
                index = self.get_index(self.array[i], self.size, type_of_cutting)
                if (temp_arr_cut[index] == -1) or (temp_arr_cut[index] == self.array[i]):
                    temp_arr_cut[index] = self.array[i]
                else:
                    count_collisions += 1
                if i / self.size in self.gaps:
                    future_result[i / self.size] = count_collisions
            future_result[1.00] = count_collisions

            return future_result
        else:
            raise Exception("Incorrect type of middle square hash")

    def get_index(self, number, need_size, types):
        square = number ** 2
        if square < need_size:
            return square
        else:
            square_len = int(log10(square) + 1)
            need_len = int(log10(self.size + 1))
            if types == 1:
                part = square // (10 ** ((square_len - need_len + 1) // 2))
            else:
                part = square // (10 ** ((square_len - need_len) // 2))
            index = part % (10 ** need_len)
            return index


class CloteHashData(Data):
    def __init__(self, _size, _max_element):
        super().__init__(_size, _max_element)

    def hash(self, type_of_clotting=2):
        if type_of_clotting in [1, 2]:
            temp_arr_clote = [-1] * self.size
            count_collisions = 0
            future_result = {}

            for i in range(self.size):
                index = self.get_index(self.array[i], self.size, type_of_clotting)

                if (temp_arr_clote[index] == -1) or (temp_arr_clote[index] == self.array[i]):
                    temp_arr_clote[index] = self.array[i]
                else:
                    count_collisions += 1
                if i / self.size in self.gaps:
                    future_result[i / self.size] = count_collisions
            future_result[1.00] = count_collisions

            return future_result
        else:
            raise Exception("Incorrect type of clote hash")

    def get_index(self, number, need_size, types):
        if types == 1:
            temp = 0
            while number > need_size:
                temp += number // (10 ** int(log10(number) + 1 - log10(need_size + 1)))
                number %= (10 ** int(log10(number) + 1 - log10(need_size + 1)))
            temp += number
            return temp % need_size
        else:
            temp = 0
            while number != 0:
                temp += number % need_size
                number //= need_size
            return temp % need_size


class MultiplyHashData(Data):
    def __init__(self, _size, _max_element, _plural1, _plural2, _plural3, _plural4):
        super().__init__(_size, _max_element)
        self.plurals = [_plural1, _plural2, _plural3, _plural4]

    def hash(self, type_of_plural=1):
        if type_of_plural in [1, 2, 3, 4]:
            temp_arr_plural = [-1] * self.size
            count_collisions = 0
            future_result = {}

            for i in range(self.size):
                index = int(len(temp_arr_plural) * ((self.array[i] * self.plurals[type_of_plural - 1]) % 1))
                if temp_arr_plural[index] == -1 or temp_arr_plural[index] == self.array[i]:
                    temp_arr_plural[index] = self.array[i]
                else:
                    count_collisions += 1
                if i / self.size in self.gaps:
                    future_result[i / self.size] = count_collisions
            future_result[1.00] = count_collisions

            return future_result
        else:
            raise Exception("Incorrect type of plural hash")


class ConvertNumberSystemHashData(Data):
    def __init__(self, _size, _max_element, _system1, _system2, _system3, _system4):
        super().__init__(_size, _max_element)
        self.systems = [_system1, _system2, _system3, _system4]

    def hash(self, type_of_system=1):
        if type_of_system in [1, 2, 3, 4]:
            temp_arr_system = [-1] * self.size
            count_collisions = 0
            future_result = {}

            for i in range(self.size):
                index = self.get_index(self.array[i], self.size, self.systems[type_of_system - 1])

                if temp_arr_system[index] == -1 or temp_arr_system[index] == self.array[i]:
                    temp_arr_system[index] = self.array[i]
                else:
                    count_collisions += 1
                if i / self.size in self.gaps:
                    future_result[i / self.size] = count_collisions
            future_result[1.00] = count_collisions

            return future_result
        else:
            raise Exception("Incorrect type of convert number system hash")

    def get_index(self, number, need_size, system):
        temp = 0
        plural = 1
        while number > 0:
            temp += number % 10 * plural
            plural *= system
            number //= 10

        return temp % need_size
