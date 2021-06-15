from repositories.SensorHistoryRepository import SensorHistoryRepository
from datetime import date, time

class SensorHistory:

	def __init__(self, id, sensor_id, value, date, time):
		self._id = id
		self.sensor_id = sensor_id
		self.value = value
		self.date = date
		self.time = time

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, value):
		self._id = value

	@property
	def sensor_id(self):
		return self._sensor_id

	@sensor_id.setter
	def sensor_id(self, value):
		if type(value) == int and value >= 0:
			self._sensor_id = value
		else:
			raise ValueError("Geen geldige SensorHistory sensor_id!")

	@property
	def value(self):
		return self._value
	
	@value.setter
	def value(self, value):
		if type(value) == float and value >= 0.00:
			self._value = value
		else:
			raise ValueError("Geen gelde value voor SensorHistory instance!")

	@property
	def date(self):
		return self._date

	@date.setter
	def date(self, value):
		if type(value) == date:
			self._date = value
		else:
			raise ValueError("Geen geldige datum voor SensorHistory instance!")

	@property
	def time(self):
		return self._time

	@time.setter
	def time(self, value):
		if type(value) == time:
			self._time = value
		else:
			raise ValueError("Geen geldige time voor SensorHistory instance!")

	def save(self):
		return SensorHistoryRepository.create(self)
