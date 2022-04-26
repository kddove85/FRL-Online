from django.shortcuts import render
from .models import Station
from .recording_logic import recording_logic


def index(request):
    if request.method == 'POST':
        stations = Station.objects.order_by('call_sign')
        recording_logic.RecordingLogic(request.POST['radioStation'],
                                       request.POST['fileOutputName'],
                                       request.POST['startTime'],
                                       request.POST['endTime'])
        context = {"stations": stations, 'status': "Recording Request Submitted"}
        return render(request, 'app/index.html', context)

    if request.method == 'GET':
        stations = Station.objects.order_by('call_sign')
        context = {"stations": stations}
        return render(request, 'app/index.html', context)
