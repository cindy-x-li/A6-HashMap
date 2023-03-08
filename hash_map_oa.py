# Name: Cindy Li
# OSU Email: lici@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/17/2023
# Description: The HashMap class is build on a dynamic array and uses
# open addressing, specifically quadratic probing, to stores key-value
# pairs.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #
    def calc_index(self, key: str, cap: int = None) -> int:
        if cap is None:
            return self._hash_function(key) % self._capacity
        else:
            return self._hash_function(key) % cap

    def quad_probe(self, initial_index: int, j: int) -> int:
        return (initial_index + j**2) % self._capacity

    def put(self, key: str, value: object) -> None:
        """Updates the key/value pair in the hash map. If the given key already exists,
        its associated value is updated to the new value. If the given key is absent,
        a new key/value pair must be added.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # initial insertion
        index = self.calc_index(key)
        if self._buckets[index] is None:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        elif self._buckets[index].is_tombstone is True:
            self._buckets[index].is_tombstone = False
            self._size += 1
        # checks for already existing key
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            self._buckets[index].value = value
        # checks for tombstones

        else:
            # insertion via quadratic probing starts after 1st attempt to insert fails
            increment = 1
            quad_index = self.quad_probe(index, increment)
            while self._buckets[quad_index] is not None:
                if self._buckets[quad_index].is_tombstone is True:
                    self._buckets[quad_index].is_tombstone = False
                    break
                elif self._buckets[quad_index].key == key:
                    self._buckets[quad_index].value = value
                    return
                increment += 1
                quad_index = self.quad_probe(index, increment)

            self._buckets[quad_index] = HashEntry(key, value)
            self._size += 1

    def table_load(self) -> float:
        """Returns the current hash table load factor.
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """Returns the number of empty buckets in the hash table
        """
        empty = 0
        for i in range(self._capacity):
            if self._buckets[i] is None:
                empty += 1

        return empty

    def resize_table(self, new_capacity: int) -> None:
        """Changes the capacity of the internal hash table.
        """
        if new_capacity < self._size:
            return

        if new_capacity != 2:
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity
        prev_buckets = self._buckets
        self._buckets = DynamicArray()
        self._size = 0

        for _ in range(self._capacity):
            self._buckets.append(None)

        for i in range(prev_buckets.length()):
            entry = prev_buckets[i]
            if entry is not None and entry.is_tombstone is False:
                self.put(entry.key, entry.value)

    def get(self, key: str) -> object:
        """Returns the value associated with the given key
        """

        # initial search
        index = self.calc_index(key)
        if self._buckets[index] is None:
            return None
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            return self._buckets[index].value
        else:
            # quadratic probing starts after 1st search attempt fails
            increment = 1
            quad_index = self.quad_probe(index, increment)
            while self._buckets[quad_index] is not None:
                # if self._buckets[quad_index].is_tombstone is True:
                #     return None
                if self._buckets[quad_index].key == key:
                    return self._buckets[quad_index].value
                increment += 1
                quad_index = self.quad_probe(index, increment)

        return None

    def contains_key(self, key: str) -> bool:
        """Checks if a given key is in the hash map.
                Return true if key exists. Otherwise, False.
                """
        if self.get(key) is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """Removes key/value pair from the hash map
        """
        index = self.calc_index(key)
        if self._buckets[index] is None:
            return
        elif self._buckets[index].key == key:
            if self._buckets[index].is_tombstone is False:
                self._buckets[index].is_tombstone = True
                self._size -= 1
            else:
                return
        else:
            # quadratic probing starts after 1st search attempt fails
            increment = 1
            quad_index = self.quad_probe(index, increment)
            while self._buckets[quad_index] is not None:
                if self._buckets[quad_index].key == key:
                    if self._buckets[quad_index].is_tombstone is False:
                        self._buckets[quad_index].is_tombstone = True
                        self._size -= 1
                        break
                    else:
                        return
                increment += 1
                quad_index = self.quad_probe(index, increment)

    def clear(self) -> None:
        """Clears the contents of the hash map. Capacity is not affected.
                """
        for i in range(self._capacity):
            if self._buckets[i] is not None:
                self._buckets[i] = None
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """Returns a dynamic array where each index contains a tuple of a
        key/value pair stored in the hash map. Order does not matter.
        """
        da_new = DynamicArray()
        for i in range(self._capacity):
            value = self._buckets[i]
            if value is None:
                continue
            if value.is_tombstone is False:
                da_new.append((value.key, value.value))

        return da_new

    def __iter__(self):
        """ Create iterator for looping through HashMap object
        """
        self._index = 0
        return self

    def __next__(self):
        """Obtain next value and advance iterator.
        Returns active hash entries (i.e. not tombstones).
        """
        try:
            value = self._buckets[self._index]
            while value is None or value.is_tombstone is True:
                self._index = self._index + 1
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1

        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    '''
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    
    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())
    '''
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    m.put('some key', 'some value')
    m.remove('some key')
    print(m.get_size())
    m.remove('some key')
    print(m.get_size())
    # m.put('some key', 'some value')

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        # print(result)
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            if result is False:
                print(key, capacity, result)
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
            if result is False:
                print(key, "not", capacity, result)
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    '''
    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)
    
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    
    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())
    
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
    '''