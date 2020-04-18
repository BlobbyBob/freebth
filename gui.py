import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

from TimeSlots import Weekday

schedules = []


def compute_overview(starthour, startmin, endhour, endmin, slotsize, days):
    schedule_url = 'https://stadtplan.bonn.de/cms/cms.pl?Amt=Stadtplan&set=5_1_3_0&act=1&Drucken=1&meta=neu&sid=&suchwert='

    output = "<h2>Freie Slots (Mindestgröße %s min) zwischen %s:%02s und %s:%02s</h2>" % (slotsize, starthour, startmin, endhour, endmin)
    for schedule in schedules:
        if schedule['sectioned']:
            for i, timeslots in enumerate(schedule['timeslots']):
                freeslots = timeslots.find_free((starthour, startmin), (endhour, endmin), slotsize, days)
                if len(freeslots) > 0:
                    output += "<b>%s</b> (Hallenteil %s)<br>" % (schedule['gymName'], i+1)
                    output += "<small><a href='%s%s' target='_blank'>Stadt Bonn</a> - " % (schedule_url, schedule['gymId'])
                    output += "<a href='#details' onclick='return details(\"%s\")'>Schnellübersicht</a></small>" % schedule['gymId']
                    output += "<ul>"
                    for slot in freeslots:
                        output += "<li>%s</li>" % slot
                    output += "</ul>"
        else:
            freeslots = schedule['timeslots'].find_free((starthour, startmin), (endhour, endmin), slotsize, days)
            if len(freeslots) > 0:
                output += "<b>%s</b><br>" % schedule['gymName']
                output += "<small><a href='%s%s' target='_blank'>Stadt Bonn</a> - " % (schedule_url, schedule['gymId'])
                output += "<a href='#details' onclick='return details(\"%s\")'>Schnellübersicht</a></small>" % schedule['gymId']
                output += "<ul>"
                for slot in freeslots:
                    output += "<li>%s</li>" % slot
                output += "</ul>"

    return output


def compute_details(gym_id):
    for schedule in schedules:
        if schedule['gymId'] == gym_id:
            output = "<h3>Übersicht für %s</h3>" % schedule['gymName']
            if schedule['sectioned']:
                for i, timeslots in enumerate(schedule['timeslots']):
                    output += "<h5>Hallenteil %s</h5>" % (i+1)
                    output += "<pre>"
                    output += timeslots.html_preformatted()
                    output += "</pre>"
            else:
                output += "<pre>"
                output += schedule['timeslots'].html_preformatted()
                output += "</pre>"
            output += "<style>.red{background-color:red;}.green{background-color:green}</style>"
            return output

    return 'Nichts gefunden'


class FreebthRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            requested = self.requestline.split(' ')[1]

            if 'github.png' in requested:
                self.send_response(200, "OK")
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                with open('github.png', 'rb') as f:
                    self.wfile.write(f.read())
                return

            self.send_response(200, "OK")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            if '?' not in requested:
                with open('index.html', 'rb') as f:
                    self.wfile.write(f.read())
            else:
                url = urlparse(requested)
                parameters = parse_qs(url.query)

                if 'details' in parameters:
                    self.wfile.write(compute_details(parameters['details'][0]).encode('utf-8'))
                else:
                    starthour = 9
                    startmin = 0
                    endhour = 22
                    endmin = 0
                    slotsize = 60
                    if 'shour' in parameters:
                        starthour = int(parameters['shour'][0])
                    if 'smin' in parameters:
                        startmin = int(parameters['smin'][0])
                    if 'ehour' in parameters:
                        endhour = int(parameters['ehour'][0])
                    if 'emin' in parameters:
                        endmin = int(parameters['emin'][0])
                    if 'slot' in parameters:
                        slotsize = int(parameters['slot'][0])
                    days = list()
                    if 'days' in parameters:
                        days_param = parameters['days'][0].split('.')
                        for i in range(0, 7):
                            if str(i) in days_param:
                                days.append(Weekday(i))
                    self.wfile.write(compute_overview(starthour, startmin, endhour, endmin, slotsize, days).encode('utf-8'))
        except:
            print("An error occured during the request.")


def start_webserver(port=2020):
    with socketserver.TCPServer(("", port), FreebthRequestHandler) as httpd:
        print("[INFO] Server listening on port", port)
        httpd.serve_forever()
    print("Stopped server.")
