from django.shortcuts import render, redirect
from django.http import HttpResponse

def return_product(request):
    if request.method == "POST":
        # Simulate processing the return
        return redirect('return_success')  # Redirect to the success page
    return render(request, 'returns/return_form.html')

def return_success(request):
    return HttpResponse("Product returned successfully!")  # Success message
