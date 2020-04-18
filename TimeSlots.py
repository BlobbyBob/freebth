from enum import IntEnum
from math import ceil, floor

slotcount = 24 * 12 * 7


class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __str__(self):
        if self == Weekday.MONDAY:
            return "Montag"
        elif self == Weekday.TUESDAY:
            return "Dienstag"
        elif self == Weekday.WEDNESDAY:
            return "Mittwoch"
        elif self == Weekday.THURSDAY:
            return "Donnerstag"
        elif self == Weekday.FRIDAY:
            return "Freitag"
        elif self == Weekday.SATURDAY:
            return "Samstag"
        elif self == Weekday.SUNDAY:
            return "Sonntag"


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
        startindex = starttime[0] * (24 * 12) + starttime[1] * 12 + floor(starttime[2] / 5)
        endindex = endtime[0] * (24 * 12) + endtime[1] * 12 + ceil(endtime[2] / 5)

        for i in range(startindex, endindex, 1):
            self.__slots[i % slotcount] = True

    def is_free(self, time):
        index = time[0] * (24 * 12) + time[1] * 12 + floor(time[2] / 5)
        return not self.__slots[index]

    def slots(self):
        return self.__slots

    def find_free(self, starttime, endtime, minslotsize=60):
        """
        Check if a free slot with the defined constraints is available
        :param starttime: tuple(starthour, startmin)
        :param endtime: tuple(endhour, endmin)
        :param minslotsize: minimum slot size wanted (in minutes)
        :return: String list of all slots in text form
        """

        slots = []
        minslots = ceil(minslotsize / 5)
        for day in Weekday:
            startindex = day * (24 * 12) + starttime[0] * 12 + floor(starttime[1])
            endindex = day * (24 * 12) + endtime[0] * 12 + ceil(endtime[1]) - 1
            slotsize = 0
            for i in range(startindex, endindex, 1):
                if self.__slots[i]:
                    if slotsize > minslots:
                        s = i - slotsize
                        hour = (s % (24 * 12)) // 12
                        minute = ((s % 12) * 5) % 60
                        length = slotsize * 5
                        slots.append(f"Freier Slot: {str(day)} ab {hour:02}:{minute:02} für {length} Minuten")
                    slotsize = 0
                else:
                    slotsize += 1
            if slotsize >= minslots:
                slotsize += 1
                s = endindex - slotsize + 1
                hour = (s % (24 * 12)) // 12
                minute = ((s % 12) * 5) % 60
                length = slotsize * 5
                slots.append(f"Freier Slot: {str(day)} ab {hour:02}:{minute:02} für {length} Minuten")

        return slots

    def print_day(self, day):
        print("Slots am " + str(day) + ":")
        for i in range(day * (24 * 12), (day + 1) * (24 * 12)):
            if i % 12 == 0:
                print(f"{(i % (24 * 12)) // 12:2} Uhr: ", end='')
            if self.__slots[i]:
                print('0', end='')
            else:
                print('.', end='')
            if i % 12 == 11:
                print()

    def html_preformatted(self):
        output = f"        {str(Weekday.MONDAY): <11}  {str(Weekday.TUESDAY): <11}  {str(Weekday.WEDNESDAY): <11}  " \
                 f"{str(Weekday.THURSDAY): <11}  {str(Weekday.FRIDAY): <11}  {str(Weekday.SATURDAY): <11}  " \
                 f"{str(Weekday.SUNDAY): <11}\n"
        output += "\n"
        for hour in range(0, 24):
            output += f"{hour:2} Uhr  "
            for day in range(0, 7):
                for slot in range(0, 11):
                    if self.__slots[day * (24 * 12) + hour * 12 + slot]:
                        output += "<span class='red'>&nbsp;</span>"
                    else:
                        output += "<span class='green'>&nbsp;</span>"
                if day != 6:
                    output += '  '
            output += '\n'
        return output
