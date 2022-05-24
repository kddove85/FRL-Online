from django.shortcuts import render
from urllib import parse
from .models import Station
from .models import ScheduledItem
from .models import Weekday
from .recording_logic import recording_logic
from datetime import datetime


def index(request):
    stations = Station.objects.order_by('call_sign')
    days = Weekday.objects.order_by('value')
    scheduled_items = ScheduledItem.objects.order_by('day_of_the_week', 'start_time')
    context = {"stations": stations, "days": days, "scheduled_items": scheduled_items}

    if request.method == 'POST':
        query_string = request.body.decode('utf8')
        payload = dict(parse.parse_qsl(query_string))
        payload = process_payload(payload)
        for day in payload['days']:
            item = ScheduledItem.objects.create_request(payload['radioStation'], payload['fileOutputName'], day,
                                                        payload['startTime'], payload['endTime'])
            item.save()

            '''
            get all items in table scheduled items
            filter on Day of the week
            if there are any to record today, spin new thread to begin recording logic
            '''

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


# Need to make this run periodically
def get_next_scheduled_item():
    now = datetime.now()
    scheduled_items = ScheduledItem.objects.filter(day_of_the_week=now.weekday())
    scheduled_items = scheduled_items.filter(start_time__gte=now.strftime('%H:%M'))
    scheduled_items = scheduled_items.order_by('start_time')
    scheduled_item = scheduled_items.first()
    recording_logic.RecordingLogic(scheduled_item.url,
                                   scheduled_item.output_name,
                                   scheduled_item.start_time,
                                   scheduled_item.end_time)
