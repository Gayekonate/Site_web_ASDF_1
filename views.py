from django.shortcuts import render, redirect
from api.adhesion import get_all_users, Adhesion



def index(request):
    return render(request, 'membres/index.html', {'membres': get_all_users()})


def add_membre(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone_number = request.POST.get("phone_number")
    mail = request.POST.get("mail")
    address = request.POST.get("address")

    membre = Adhesion(first_name, last_name, phone_number, mail, address)
    membre.save()
    return redirect('index')