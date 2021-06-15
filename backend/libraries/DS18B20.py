class DS18B20:
	def __init__(self, address, sensor_object):
		self.sensor_file_name = f"/sys/bus/w1/devices/{address}/w1_slave"
		self._sensor_object = sensor_object

	def read_temperature(self):
		sensor_file = open(self.sensor_file_name, 'r')

		for line in sensor_file:
			if 't=' in line:
				foundIndex = line.find('t=')+2
				temp = int(line[foundIndex:]) / 1000

		sensor_file.close()

		return temp

	def get_db_object(self):
		return self._sensor_object