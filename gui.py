import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

schedules = []


def compute_overview(starthour, startmin, endhour, endmin, slotsize):
    schedule_url = 'https://stadtplan.bonn.de/cms/cms.pl?Amt=Stadtplan&set=5_1_3_0&act=1&Drucken=1&meta=neu&sid=&suchwert='

    output = f"<h2>Freie Slots (Mindestgröße {slotsize} min) zwischen {starthour}:{startmin:02} und {endhour}:{endmin:02}</h2>"
    for schedule in schedules:
        if schedule['sectioned']:
            for i, timeslots in enumerate(schedule['timeslots']):
                freeslots = timeslots.find_free((starthour, startmin), (endhour, endmin), slotsize)
                if len(freeslots) > 0:
                    output += f"<b>{schedule['gymName']}</b> (Hallenteil {i + 1})<br>"
                    output += f"<small><a href='{schedule_url}{schedule['gymId']}' target='_blank'>Stadt Bonn</a> - " \
                              f"<a href='#details' onclick='return details(\"{schedule['gymId']}\")'>Schnellübersicht" \
                              f"</a></small>"
                    output += "<ul>"
                    for slot in freeslots:
                        output += f"<li>{slot}</li>"
                    output += "</ul>"
        else:
            freeslots = schedule['timeslots'].find_free((starthour, startmin), (endhour, endmin), slotsize)
            if len(freeslots) > 0:
                output += f"<b>{schedule['gymName']}</b>"
                output += f"<small><a href='{schedule_url}{schedule['gymId']}' target='_blank'>Stadt Bonn</a> - " \
                          f"<a href='#details' onclick='return details(\"{schedule['gymId']}\")'>Schnellübersicht" \
                          f"</a></small>"
                output += "<ul>"
                for slot in freeslots:
                    output += f"<li>{slot}</li>"
                output += "</ul>"

    return output


def compute_details(gym_id):
    for schedule in schedules:
        if schedule['gymId'] == gym_id:
            output = f"<h3>Übersicht für {schedule['gymName']}</h3>"
            if schedule['sectioned']:
                for i, timeslots in enumerate(schedule['timeslots']):
                    output += f"<h5>Hallenteil {i + 1}</h5>"
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
                    self.wfile.write(compute_overview(starthour, startmin, endhour, endmin, slotsize).encode('utf-8'))
        except:
            print("An error occured during the request.")


def start_webserver(port=2020):
    with socketserver.TCPServer(("", port), FreebthRequestHandler) as httpd:
        print("[INFO] Server listening on port", port)
        httpd.serve_forever()
    print("Stopped server.")
