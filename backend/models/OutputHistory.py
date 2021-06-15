from repositories.OutputHistoryRepository import OutputHistoryRepository
from datetime import date, time


class OutputHistory:

    def __init__(self, id, output_id, user_id, value, date, time):
        self._id = id
        self.output_id = output_id
        self.user_id = user_id
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
    def output_id(self):
        return self._output_id

    @output_id.setter
    def output_id(self, value):
        if type(value) == int and value >= 0:
            self._output_id = value
        else:
            raise ValueError("Geen geldige OutputHistory output_id!")

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if type(value) == int and value >= 0:
            self._user_id = value
        else:
            raise ValueError("Geen geldige OutputHistory user_id!")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if type(value) == int and value >= 0:
            self._value = value
        else:
            raise ValueError("Geen gelde value voor OutputHistory instance!")

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if type(value) == date:
            self._date = value
        else:
            raise ValueError("Geen geldige datum voor OutputHistory instance!")

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if type(value) == time:
            self._time = value
        else:
            raise ValueError("Geen geldige time voor OutputHistory instance!")

    def save(self):
        return OutputHistoryRepository.create(self)
