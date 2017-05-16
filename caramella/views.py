# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from models import *
import datetime
import time

# Create your views here.
def index(request):
    return render_to_response('index.html', RequestContext(request))

def cargarLatas(request):
    return render_to_response('cargarLatas.html', RequestContext(request))

def remito(request):
    return render_to_response('Remito.html', RequestContext(request))

def verStock(request):
    return render_to_response('verStock.html', RequestContext(request))

def clientes(request):
    if request.is_ajax():
        if "addCliente" in request.POST:
            band = Cliente.objects.filter(razon_social = request.POST.get('razon_social')).count()
            band1 = Cliente.objects.filter(cuit = request.POST.get('cuit')).count()
            if band == 0 and band1 == 0:
                precio = float(request.POST.get('precio'))
                cliente = Cliente.objects.create(razon_social = request.POST.get('razon_social'), cuit = request.POST.get('cuit'), precio = precio, direccion = request.POST.get('dir'), telefono = request.POST.get('tel'), localidad = request.POST.get('local'))
                cliente.save()
                data = {'error':"EL cliente se agrego satisfactoriamente", 'cliente':{'id':cliente.id, 'razon_social':cliente.razon_social, 'cuit':cliente.cuit}}
                return JsonResponse(data)
            return JsonResponse({'error':"No se pudo agregar el cliente por que ya existe uno con esa Razon Social o ese CUIT..."})
        elif "rmvCliente" in request.POST:
            cliente = Cliente.objects.get(id__exact = request.POST.get('id'))
            cliente.delete()
            return JsonResponse({'error':"Cliente eliminado con exito..."})
        elif "modCliente" in request.POST:
            cliente = Cliente.objects.get(id__exact = request.POST.get('id'))
            data = {'cliente':{'id':cliente.id, 'razon_social':cliente.razon_social, 'cuit':cliente.cuit, 'local':cliente.localidad, 'dir':cliente.direccion, 'tel':cliente.telefono, 'precio':cliente.precio}}
            return JsonResponse(data)
        elif "saveCliente" in request.POST:
            cliente = Cliente.objects.get(id__exact = request.POST.get('id'))
            cliente.razon_social = request.POST.get('razon_social')
            cliente.precio = request.POST.get('precio')
            cliente.direccion = request.POST.get('dir')
            cliente.telefono = request.POST.get('tel')
            cliente.cuit = request.POST.get('cuit')
            cliente.localidad = request.POST.get('local')
            cliente.save()
            data = {'error':"Nuevos datos del cliente guardados con exito...", 'cliente':{'id':cliente.id, 'razon_social':cliente.razon_social, 'cuit':cliente.cuit}}
            return JsonResponse(data)
    clientes = Cliente.objects.all()
    return render_to_response('clientes.html', {'clientes':clientes}, RequestContext(request))
