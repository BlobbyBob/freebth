from enum import IntEnum

slotcount = 24 * 12 * 7


class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __mul__(self, other):
        return int(self)


class TimeSlots:

    def __init__(self):
        # A slot for every 5 min of the day and every day of the week
        self.__slots = [False] * slotcount

    def block(self, starttime, endtime):
        """
        Block time slots
        :param starttime: tuple(startday, starthour, startmin)
        :param endtime: tuple(endday, endhour, endmin)
        :return:
        """
        startindex = starttime[0] * (24 * 12) + starttime[1] * 24 + starttime[2] // 5
        endindex = endtime[0] * (24 * 12) + endtime[1] * 24 + (endtime[2]) // 5

        for i in range(startindex, endindex, 1):
            self.__slots[i % slotcount] = True

    def is_free(self, time):
        index = time[0] * (24 * 12) + time[1] * 24 + time[2] // 5
        return not self.__slots[index]

    def slots(self):
        return self.__slots
