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
from helados import settings
#Aca importo librerias externas a Django que seran utilizadas en el software
#import serial
import xlsxwriter
import base64
from subprocess import call    

def index(request):
    return render_to_response('index.html', RequestContext(request))

def getLote(date):
    d1 = datetime.datetime.strptime(date, "%d/%m/%Y")
    d2 = datetime.datetime.strptime(settings.LOTE[1], "%d/%m/%Y")
    lote = settings.LOTE[0]+abs((d2 - d1).days)
    lote = str(lote)
    if len(lote) == 1:
        lote = "000"+lote
    elif len(lote) == 2:
        lote = "00"+lote
    elif len(lote) == 3:
        lote = "0"+lote
    else:
        lote = lote
    return lote

def cargarLatas(request):
    fecha = time.strftime("%d/%m/%Y")
    lote = getLote(str(fecha))
    grupos = Grupo.objects.all()
    gru_gus = []
    for i in range(len(grupos)):
        gustos = Gusto.objects.filter(grupo = grupos[i], activo = True)#Agregar aca para que solamente me muestre los gustos activos
        agregar = [grupos[i],gustos]
        gru_gus.append(agregar)
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
    return render_to_response('cargarLatas.html', {'grupos':gru_gus, 'fecha':fecha, 'ultimo_id':ultimo_id, 'lote':lote}, RequestContext(request))

def hacerEncabezado(cliente, remito, worksheet, fecha):
    worksheet.set_column('B:B', 45)
    worksheet.set_column('A:A', 20)
    worksheet.set_column('C:C', 25)
    worksheet.set_column('D:D', 40)
    worksheet.write(0, 1, u"Razón Social:")
    worksheet.write(0, 2, "Vitali Maria Evangelina")
    worksheet.write(1, 1, u"Télefono:")
    worksheet.write(1, 2, "03547-421270")
    worksheet.write(2, 1, "Fax:")
    worksheet.write(3, 1, "Cod. Postal:")
    worksheet.write(3, 2, "5186")
    worksheet.write(4, 1, "Direccion:")
    worksheet.write(4, 2, "Lucas V cordoba 281")
    worksheet.write(0, 3, "CUIT:")
    worksheet.write(0, 4, "27-6787892-1")
    worksheet.write(0, 6, "REMITO")
    nro = Remito.objects.all().count()
    worksheet.write(1, 6, nro)
    worksheet.write(2, 6, "Fecha: "+fecha)
    worksheet.write(6, 0, u"Señor/es:")
    worksheet.write(7, 0, "Nombre: ")
    worksheet.write(7, 1, cliente.razon_social)
    worksheet.write(8, 0, "Domicilio: ")
    worksheet.write(8, 1, cliente.direccion)
    worksheet.write(9, 0, "Localidad: ")
    worksheet.write(9, 1, cliente.localidad)
    worksheet.write(10, 0, "CUIT: ")
    worksheet.write(10, 1, cliente.cuit)
    worksheet.write(7, 3, u"Télefono: ")
    worksheet.write(7, 4, cliente.telefono)
    worksheet.write(8, 3, "Provincia: ")
    worksheet.write(8, 4, u"Córdoba")
    worksheet.write(12, 0, u"Artículo")
    worksheet.write(12, 1, u"Descripción")
    worksheet.write(12, 2, u"Kilos")
    worksheet.write(12, 3, u"Importe")
    
def generarPie(worksheet, total, cant, row, kilos):
    worksheet.write(row, 0, u"Total")
    worksheet.write(row, 2, str(kilos))
    worksheet.write(row, 3, "$"+str(total))
    worksheet.write(row+1, 0, u"Cantidad total de latas retiradas: "+str(cant))
    
