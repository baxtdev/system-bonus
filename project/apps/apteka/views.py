from datetime import datetime
from sqlite3 import paramstyle
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


from accounts.models import User
from .models import History, Manager
from accounts.forms import RegisterForm


# @login_required(login_url='main:login')
def index(request):
	return render(request, 'index.html')



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Теперь вы вошли как {username}.")
                return redirect("main:homepage")
            else:
                messages.error(
                    request, "Неправильное имя пользователя или пароль.")
        else:
            messages.error(
                request, "Неправильное имя пользователя или пароль.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из системы.")
    return redirect("main:homepage")



@login_required(login_url='main:login')
def find_customer(request):
    code = request.GET.get('search')
    if code:
        customer = User.objects.filter(code=code)
        if customer:
            return render(request, 'customer_about.html', {'customer': customer[0]})
        else:
            messages.error(request, "Пользователь не найден.")
            return redirect("main:homepage")
    else:
        messages.error(request, "Введите код пользователя.")
        return redirect("main:homepage")



@login_required(login_url='main:login')
def bonus_temp(request):
    code = request.GET.get('code')
    if code:
        customer = User.objects.filter(code=code)
        return render(request, 'customer.html',{'customer':customer[0]})

@login_required(login_url='main:login')
def bonus_take(request):
    if request.method == "POST":
        code = request.POST.get('code')
        bonus = request.POST.get('bonus')
        customer = User.objects.filter(code=int(code))
        if customer:
            try:
                customer[0].bonus -= int(bonus)
                # add history
                History.objects.create(
                    customer=customer[0],
                    manager=Manager.objects.get(id=request.user.id),
                    pharmacy=Manager.objects.get(id=request.user.id).pharmacy,
                    method=1,
                    bonus=bonus,
                    date=datetime.now(),
                )
                customer[0].save()

                messages.success(request, "Бонусы успешно списаны.")

                return render(request, 'customer_about.html', {'customer': customer[0]})
            except Manager.DoesNotExist:
                messages.error(request, "Вы не являетесь Продавцом аптеки")
                # return render(request, 'customer_about.html', {'customer': customer[0]})
                return redirect("main:logout")
                    
        else:
            messages.error(request, "Пользователь не найден.")
            return redirect("main:homepage")
    else:
        messages.error(request, "Пользователь не найден.")
        return redirect("main:homepage")



@login_required(login_url='main:login')
def cash_temp(request):
    code = request.GET.get('code')
    if code:
        customer = User.objects.filter(code=code)
        return render(request, 'cash.html',{'customer':customer[0]})


@login_required(login_url='main:login')
def add_cash(request):
    if request.method == "POST":
        code = request.POST.get('code')
        cash = request.POST.get('cash')
        customer = User.objects.filter(code=code)
        if customer:
            try:
            # add 3% to customer's bonus
                customer[0].bonus += int(cash) * 0.03
                # customer[0].save()
                # messages.success(request, "Деньги успешно приняты.")
                # add history
                History.objects.create(
                    customer=customer[0],
                    manager=Manager.objects.get(id=request.user.id),
                    pharmacy=Manager.objects.get(id=request.user.id).pharmacy,
                    method=0,
                    # - 3% to customer's bonus
                    bonus=int(cash) * 0.03,
                    date=datetime.now(),
                )
                customer[0].save()
                messages.success(request, "Деньги успешно приняты.")
                return render(request, 'customer_about.html', {'customer': customer[0]})
            except Manager.DoesNotExist:
                messages.error(request, "Пользоватеь ни имеет прав как Manager")
                # return render(request, 'customer_about.html', {'customer': customer[0]})
                return redirect("main:logout")
                 
        else:
            messages.error(request, "Пользователь не найден.")
            return redirect("main:homepage")
    else:
        messages.error(request, "Пользователь не найден.")
        return redirect("main:homepage")

@login_required(login_url='main:login')
def add_user(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Пользователь успешно зарегистрирован.")
			return redirect("main:homepage")
		messages.error(request, "Ошибка при регистрации.")
	form = RegisterForm()
	return render (request=request, template_name="register.html", context={"register_form":form})