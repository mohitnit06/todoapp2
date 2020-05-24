from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.
def input(request):
    return render(request, 'generator/input.html')

def password_generated(request):
    generated_password = ''

    characters = list('abcdefghijklmnopqrstuvwxyz')
    uppercase_characters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    special_characters = list('@#$')
    numbers = list('1234567890')

    password_length = int(request.GET.get('length',12))

    if request.GET.get('uppercase'):
        characters.extend(uppercase_characters)

    if request.GET.get('numbers'):
        characters.extend(numbers)

    if request.GET.get('special'):
        characters.extend(special_characters)

    for x in range(password_length):
        generated_password += random.choice(characters)

    return render(request, 'generator/password_generated.html',{'password' : generated_password})
