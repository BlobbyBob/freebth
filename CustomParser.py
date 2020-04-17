from enum import Enum
from html.parser import HTMLParser


class _GymListParserState(Enum):
    INIT = 0
    ID = 1
    NAME = 2


class GymListParser(HTMLParser):
    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.infos = list()
        self.__state = _GymListParserState.INIT

    def handle_starttag(self, tag, attrs):
        if tag == 'td' and ('class', 'feld') in attrs:
            if self.__state == _GymListParserState.INIT:
                self.infos.append(list())
                self.__state = _GymListParserState.ID

    def handle_data(self, data):
        if self.__state == _GymListParserState.ID:
            self.infos[len(self.infos) - 1].append(data)
            self.__state = _GymListParserState.NAME
        elif self.__state == _GymListParserState.NAME:
            self.infos[len(self.infos) - 1].append(data)
            self.__state = _GymListParserState.INIT


class _ScheduleParserState(Enum):
    INIT = 0
    DESCRIPTION = 1
    EVENT = 2
    APPOINTMENTTYPE = 3


class ScheduleParser(HTMLParser):
    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.__state = _ScheduleParserState.INIT
        self.schedule = list()

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and ('class', 'tool_beschr') in attrs:
            if self.__state == _ScheduleParserState.INIT:
                self.schedule.append(list())
                self.__state = _ScheduleParserState.DESCRIPTION
        elif tag == 'br':
            if self.__state == _ScheduleParserState.DESCRIPTION:
                self.__state = _ScheduleParserState.EVENT
            elif self.__state == _ScheduleParserState.EVENT:
                self.__state = _ScheduleParserState.APPOINTMENTTYPE
            elif self.__state == _ScheduleParserState.APPOINTMENTTYPE:
                self.__state = _ScheduleParserState.INIT

    def handle_data(self, data):
        if self.__state == _ScheduleParserState.DESCRIPTION:
            self.schedule[len(self.schedule) - 1].append(data.strip('\n\r\t'))
        elif self.__state == _ScheduleParserState.APPOINTMENTTYPE:
            self.schedule[len(self.schedule) - 1].append(data.strip('\n\r\t'))
