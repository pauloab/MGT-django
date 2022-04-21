from secrets import choice
from django.db import models
from django.contrib.auth.models import User

TIPO_TAREA = [
    ("TAR","Tarea"),
    ("REC","Recuperacion"),
    ("PRU","Prueba"),
    ("SUP","Examen Sup."),
    ("PRO","Proyecto"),
]

class Tarea(models.Model):
    nombre = models.CharField(null=False,blank=False, max_length=150)
    tipo = models.CharField( max_length=3, default=TIPO_TAREA[0][0], choices=TIPO_TAREA)
    notas_adicionales = models.TextField(blank=True, null=True)
    fecha_agregado = models.DateField(auto_now=True)
    fecha_tarea = models.DateTimeField(null=False, blank=False, auto_now=False)
    cancelado = models.BooleanField(blank=False, null=False, default=False)
    valor_acordado = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=5)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)

    def get_tipo(self):
        for item in TIPO_TAREA:
            if item[0] == self.tipo:
                return item[1]
        return "N/A"