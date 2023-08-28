from django.shortcuts import render
from BD_NP import path
from BD_NP import upgrade_me

path('upgrade/', upgrade_me, name='upgrade')
# Create your views here.
