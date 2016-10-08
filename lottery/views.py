from django.shortcuts import render, redirect
from lottery.models import Lottery
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from datetime import timedelta
import random, json
from django.http import HttpResponse
import os
from django.conf import settings

# Create your views here.
def lottery(request):
    now = timezone.now()
    if request.method == 'POST':
        sn = request.POST['sn']
        try:
            myfile = request.FILES['myfile']
        except:
            myfile = ''
        if sn == '' or myfile == '' :
            return redirect('lottery')
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
    return render (request,template,{'total':total,'now':now})

def end(request):
    template = 'lottery/end.html'
    # get img was not null
    people = Lottery.objects.filter(img__contains='.',enabled=0)
    # data save to list
    people = list(people)
    # random it!
    random.shuffle(people)
    person = 0
    show_list = []
    if request.POST.get('number'):
        Lottery.objects.all().delete()
        reset = True
        number = int(request.POST['number'])
        for i in range(1, number+1):
            num = ('{:08}'.format(i))
            lottery = Lottery(sn=num)
            lottery.save()
        return render(request, template, {'reset': reset, 'number': number})

    if request.method == 'POST':
        # select anyone to view
        if request.POST.get('open'):
            print(request)
            if people:
                person = people.pop()
                person.enabled = 1
                person.save()
            else:
                person = None
            show_list = Lottery.objects.filter(enabled=1).order_by('update_dt')

            return render(request, template,{'person':person , 'show':show_list})
        elif request.POST.get('reset'):
            number = Lottery.objects.all().count()
            Lottery.objects.all().delete()
            pic_path = settings.MEDIA_ROOT
            print(pic_path)
            all_pic = os.listdir(pic_path)
            for pic in all_pic:
                os.remove(pic_path +'/'+ pic)
            reset = True
            for i in range(1, number + 1):
                num = ('{:08}'.format(i))
                lottery = Lottery(sn=num)
                lottery.save()
            return render(request, template, {'reset': reset, 'number': number})

    return render(request, template,{'person':person , 'show':show_list})

def api(request):
    if request.method == 'POST' or request.method == 'GET':
        people = Lottery.objects.filter(img__contains='.')
        data = []
        for person in people:
            x = {person.sn:{'url':person.img.url,'enabled':person.enabled}}
            data.append(x)
        return HttpResponse(json.dumps(data), content_type='application/json')