
class Time:

    def __init__(self):

        self.day = 1
        self.month = 1
        self.year = 2020
        self.time = 480
        self.hour = self.time // 60
        self.minute = self.time - (self.hour * 60)

        self.max_time = 1440
        self.max_day = 30
        self.max_month = 12

    def print(self):
        hour_temp = self.time//60
        minute_temp = self.time - (hour_temp*60)
        print("{0}:{1} {2}/{3}/{4}".format(hour_temp, minute_temp, self.day, self.month, self.year))

    def str(self):
        hour_temp = self.time // 60
        minute_temp = self.time - (hour_temp * 60)
        return "{}/{}/{} {}:{}:00".format(self.day, self.month, self.year, hour_temp, minute_temp)

    def do_step(self, i):
        self.time = self.time + 1
        self.hour = self.time // 60
        self.minute = self.time - (self.hour * 60)

        if self.time > self.max_time:
            self.day = self.day + 1
            self.time = 1
            if self.day > self.max_day:
                self.month = self.month + 1
                self.day = 1
                if self.month > self.max_month:
                    self.year = self.year + 1