from django.shortcuts import render, redirect
from lottery.models import Lottery
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from datetime import datetime, timedelta
import random

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
    request.session['show'] =[]
    return render (request,template)

def end(request):
    template = 'lottery/end.html'
    # get img was not null
    people = Lottery.objects.filter(img__contains='.',enabled=0)
    # data save to list
    people = list(people)
    # random it!
    random.shuffle(people)
    person = 1
    show_list = []
    print(people)
    if request.method == 'POST':
        # select anyone to view
        if people:
            person = people.pop()
            person.enabled = 1
            person.save()
        else:
            person = None
        show_list = Lottery.objects.filter(enabled=1).order_by('update_dt')
        print('_______')
        print(show_list)

        return render(request, template,{'person':person , 'show':show_list})

    return render(request, template,{'person':person , 'show':show_list})