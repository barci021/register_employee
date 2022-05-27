from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)

from django.views.generic.base import View, TemplateView

from .models import Funcionario
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


class FuncionariosList(ListView):
    model = Funcionario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_button'] = _("Employee report")
        return context


class FuncionarioEdit(UpdateView):
    model = Funcionario
    fields = ['nome', 'departamentos', 'de_ferias']


class FuncionarioDelete(DeleteView):
    model = Funcionario
    success_url = reverse_lazy('list_funcionarios')


class FuncionarioNovo(CreateView):
    model = Funcionario
    fields = ['nome', 'departamentos']

    def form_valid(self, form):
        funcionario = form.save(commit=False)
        username = funcionario.nome.split(' ')[0] + funcionario.nome.split(' ')[1]
        funcionario.empresa = self.request.user.funcionario.empresa
        funcionario.user = User.objects.create(username=username)
        funcionario.save()
        return super(FuncionarioNovo, self).form_valid(form)


class Render:
    @staticmethod
    def render(path: str, params: dict, filename: str):
        template = get_template(path)
        html = template.render(params)
        response = io.BytesIO()
        pdf = pisa.pisaDocument(
            io.BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(
                response.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)


class Pdf(View):

    def get(self, request):
        params = {
            'today': 'Variavel today',
            'sales': 'Variavel sales',
            'request': request,
        }
        return Render.render('funcionarios/relatorio.html', params, 'file')


class PdfDebug(TemplateView):
    template_name = 'funcionarios/relatorio.html'