def remito(request):
    clientes = Cliente.objects.all()
    fecha = time.strftime("%d/%m/%Y")
    if request.is_ajax():
        if "codigo" in request.POST:
            codigo = request.POST.get('codigo')
            lata = ''
            try:
                lata = Lata.objects.get(codigo = codigo, en_stock = True)
            except:
                return JsonResponse({'titulo':"Error de lectura",'error':"El codigo ingresado no es reconocido por el sistema"})
            data = {"lata":{"id":lata.id, "codigo":lata.codigo, "gusto":lata.gusto.nombre, "peso":lata.peso}}
            return JsonResponse(data)
        elif "id_cliente" in request.POST:
            ids = request.POST.getlist('ids[]')
            cliente = Cliente.objects.get(id__exact = request.POST.get('id_cliente'))
            fecha = time.strftime("%Y-%m-%d")
            remito = Remito.objects.create(cliente = cliente, fecha = fecha, pesoTotal = 0.0, precioTotal = 0.0)
            archivo = 'media/remitos/'+remito.nombreArchivo()
            workbook = xlsxwriter.Workbook(archivo)
            worksheet = workbook.add_worksheet()
            hacerEncabezado(cliente, remito, worksheet, fecha)
            row = 13
            col = 0
            total = 0
            cant = 0
            kgs = 0
            for i in range(len(ids)):
                lata = Lata.objects.get(id__exact = ids[i])
                remito.latas.add(lata)
                worksheet.write(row, col, i+1)
                worksheet.write(row, col + 1, lata.descripcion())
                worksheet.write(row, col + 2, str(lata.peso)+" Kgs.")
                worksheet.write(row, col + 3, "$"+str(lata.sacarPrecio(cliente.precio)))
                row += 1
                cant += 1
                total += lata.sacarPrecio(cliente.precio)
                kgs += lata.peso
                lata.en_stock = False
                lata.save()
            generarPie(worksheet, total, cant, row, kgs)
            workbook.close()
            print kgs
            remito.pesoTotal = kgs
            remito.precioTotal = total
            remito.save()
            call(["gnumeric",archivo])
            return JsonResponse({'error':"Remito guardado. Encontrara el archivo en la siguiente ubicacion: ..."})
    return render_to_response('Remito.html', {'clientes':clientes, 'fecha':fecha}, RequestContext(request))

def getKilos(latas):
    totalKilos = 0.0
    for lata in latas:
        totalKilos += lata.peso
    return totalKilos
    
def verStock(request):
    latas = Lata.objects.filter(en_stock = True)
    gustos = Gusto.objects.filter(activo = True)
    totalLatas = len(latas)
    totalKilos = getKilos(latas)
    if request.method == 'POST':
        if "porGusto" in request.POST:
            gusto = Gusto.objects.get(id__exact = request.POST.get('selectGusto'))
            latas = Lata.objects.filter(en_stock = True, gusto = gusto)
            totalKilos = getKilos(latas)
            totalLatas = len(latas)
            return render_to_response('verStock.html', {'latas':latas, 'totalLatas':totalLatas, 'totalKilos':totalKilos, 'gustos':gustos, 'busqueda':"gustos ("+gusto.nombre+")"}, RequestContext(request))
        elif "porLote" in request.POST:
            lote = request.POST.get('lote')
            latas = Lata.objects.filter(en_stock = True, lote = lote)
            totalKilos = getKilos(latas)
            totalLatas = len(latas)
            return render_to_response('verStock.html', {'latas':latas, 'totalLatas':totalLatas, 'totalKilos':totalKilos, 'gustos':gustos, 'busqueda':"lote ("+lote+")"}, RequestContext(request))
    return render_to_response('verStock.html', {'latas':latas, 'totalLatas':totalLatas, 'totalKilos':totalKilos, 'gustos':gustos}, RequestContext(request))

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

def stats(request):
    fechaDesde, fechaHasta = None, None
    clientes = Cliente.objects.all()
    resultado = []
    kilos = 0.0
    totalKilos = 0.0
    for i in range(len(clientes)):
        kilos = 0.0
        if not request.method == 'POST':
            remitos = clientes[i].remito_set.all()
        else:
            fechaDesde = datetime.datetime.strptime(request.POST['fechaDesde'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
            fechaHasta = datetime.datetime.strptime(request.POST['fechaDesde'] + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
            remitos = clientes[i].remito_set.filter(fecha__range=[fechaDesde, fechaHasta])
            fechaDesde = fechaDesde.strftime("%Y-%m-%d")
            fechaHasta = fechaHasta.strftime("%Y-%m-%d")
        for j in range(len(remitos)):
            kilos += remitos[j].pesoTotal
        totalKilos += kilos
        kilos = ("%.3f" % round(kilos,3))
        resultado.append({'cliente':clientes[i].razon_social, 'cantidad': kilos})
    totalKilos = ("%.3f" % round(totalKilos,3))
    return render_to_response('estadisticas.html', {'resultado':resultado, 'totalKilos':totalKilos, 'fechaDesde':fechaDesde, 'fechaHasta':fechaHasta}, RequestContext(request))
