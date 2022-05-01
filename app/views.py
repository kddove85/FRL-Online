from django.shortcuts import render
from urllib import parse
from .models import Station
from .models import ScheduledItem
from .recording_logic import recording_logic
import threading


def index(request):
    if request.method == 'POST':
        stations = Station.objects.order_by('call_sign')
        query_string = request.body.decode('utf8')
        payload = dict(parse.parse_qsl(query_string))
        item = ScheduledItem.objects.create_request(payload['radioStation'], payload['fileOutputName'],
                                                    payload['startTime'], payload['endTime'])
        item.save()
        context = {"stations": stations, 'message': "Recording Request Submitted"}
        return render(request, 'app/index.html', context)

    if request.method == 'GET':
        stations = Station.objects.order_by('call_sign')
        context = {"stations": stations}
        return render(request, 'app/index.html', context)


def process_request(payload):
    recording_logic.RecordingLogic(payload['radioStation'],
                                   payload['fileOutputName'],
                                   payload['startTime'],
                                   payload['endTime'])
