from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, AddStockForm
from django.contrib import messages
from .tools import get_stock_data
import requests
import pandas as pd
from django.http import JsonResponse
from bs4 import BeautifulSoup
from decimal import Decimal
from .models import Portfolio
@login_required(login_url='/login')
def index(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            stock = form.cleaned_data['stock']
            quantity = form.cleaned_data['quantity']
            at_bought = form.cleaned_data['at_bought']
            date_bought = form.cleaned_data['date_bought']
            type = form.cleaned_data['type']
            if stock in portfolio.stocks:
                portfolio.stocks[stock]['at_bought'] = format((portfolio.stocks[stock]['at_bought']*portfolio.stocks[stock]['quantity'] + float(at_bought)*int(quantity)) / (portfolio.stocks[stock]['quantity']+int(quantity)), '.2f')
                portfolio.stocks[stock]['quantity'] += int(quantity)
                portfolio.stocks[stock]['date_bought'] = str(date_bought)
                portfolio.stocks[stock]['type'] = type
                portfolio.total_invested = portfolio.total_invested + Decimal(at_bought)*int(quantity)
            else:
                portfolio.stocks[stock] = {
                    'quantity': int(quantity),
                    'at_bought': float(at_bought),
                    'date_bought': str(date_bought),
                    'type': type
                }
                portfolio.total_invested = portfolio.total_invested + Decimal(at_bought)*int(quantity)
            portfolio.save()
            return redirect('/')
    else:
        form = AddStockForm()
    return render(request, 'index.html', {'form': form, 'portfolio': portfolio})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create a blank portfolio for the user
            Portfolio.objects.create(user=user)
            
            # Log the user in and display success message
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('/')  # Redirect to a desired page after signup
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('/')  # Redirect to a desired page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required(login_url="login")
def stocks(request, stock_name):
    stock_name = stock_name.upper()
    try:
        data = get_stock_data(request, stock_name)
    except:
        messages.error(request, "Scrip has not been traded yet or not found.")
        return redirect('/')
    return render(request, "stocks.html", {"data": data})

def deleteStock(request, stock_name):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    portfolio.total_invested = portfolio.total_invested - Decimal(portfolio.stocks[stock_name]['at_bought'])*int(portfolio.stocks[stock_name]['quantity'])
    portfolio.stocks.pop(stock_name)
    portfolio.save()
    return redirect('/')
