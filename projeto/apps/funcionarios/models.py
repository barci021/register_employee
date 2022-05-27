from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from apps.departamentos.models import Departamento
from django.db.models import Sum
from django.core.mail import send_mail, mail_admins, send_mass_mail


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    departamentos = models.ManyToManyField(Departamento)
    imagem = models.ImageField()
    de_ferias = models.BooleanField(default=False)

    def get_absolute_url(self):
       return reverse('list_funcionarios')

    @property
    def total_horas_extra(self):
        total = self.registrohoraextra_set.filter(
            utilizada=False).aggregate(
            Sum('horas'))['horas__sum']
        return total or 0

    def save(self, *args, **kwargs):
        super(Funcionario, self).save(*args, **kwargs)

        send_mail(
           'Novo fucionario cadastrado',
           'o funcionario %s foi cadastrado' % self.nome,
            'from@example.com',
            ['to@example'],
            fail_silently=False,
        )


    def __str__(self):
        return self.nome