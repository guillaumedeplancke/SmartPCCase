from models.SensorHistory import SensorHistory
from datetime import datetime


class Sensor:

	def __init__(self, id, name, unit, input_bus, input_pin, category_id):
		self._id = id
		self.name = name
		self.unit = unit
		self.input_bus = input_bus
		self.input_pin = input_pin
		self.category_id = category_id

	@property
	def id(self):
		return self._id

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		if type(value) == str and value != "":
			self._name = value
		else:
			raise ValueError("Geen geldige sensor naam!")

	@property
	def unit(self):
		return self._unit

	@unit.setter
	def unit(self, value):
		if type(value) == str and value != "":
			self._unit = value
		else:
			raise ValueError("Geen geldige sensor eenheid!")

	@property
	def input_bus(self):
		return self._input_bus

	@input_bus.setter
	def input_bus(self, value):
		if type(value) == str and value != "":
			self._input_bus = value
		else:
			raise ValueError("Geen geldige sensor bus!")

	@property
	def input_pin(self):
		return self._input_pin

	@input_pin.setter
	def input_pin(self, value):
		if type(value) == int or type(value) == str:
			self._input_pin = value
		else:
			raise ValueError("Geen geldige sensor pin!")

	@property
	def category_id(self):
		return self._category_id

	@category_id.setter
	def category_id(self, value):
		if type(value) == int and value >= 0:
			self._category_id = value
		else:
			raise ValueError("Geen geldige sensor category_id!")

	@property
	def hardware_object(self):
		if hasattr(self, '_hardware_object'):
			return self._hardware_object
		else:
			return None

	@hardware_object.setter
	def hardware_object(self, object):
		self._hardware_object = object

	@property
	def latest_value(self):
		if hasattr(self, '_latest_value'):
			return self._latest_value
		else:
			return 0

	@latest_value.setter
	def latest_value(self, value):
		if type(value) == int or type(value) == float:
			self._latest_value = value
		else:
			raise ValueError("Geen geldige sensor value")

	def create_history_entry(self, value):
		date = datetime.now().date()
		time = datetime.now().time()

		self.latest_value = value

		history_item = SensorHistory(0, self.id, value, date, time)
		return history_item.save()
	
