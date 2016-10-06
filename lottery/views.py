from django.shortcuts import render, redirect
from lottery.models import Lottery
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from datetime import timedelta
import random, json
from django.http import HttpResponse

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
        lottery = get_object_or_None(Lottery, sn=sn)
        if lottery == None:
            return HttpResponse('此序號不再此次活動中，請重新輸入')
        lottery = get_object_or_None(Lottery,sn=sn,enabled=False)
        if lottery == None:
            return HttpResponse('該序號已經有人使用，請重新輸入')
        else:
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
    all = Lottery.objects.all()
    total = all.count()
    now = all.filter(img__contains='.').count()
    print(now)
    return render (request,template,{'total':total,'now':now})

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

def api(request):
    if request.method == 'POST' or request.method == 'GET':
        people = Lottery.objects.filter(img__contains='.')
        print(people)
        data = []
        for person in people:
            x = { 'sn':person.sn,
                  'url':person.img.url,
                  'enabled':person.enabled}
            data.append(x)
        return HttpResponse(json.dumps(data), content_type='application/json')