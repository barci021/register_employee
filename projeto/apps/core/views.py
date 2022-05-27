from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response


@login_required
def home(request):
    data = {}
    data['usuario'] = request.user
    funcionario = request.user.funcionario
    data['total_funcionarios'] = funcionario.total_funcionarios
    data['total_funcionarios_ferias'] = funcionario.total_funcionarios_ferias
    data['total_funcionarios_doc_pendente'] = funcionario.total_funcionarios_doc_pendente
    data['total_funcionarios_doc_ok'] = funcionario.total_funcionarios_doc_ok
    data['total_funcionarios_rg'] = 10

    return render(request, 'core/index.html', data)


 # lendo e setando cookies
def view(request):
    response = render_to_response('index.html')
    response.set_cookie('testando_cookie', 'testando123')
    value = request.COOKIES.get('testando_cookie')
    print(value)
    return response
