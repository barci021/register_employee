from django.db import models
from django.urls import reverse



class Departamento(models.Model):
    nome = models.CharField(max_length=70)

    def get_absolute_url(self):
        return reverse('list_departamentos')

    def __str__(self):
        return self.nome