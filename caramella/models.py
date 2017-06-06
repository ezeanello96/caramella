# -*- coding: utf-8 -*-
from django.db import models

class Grupo(models.Model):
    nombre = models.CharField("Nombre", max_length=20)
    
    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ("nombre",)
        
    def __unicode__(self):
	    return self.nombre
    
class Gusto(models.Model):
    nombre = models.CharField("Nombre", max_length=20)
    grupo = models.ForeignKey(Grupo)
    rna = models.CharField("Nro RNA", max_length=50)
    rne = models.CharField("Nro RNE", max_length=50)
    activo = models.BooleanField("Gusto activo")
    #ingredientes = models.ManyToManyField(Ingrediente)
    
    class Meta:
        verbose_name = 'Gusto'
        verbose_name_plural = 'Gustos'
        ordering = ("grupo","nombre",)
        
    def __unicode__(self):
        return self.grupo.nombre + " - " + self.nombre
    
class Cliente(models.Model):
    razon_social = models.CharField("Razon Social", max_length=50)
    precio = models.FloatField("Precio por Kilogramo")
    direccion = models.CharField("Dirección", max_length=40)
    telefono = models.CharField("Telefono", max_length=20)
    cuit = models.CharField("CUIT", max_length=20)
    localidad = models.CharField("Localidad", max_length=20)
    activo = models.BooleanField("Cliente activo")
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ("cuit","razon_social",)
        
    def __unicode__(self):
        return self.cuit + " - " + self.razon_social
    

class Lata(models.Model):
    peso = models.FloatField("Peso")
    codigo = models.CharField("Codigo de barras", unique=True, max_length=255)
    gusto = models.ForeignKey(Gusto)
    lote = models.CharField("Lote", max_length=20)
    fecha_elab = models.DateField("Fecha de elaboración", auto_now_add=True)
    en_stock = models.BooleanField("En stock")
    
    class Meta:
        verbose_name = 'Lata'
        verbose_name_plural = 'Latas'
        ordering = ("codigo","lote","gusto",)
        
    def __unicode__(self):
        return  self.codigo + " - " + str(self.fecha_elab)
    
    def sacarPrecio(self, precio_kg):
        precio = self.peso * float(precio_kg)
        return precio
    
    def descripcion(self):
        return self.gusto.nombre + " - " + self.codigo

class Remito(models.Model):
    fecha = models.DateField("Fecha")
    cliente = models.ForeignKey(Cliente)
    latas = models.ManyToManyField(Lata)
    archivo = models.FileField("Archivo", upload_to='remitos/')
    
    class Meta:
        verbose_name = 'Remito'
        verbose_name_plural = 'Remitos'
        ordering = ("fecha","cliente")
        
    def __unicode__(self):
        return str(self.fecha) + " - " + self.cliente.razon_social
    
    def nombreArchivo(self):
        return str(self.fecha+"-"+self.cliente.razon_social)+".xlsx"
