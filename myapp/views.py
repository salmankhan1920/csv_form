from django.shortcuts import render, redirect
from .forms import OrderForm
import csv
from django.http import HttpResponse
from django.http import FileResponse
from django.utils import timezone
from django.contrib import messages
import os




# def order_form(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.timing = timezone.now().time()
#             order.date = timezone.now().date()
#             order.save()
            
#             # Save to CSV
#             csv_file_path = 'orders.csv'
#             file_exists = os.path.isfile(csv_file_path)
            
#             with open(csv_file_path, 'a', newline='') as csvfile:
#                 writer = csv.writer(csvfile)
#                 if not file_exists:
#                     writer.writerow(['ID Name', 'Timing', 'Date', 'Order ID', 'Amount', 'Address Code', 'Cancel Status'])
#                 writer.writerow([order.id_name, order.timing, order.date, order.order_id, order.amount, order.address_code, order.cancel_status])
            
#             messages.success(request, 'Order submitted successfully!')
#             return redirect('order_form')  # Redirect to a fresh form
#     else:
#         form = OrderForm()
    
#     return render(request, 'order_form.html', {'form': form})


# def order_form(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             now = timezone.localtime(timezone.now())
#             order.timing = now.time()
#             order.date = now.date()
#             order.save()
            
#             # Save to CSV
#             csv_file_path = 'orders.csv'
#             file_exists = os.path.isfile(csv_file_path)
            
#             with open(csv_file_path, 'a', newline='') as csvfile:
#                 writer = csv.writer(csvfile)
#                 if not file_exists:
#                     writer.writerow(['ID Name', 'Timing', 'Date', 'Order ID', 'Amount', 'Address Code', 'Cancel Status'])
#                 writer.writerow([order.id_name, order.timing, order.date, order.order_id, order.amount, order.address_code, order.cancel_status])
            
#             messages.success(request, 'Order submitted successfully!')
#             return redirect('order_form')  # Redirect to a fresh form
#     else:
#         form = OrderForm()
    
#     return render(request, 'order_form.html', {'form': form})


# def order_form(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             now = timezone.localtime(timezone.now())
#             order.timing = now.time()
#             order.date = now.date()
#             order.save()
            
#             # Save to CSV
#             csv_file_path = 'orders.csv'
#             file_exists = os.path.isfile(csv_file_path)
            
#             with open(csv_file_path, 'a', newline='') as csvfile:
#                 writer = csv.writer(csvfile)
#                 if not file_exists:
#                     writer.writerow(['ID Name', 'Timing', 'Date', 'Order ID', 'Amount', 'Address Code', 'Cancel Status'])
                
#                 # Format the time without microseconds
#                 formatted_time = order.timing.strftime('%H:%M:%S')
                
#                 writer.writerow([order.id_name, formatted_time, order.date, order.order_id, order.amount, order.address_code, order.cancel_status])
            
#             messages.success(request, 'Order submitted successfully!')
#             return redirect('order_form')  # Redirect to a fresh form
#     else:
#         form = OrderForm()
    
#     return render(request, 'order_form.html', {'form': form})



def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            now = timezone.localtime(timezone.now())
            order.timing = now.time()
            order.date = now.date()
            order.save()
            
            # Save to CSV
            csv_file_path = 'orders.csv'
            file_exists = os.path.isfile(csv_file_path)
            
            with open(csv_file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(['ID Name', 'Timing', 'Date', 'Order ID', 'Amount', 'Address Code', 'Refresh Link', 'Cancel Status'])
                
                # Format the time without microseconds
                formatted_time = order.timing.strftime('%H:%M:%S')
                
                writer.writerow([
                    order.id_name,
                    formatted_time,
                    order.date,
                    order.order_id,
                    order.amount,
                    order.address_code,
                    order.refresh_link,  # Add the refresh link to the CSV
                    order.cancel_status
                ])
            
            messages.success(request, 'Order submitted successfully!')
            return redirect('order_form')  # Redirect to a fresh form
    else:
        form = OrderForm()
    
    return render(request, 'order_form.html', {'form': form})

    


def display_csv(request):
    csv_file_path = 'orders.csv'
    orders = []

    try:
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                orders.append(row)
    except FileNotFoundError:
        orders = []

    return render(request, 'display_csv.html', {'orders': orders})



# def download_csv(request):
#     csv_file_path = 'orders.csv'
#     if os.path.exists(csv_file_path):
#         with open(csv_file_path, 'rb') as fh:
#             response = FileResponse(fh, content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="orders.csv"'
#             return response
#     return HttpResponse("CSV file not found", status=404)


def download_csv(request):
    csv_file_path = 'orders.csv'
    if os.path.exists(csv_file_path):
        file = open(csv_file_path, 'rb')
        response = FileResponse(file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        return response
    return HttpResponse("CSV file not found", status=404)




