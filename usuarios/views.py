from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
       username = request.POST.get('username')
       email = request.POST.get('email')
       senha = request.POST.get('senha')
       confirmarsenha = request.POST.get('confirmar_senha')

       if senha != confirmarsenha:
           messages.add_message(request, constants.ERROR, 'A Senha e a Confirmação de Senha, não conferem!' )
           return redirect('/usuarios/cadastro')
       
       if len(senha) < 6:
           messages.add_message(request, constants.ERROR, 'A Senha deve ter 6 ou mais Caracteres!' )
           return redirect('/usuarios/cadastro')   
       
       users = User.objects.filter(username = username)
       
       if users.exists():
           messages.add_message(request, constants.ERROR, f'Usuário {username} já existente!' )
           return redirect('/usuarios/cadastro')           
       
       user = User.objects.create_user(
           username = username, 
           password= senha, 
           email= email)
       
       return redirect('/usuarios/login')
    
def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username= request.POST.get('username')
        senha= request.POST.get('senha')

        user = auth.authenticate(request, username=username, password = senha)

        if user:
            auth.login(request, user)
            return redirect('/pacientes/home')

        messages.add_message(request, constants.ERROR, 'Usuário ou Senha Inválidos!' )
        return redirect('/usuarios/login')
        

def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')