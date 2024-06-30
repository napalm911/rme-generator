from const import OTBMNodeSpecialByte

class Byt3s:
    def __init__(self, data):
        self.data = bytearray(data)
        self.position = 0

    def read_byte(self, increment_position=True):
        val = self.data[self.position] & 0xFF
        if increment_position:
            self.position += 1
        return val

    def peek_byte(self):
        return self.data[self.position] & 0xFF

    def escape_read_byte(self, offset=None):
        return self._get_escaped_value(offset)

    def escape_read_uint16_le(self, offset=None):
        int1 = self._get_escaped_value(offset)
        int2 = self._get_escaped_value()
        return int1 | (int2 << 8)

    def escape_read_uint32_le(self, offset=None):
        int1 = self._get_escaped_value(offset)
        int2 = self._get_escaped_value()
        int3 = self._get_escaped_value()
        int4 = self._get_escaped_value()
        return (int1 | (int2 << 8) | (int3 << 16)) + (int4 * 0x1000000)

    def escape_peek_uint16_le(self, offset=None):
        int1 = self._get_escaped_value(offset, increment_position=False)
        int2 = self._get_escaped_value(offset + 1 if offset is not None else self.position + 1, increment_position=False)
        return int1 | (int2 << 8)

    def escape_read_string(self):
        length = self.escape_read_uint16_le()
        str_arr = [self.escape_read_byte() for _ in range(length)]
        return ''.join(map(chr, str_arr))

    def write_byte(self, value, offset=None):
        check_int(value, 0, 255)
        self.position = offset if offset is not None else self.position
        self.data[self.position] = value & 0xFF
        self.position += 1

    def escape_write_byte(self, value):
        if value in (OTBMNodeSpecialByte.START.value, OTBMNodeSpecialByte.END.value, OTBMNodeSpecialByte.ESCAPE_CHAR.value):
            self.write_byte(OTBMNodeSpecialByte.ESCAPE_CHAR.value)
        self.write_byte(value)

    def escape_write_uint16_le(self, value):
        int1 = value & 0xFF
        int2 = value >> 8
        self.escape_write_byte(int1)
        self.escape_write_byte(int2)

    def escape_write_uint32_le(self, value):
        int1 = value & 0xFF
        int2 = value >> 8
        int3 = value >> 16
        int4 = value >> 24
        self.escape_write_byte(int1)
        self.escape_write_byte(int2)
        self.escape_write_byte(int3)
        self.escape_write_byte(int4)

    def escape_write_string(self, str_val):
        check_string(str_val)
        length = len(str_val)
        self.escape_write_uint16_le(length)
        for char in str_val:
            self.escape_write_byte(ord(char))

    def _get_escaped_value(self, offset=None, increment_position=True):
        backup_position = self.position
        self.position = offset if offset is not None else self.position
        if (self.data[self.position] == OTBMNodeSpecialByte.ESCAPE_CHAR.value and
            self.data[self.position + 1] in (OTBMNodeSpecialByte.START.value, OTBMNodeSpecialByte.END.value, OTBMNodeSpecialByte.ESCAPE_CHAR.value)):
            self.read_byte(increment_position)
            val = self.read_byte(increment_position)
        else:
            val = self.read_byte(increment_position)
        self.position = backup_position if not increment_position else self.position
        return val

def check_int(value, min_val, max_val):
    if not isinstance(value, int):
        raise NotAnIntError(value)
    if value < min_val or value > max_val:
        raise IntSizeError(value, min_val, max_val)

def check_string(str_val):
    if not isinstance(str_val, str):
        raise NotAStringError(str_val)

class NotAStringError(Exception):
    def __init__(self, str_val):
        super().__init__(f'Not a string. Got a: {type(str_val)}')
        self.code = 'NOT_STR'

class NotAnIntError(Exception):
    def __init__(self, value):
        super().__init__(f'Not an integer. Got: {value}')
        self.code = 'NOT_INT'

class IntSizeError(Exception):
    def __init__(self, value, min_val, max_val):
        super().__init__(f'Integer is out of bounds. Received {value} but integer has to be between {min_val} and {max_val}')
        self.code = 'INT_BOUNDS'
