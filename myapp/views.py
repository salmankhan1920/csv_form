from django.shortcuts import render, redirect
from .forms import OrderForm
import csv
from django.http import HttpResponse
from django.http import FileResponse
from django.utils import timezone
from django.contrib import messages
import os
from django.contrib.auth.decorators import login_required
from .models import OrderLog, Order
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings





def is_superuser(user):
    return user.is_superuser




@login_required
def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            now = timezone.localtime(timezone.now())
            order.timing = now.time()
            order.date = now.date()
            order.user = request.user
            order.save()
            
            # Create log entry
            OrderLog.objects.create(user=request.user, order=order, action="created")
            
            # Save to CSV
            save_to_csv(order, request.user)
            
            messages.success(request, 'Order submitted successfully!')
            return redirect('order_form')
    else:
        initial_data = {}
        if request.GET.get('clone') == 'true':
            last_order = Order.objects.filter(user=request.user).order_by('-id').first()
            if last_order:
                initial_data = {
                    'id_name': last_order.id_name,
                    'order_id': last_order.order_id,
                    'refresh_link': last_order.refresh_link,
                    'cancel_status': last_order.cancel_status,
                }
        form = OrderForm(user=request.user, initial=initial_data)
    
    # Get recent orders for the logged-in user
    recent_orders = Order.objects.filter(user=request.user).order_by('-date', '-timing')[:4]
    
    context = {
        'form': form,
        'recent_orders': recent_orders
    }
    
    return render(request, 'order_form.html', context)




def save_to_csv(order, user):
    #csv_file_path = 'orders.csv'
    csv_file_path = os.path.join(settings.BASE_DIR, 'orders.csv')
    file_exists = os.path.isfile(csv_file_path)
    
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['User', 'ID Name', 'Timing', 'Date', 'Order ID', 'Amount', 'Address Code', 'Refresh Link', 'Cancel Status'])
        
        # Format the time without microseconds
        formatted_time = order.timing.strftime('%H:%M:%S')
        
        writer.writerow([
            user.username,
            order.id_name,
            formatted_time,
            order.date,
            order.order_id,
            order.amount,
            order.address_code,
            order.refresh_link,
            order.cancel_status
        ])


@login_required
def user_logs(request):
    # Get all logs for the current user
    logs = OrderLog.objects.filter(user=request.user).order_by('-timestamp')
    
    # Get all orders for the current user
    orders = Order.objects.filter(user=request.user).order_by('-date', '-timing')
    
    context = {
        'logs': logs,
        'orders': orders,
    }

    return render(request, 'user_logs.html', context)








@user_passes_test(is_superuser)
@staff_member_required
def display_csv(request):
   # csv_file_path = 'orders.csv'
    csv_file_path = os.path.join(settings.BASE_DIR, 'orders.csv')
    orders = []

    try:
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                orders.append(row)
    except FileNotFoundError:
        orders = []

    return render(request, 'display_csv.html', {'orders': orders})






def download_csv(request):
    #csv_file_path = 'orders.csv'
    csv_file_path = os.path.join(settings.BASE_DIR, 'orders.csv')
    if os.path.exists(csv_file_path):
        file = open(csv_file_path, 'rb')
        response = FileResponse(file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        return response
    return HttpResponse("CSV file not found", status=404)




def signup_view(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # If so, redirect to the order form (or any other appropriate page)
        return redirect('order_form')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('order_form')
        else:
            messages.error(request, 'There was an error with your signup. Please try again.')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})






def login_view(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # If so, redirect to the order form (or any other appropriate page)
        return redirect('order_form')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # You can add a success message here if you want
            messages.success(request, 'You have successfully logged in.')
            return redirect('order_form')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')



@staff_member_required
def all_user_logs(request):
    logs = OrderLog.objects.all().order_by('-timestamp')
    return render(request, 'all_user_logs.html', {'logs': logs})



def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def user_count(request):
    users = User.objects.all().order_by('username')
    total_users = users.count()
    context = {
        'total_users': total_users,
        'users': users
    }
    return render(request, 'user_count.html', context)



def get_last_order(request):
    last_order = Order.objects.filter(user=request.user).order_by('-id').first()
    if last_order:
        return JsonResponse({
            'id_name': last_order.id_name,
            'order_id': last_order.order_id,
            'amount': last_order.amount,
            'address_code': last_order.address_code,
            'refresh_link': last_order.refresh_link,
            'cancel_status': last_order.cancel_status,
        })
    return JsonResponse({})


    