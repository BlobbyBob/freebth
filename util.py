import re

from TimeSlots import Weekday

section_regex = re.compile('([0-9\\-]+)$')
timeinfo_regex = re.compile('^(\\w+) .+ --- ([0-9]+):([0-9]+) - ([0-9]+):([0-9]+)')


def parse_section_meta(schedule):
    sectioned = False
    max_section = 0

    for details in schedule:
        sectioninfo = details[2]
        if 'Hallenteil' in sectioninfo:
            sectioned = True
            try:
                sections = section_regex.search(sectioninfo).groups()[0]
                if '-' in sections:
                    max_section = max(max_section, int(sections.split('-')[1]))
                else:
                    max_section = max(max_section, int(sections))
            except:
                print("Unexpected format of section descriptor: '" + sectioninfo + "'")

    return sectioned, max_section


def parse_sections(sectioninfo):
    sections = list()
    groups = section_regex.search(sectioninfo).groups()
    if len(groups) > 0:
        info = groups[0]
        if '-' in info:
            parts = info.split('-')
            min_section = int(parts[0])
            max_section = int(parts[1])
            for i in range(min_section, max_section + 1):
                sections.append(i)
        else:
            sections.append(int(info))
    else:
        print("Unexpected format of section descriptor: '" + sectioninfo + "'")

    return sections


def parse_into_timeslots(timeslots, timeinfo, event_type):
    # Only look at regular events
    if 'regelmäßiger' in event_type:
        day_str, starthour, startmin, endhour, endmin = timeinfo_regex.search(timeinfo).groups()
        days = {
            "Montag": Weekday.MONDAY,
            "Dienstag": Weekday.TUESDAY,
            "Mittwoch": Weekday.WEDNESDAY,
            "Donnerstag": Weekday.THURSDAY,
            "Freitag": Weekday.FRIDAY,
            "Samstag": Weekday.SATURDAY,
            "Sonntag": Weekday.SUNDAY,
        }
        if day_str in days:
            day = days[day_str]
            timeslots.block((day, int(starthour), int(startmin)),
                            (day, int(endhour), int(endmin)))
        else:
            print("Unknown day descriptor: " + day_str)
