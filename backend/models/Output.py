from models.OutputHistory import OutputHistory
from datetime import datetime
from RPi import GPIO


class Output:

    def __init__(self, id, name, description, icon, output_num, is_pwm, category_id):
        self._id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.output_num = output_num
        self.is_pwm = is_pwm
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
            raise ValueError("Geen geldige output naam!")

    @property
    def description(self):
        return self._description

    @name.setter
    def description(self, value):
        if type(value) == str and value != "":
            self._description = value
        else:
            raise ValueError("Geen geldige output description!")

    @property
    def icon(self):
        return self._icon

    @name.setter
    def icon(self, value):
        if type(value) == str and value != "":
            self._icon = value
        else:
            raise ValueError("Geen geldige output icon!")

    @property
    def output_num(self):
        return self._output_num

    @output_num.setter
    def output_num(self, value):
        if type(value) == int and value >= 0:
            self._output_num = value
        else:
            raise ValueError("Geen geldige output pin!")

    @property
    def is_pwm(self):
        return self._is_pwm

    @is_pwm.setter
    def is_pwm(self, value):
        if type(value) == bool:
            self._is_pwm = value
        else:
            raise ValueError("Geen geldige boolean voor is_pwm!")

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, value):
        if type(value) == int and value >= 0:
            self._category_id = value
        else:
            raise ValueError("Geen geldige output category_id!")

    @property
    def pwm_object(self):
        return self._pwm

    @pwm_object.setter
    def pwm_object(self, pwm):
        self._pwm = pwm

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
            raise ValueError("Geen geldige output value")

    def set_value(self, value):
        if self._is_pwm == False:
            if value > 1:
                value = 1

            GPIO.output(self._output_num, value)
        else:
            if value > 100:
                value = 100

            self._pwm.ChangeDutyCycle(value)

        self.create_history_entry(value)

    def create_history_entry(self, value):
        date = datetime.now().date()
        time = datetime.now().time()

        self.latest_value = value

        history_item = OutputHistory(0, self.id, 1, value, date, time)
        return history_item.save()
