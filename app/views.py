from django.shortcuts import render
from urllib import parse
from .models import Station
from .models import ScheduledItem
from .models import Weekday
from .recording_logic import recording_logic


def index(request):
    stations = Station.objects.order_by('call_sign')
    days = Weekday.objects.order_by('value')
    context = {"stations": stations, "days": days}

    if request.method == 'POST':
        query_string = request.body.decode('utf8')
        payload = dict(parse.parse_qsl(query_string))
        payload = process_payload(payload)
        for day in payload['days']:
            item = ScheduledItem.objects.create_request(payload['radioStation'], payload['fileOutputName'], day,
                                                        payload['startTime'], payload['endTime'])
            item.save()
        context["message"] = "Recording Request Submitted"
        return render(request, 'app/index.html', context)

    if request.method == 'GET':
        return render(request, 'app/index.html', context)


def process_payload(payload):
    processed_payload = payload
    days = []
    for x in range(0, 7):
        try:
            processed_payload.pop(str(x))
            days.append(x)
        except KeyError:
            continue
    processed_payload["days"] = days
    return processed_payload


def process_request(payload):
    recording_logic.RecordingLogic(payload['radioStation'],
                                   payload['fileOutputName'],
                                   payload['startTime'],
                                   payload['endTime'])
