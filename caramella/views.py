# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from models import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import datetime
import time
import serial
import base64
from subprocess import call    

def index(request):
    return render_to_response('index.html', RequestContext(request))

def cargarLatas(request):
    grupos = Grupo.objects.all()
    gru_gus = []
    for i in range(len(grupos)):
        gustos = Gusto.objects.filter(grupo = grupos[i], activo = True)#Agregar aca para que solamente me muestre los gustos activos
        agregar = [grupos[i],gustos]
        gru_gus.append(agregar)
    fecha = time.strftime("%d/%m/%Y")
    ultimo_id = 0
    try:
        ultimo = Lata.objects.latest('id')
        ultimo_id = ultimo.id
    except:
        pass
    if request.is_ajax():
        if "imprimir" in request.POST:
            try:
                peso = float(request.POST.get('peso'))#Descomentar esto para que cuando tenga la balanza conectada funcione: float(request.POST.get('peso'))
                lote = str(request.POST.get('lote'))
                gusto = Gusto.objects.get(id__exact = request.POST.get('gusto'))
                codigo = str(request.POST.get('codigo'))
                lata = Lata.objects.create(peso = peso, codigo = codigo, gusto = gusto, lote = lote, en_stock = True)
                lata.save()
                img_data = b''+request.POST.get('imagen')
                img_data = base64.b64decode(img_data)
                path = default_storage.save('etiqueta.png', ContentFile(img_data))
                try:
                    call(["lp","media/"+path])
                except:
                    return JsonResponse({'titulo':"Error imprimiendo",'error':"Hubo un error imprimiendo la etiqueta. Asegurese de que la impresora esta bien conectada, tiene papel y si esta encendida"})
                default_storage.delete(path)
                return JsonResponse({'titulo':"Etiqueta impresa",'error':"La etiqueta fue impresa con exito, retirela de la impresora y peguela en la lata de helado",'ultimo_id':"+1"})
            except:
                return JsonResponse({'titulo':"Error creando etiqueta",'error':"Hubo un error creando la etiqueta"})
        if "obtenerPeso" in request.POST:
            try:
                ser = serial.Serial()  # open serial port
                ser.port = '/dev/ttyUSB0'
                ser.baudrate = 9600
                ser.bytesize = serial.EIGHTBITS
                ser.parity = serial.PARITY_NONE
                ser.stopbits = serial.STOPBITS_ONE
                ser.open()
                print(ser.name)         # check which port was really used
                try:
                    ser.write(b'\x05')     # write a string
                    peso = ''
                    for i in range(7):
                        out = ser.read()
                        print out
                        if i==0 or i==8:
                            peso = peso
                        elif i==3:
                            peso = peso+out+"."
                        else:
                            peso = peso+out
                    peso = float(peso)
                    print peso
                    ser.close()
                    return JsonResponse({'peso':str(peso)})
                except:
                    return JsonResponse({'titulo':"Espere...",'error':"Espere a que el peso se estabilice sobre la balanza."})
            except:
                return JsonResponse({'titulo':"Error de conexión",'error':"Compruebe que la balanza este encendida y que el cable USB este bien conectado."})
    return render_to_response('cargarLatas.html', {'grupos':gru_gus, 'fecha':fecha, 'ultimo_id':ultimo_id}, RequestContext(request))

def remito(request):
    clientes = Cliente.objects.all()
    fecha = time.strftime("%d/%m/%Y")
    if request.is_ajax():
        codigo = request.POST.get('codigo')
        lata = ''
        try:
            lata = Lata.objects.get(codigo = codigo, en_stock = True)
        except:
            return JsonResponse({'titulo':"Error de lectura",'error':"El codigo ingresado no es reconocido por el sistema"})
        data = {"lata":{"id":lata.id, "codigo":lata.codigo, "gusto":lata.gusto.nombre, "peso":lata.peso}}
        return JsonResponse(data)
    return render_to_response('Remito.html', {'clientes':clientes, 'fecha':fecha}, RequestContext(request))

def verStock(request):
    return render_to_response('verStock.html', RequestContext(request))

def clientes(request):
    if request.is_ajax():
        if "addCliente" in request.POST:
            band = Cliente.objects.filter(razon_social = request.POST.get('razon_social')).count()
            band1 = Cliente.objects.filter(cuit = request.POST.get('cuit')).count()
            if band == 0 and band1 == 0:
                precio = float(request.POST.get('precio'))
                cliente = Cliente.objects.create(razon_social = request.POST.get('razon_social'), cuit = request.POST.get('cuit'), precio = precio, direccion = request.POST.get('dir'), telefono = request.POST.get('tel'), localidad = request.POST.get('local'), activo = True)
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
