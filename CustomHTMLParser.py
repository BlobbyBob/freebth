from enum import Enum
from html.parser import HTMLParser


class ParserState(Enum):
    INIT = 0
    ID = 1
    NAME = 2


class CustomHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.infos = []
        self.__state = ParserState.INIT

    def handle_starttag(self, tag, attrs):
        if tag == 'td' and ('class', 'feld') in attrs:
            if self.__state == ParserState.INIT:
                self.infos.append([])
                self.__state = ParserState.ID

    def handle_data(self, data):
        if self.__state == ParserState.ID:
            self.infos[len(self.infos) - 1].append(data)
            self.__state = ParserState.NAME
        elif self.__state == ParserState.NAME:
            self.infos[len(self.infos) - 1].append(data)
            self.__state = ParserState.INIT
