from smbus import SMBus
import time

class LCD:
	def __init__(self, i2c_address):
		self.__RS = 0b00000001
		self.__RW = 0b00000010
		self.__E = 0b00000100

		self.__i2c_address = i2c_address

		self.__i2c = SMBus()
		self.__i2c.open(1)

		self.init()

	def init(self):
		self.__expander_write(0x08) # reset display and set expander value to ON

		# first try
		self.__write_4_bits(0x30)
		time.sleep(0.0045)

		# second try
		self.__write_4_bits(0x30)
		time.sleep(0.0045)

		# third try
		self.__write_4_bits(0x30)
		time.sleep(0.00015)

		self.__write_4_bits(0x20) # set to 4-bit mode

		self.__send(0x0f, True) # display on & cursor blinking

		self.__send(0x28, True) # function set: 4 bit mode with 2 lines

		self.clear()

	def __send(self, value, command_mode):
		if command_mode is True:
			mode = 0
		else:
			mode = self.__RS
		
		high = value & 0xf0
		low = (value << 4) & 0xf0
		
		self.__write_4_bits(high | mode)
		self.__write_4_bits(low | mode)

	def __write_4_bits(self, value):
		self.__expander_write(value)
		self.__pulse_enable(value)

	def __expander_write(self, value):
		self.__i2c.write_byte(self.__i2c_address, value | 0x08) # send value with backlight enabled

	def __pulse_enable(self, value):	
		self.__expander_write(value | self.__E)
		time.sleep(0.000001)

		self.__expander_write(value & ~self.__E)
		time.sleep(0.00005)

	def clear(self):
		self.__send(0x01, True) # clear display & cursor home
		time.sleep(0.0005)

	def write_character(self, char):
		self.__send(ord(char), False)

	def write_message(self, message):
		for char in message:
			if char == '°':
				print('oofff')
				print(ord(char))
			self.write_character(char)

	def set_cursor(self, row, col):
		data = row << 6 | col
		self.__send(data | 128, True)

	def enable_cursor(self):
		self.__send(0x0f, True)

	def disable_cursor(self):
		self.__send(0x0c, True)

	def scroll_display(self):
		self.__send(0x18, True)	