from django.shortcuts import render, redirect
from .models import Shoe
from .forms import RoomForm



# Create your views here.


def home(request):
    shoes = Shoe.objects.all()
    context = {'shoes': shoes}
    return render(request, 'base/home.html', context)


def createShoe(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/shoeform.html', context)


def checkout(request, pk):
    shoe = Shoe.objects.get(id=pk)
    form = RoomForm(instance=shoe)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=shoe)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/shoeform.html', context)


def updateShoe(request, pk):
    shoe = Shoe.objects.get(id=pk)
    form = RoomForm(instance=shoe)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=shoe)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'base/shoeform.html', context)

def deleteShoe(request, pk):
    shoe = Shoe.objects.get(id=pk)
    if request.method == 'POST':
        shoe.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': shoe})
