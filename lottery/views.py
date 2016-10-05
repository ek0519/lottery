from django.shortcuts import render, redirect
from .models import Lottery
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from django.core.files.storage import FileSystemStorage
from django.utils import six, timezone
from datetime import datetime, timedelta

# Create your views here.
def lottery(request):
    now = timezone.now()
    if request.method == 'POST':
        print (request.POST)
        sn = request.POST['sn']
        file = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        url = fs.url(filename)
        lottery = get_object_or_None(Lottery,sn=sn,enabled=False)
        delta = timedelta(minutes=30)
        create_dt = lottery.create_dt
        print (create_dt)
        if (now - delta) < create_dt:
            if lottery:
                lottery.img = url
                lottery.save()
            else:
                return HttpResponse("輸入序號有誤，請回上一頁")
        else:
            return HttpResponse("時間已經超過30分鐘")
        return redirect('lottery')
    else:
        pass
    template = 'lottery/lottery.html'
    return render (request,template)