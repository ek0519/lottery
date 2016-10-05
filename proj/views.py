from django.shortcuts import render, redirect
from .models import Lottery
from django.http import HttpResponse
from annoying.functions import get_object_or_None
from django.core.files.storage import FileSystemStorage
from django.utils import six, timezone
from datetime import datetime, timedelta



def index(request):
    