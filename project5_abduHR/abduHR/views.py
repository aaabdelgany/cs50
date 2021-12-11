from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User,Employee
import csv,re,io



# class NewPostForm(forms.Form):
#     content=forms.CharField(label="New Post",widget=forms.Textarea)


def index(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("landing"))
        else:
            return render(request, "abduHR/index.html", {
                "message": "Invalid username and/or password."
            })
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("landing"))
    return render(request, "abduHR/index.html")
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "abduHR/index.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "abduHR/index.html")
def test(request):
    if request.method=="POST":
        return JsonResponse({"test":"yup"}, status=201)
    return JsonResponse({"test":"yup"}, status=200)

@login_required
def export(request):
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="Employee export.csv"'  
    employees = Employee.objects.all()  
    writer = csv.writer(response)  
    for employee in employees:
        print(employee.first_name)
        writer.writerow([employee.first_name,employee.last_name,employee.email,employee.phone,employee.active])
    return response

@login_required
def impemp(request):
    if request.method=="GET":
        return render(request,"abduHR/impemp.html")
    csv_file=request.FILES['file'].read().decode("utf-8")
    lines=csv_file.split("\n")
    reader=csv.reader(lines)
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    phone_regex='\d{10}'
    for row in reader:
        try:
            if not re.search(phone_regex,row[3].strip()):
                return render(request,"abduHR/impemp.html",{
                    "message":"Your import file contains asdasdinvalid phone number(s). Phone numbers must be entered in 10 digit numeric format"
                    #testing nah
                })
            if not re.search(email_regex,row[2].strip()):
                return render(request,"abduHR/impemp.html",{
                    "message":"Your import file contains invalid email(s). Please review your email column to correct your email format"
                })
            new_employee=Employee(first_name=row[0].strip(),last_name=row[1].strip(),email=row[2].strip(),phone=row[3].strip(),active=row[4].strip())
            try:
                new_employee.save()
            except IntegrityError:
                return render(request,"abduHR/impemp.html",{
                    "message":"Your import filzzze is remapping a users email to one that is already taken. Please review your email column to make sure you are using unique emails"
                })
        except IndexError:
            return render(request,"abduHR/update.html",{
                    "message":"Your import file contains incomplete data. Please make sure that the file is using columns 1-5 correctly test pull"
                })
    
    return HttpResponseRedirect(reverse("landing"))

@login_required
def update(request):
    if request.method=="GET":
        return render(request,"abduHR/update.html")
    csv_file=request.FILES['file'].read().decode("utf-8")
    lines=csv_file.split("\n")
    reader=csv.reader(lines)
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    phone_regex='\d{10}'
    for row in reader:
        if len(row)==0:
            break #for files that have empty rows
        try:
            if not re.search(phone_regex,row[3].strip()):
                return render(request,"abduHR/update.html",{
                    "message":"Your import file contains invalid phone number(s). no ty Phone numbers must be entered in 10 digit numeric format"
                })
            if not re.search(email_regex,row[2].strip()):
                return render(request,"abduHR/update.html",{
                    "message":"Your import file contains invalid email(s). Please review your email column to correct your email format"
                })
            
            update_employee=Employee.objects.get(email=row[2].strip())
            update_employee.first_name=row[0].strip()
            update_employee.last_name=row[1].strip()
            update_employee.phone=row[3].strip()
            update_employee.active=row[4].strip()
            try:
                update_employee.save()
            except IntegrityError:
                return render(request,"abduHR/update.html",{
                    "message":"Your import file is remapping a users email to one that is already taken. test. Please review your email column to make sure you are using unique emails"
                })
        except IndexError:
            return render(request,"abduHR/update.html",{
                "message":"Your import file contains incomplete data. Please make sure that the file is using columns 1-5 correctly test"
            }) 
    return HttpResponseRedirect(reverse("landing"))

@login_required
def edit(request,empid):
    employee=Employee.objects.get(id=empid)
    if request.method=="POST":
        data=json.loads(request.body)
        firstName=data.get("first_name").strip()
        lastName=data.get("last_name").strip()
        email=data.get("email").strip()
        phone=data.get("phone").strip()
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        status_flag=data.get("status_flag")
        status_update=0
        if not re.search(email_regex,email):
            return JsonResponse({"message":"Please enter a valid email"}, status=500)
        phone_regex='\d{10}'
        if not re.search(phone_regex,phone):
            return JsonResponse({"message":"Please enter a valid phone"}, status=500)
        employee.first_name=firstName
        employee.last_name=lastName
        employee.phone=phone
        employee.email=email
        if status_flag==True:
            employee.active=not employee.active
            status_update=1
        try:
            employee.save()
            return JsonResponse({"message":"Employee Updated","edit":1,"status_update":status_update},status=201)
        except IntegrityError:
            return JsonResponse({"message":"An employee already exists with that email"}, status=500)

    return render(request, "abduHR/edit.html",{
        "employee":employee
    })


@login_required
def inactive(request):
    employees=Employee.objects.filter(active=False)
    num_page=request.GET.get('num')
    try:
        paginator=Paginator(employees,num_page)
    except TypeError:
        paginator=Paginator(employees,10)
    page=request.GET.get('page',1)
    try:
        emps=paginator.page(page)
    except PageNotAnInteger:
        emps = paginator.page(1)
    except EmptyPage:
        emps = paginator.page(paginator.num_pages)

    return render(request, "abduHR/inactive.html",{
        "employees":emps
    })

@login_required
def search(request):
    if request.method=="GET":
        return HttpResponseRedirect(reverse("landing"))
    email=request.POST.get("search")
    print(email)
    try:
        searched=Employee.objects.get(email=email)
        print('yes')
    except Employee.DoesNotExist:
        paginator=Paginator(Employee.objects.all(),10)
        emps = paginator.page(1)
        return render(request, "abduHR/landing.html",{
        "employees":emps,
        "message":"There is no employee with that email"
    })
    return HttpResponseRedirect(reverse('edit',args=[searched.id]))

@login_required
def landing(request):
    employees=Employee.objects.all()
    num_page=request.GET.get('num')
    try:
        paginator=Paginator(employees,num_page)
    except TypeError:
        paginator=Paginator(employees,10)
    page=request.GET.get('page',1)
    try:
        emps=paginator.page(page)
    except PageNotAnInteger:
        emps = paginator.page(1)
    except EmptyPage:
        emps = paginator.page(paginator.num_pages)

    return render(request, "abduHR/landing.html",{
        "employees":emps
    })
@login_required
def new(request):
    if request.method == "POST":
        data=json.loads(request.body)
        firstName=data.get("first_name").strip()
        lastName=data.get("last_name").strip()
        email=data.get("email").strip()
        phone=data.get("phone").strip()
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(email_regex,email):
            return JsonResponse({"message":"Please enter a valid email"}, status=500)
        phone_regex='\d{10}'
        if not re.search(phone_regex,phone):
            return JsonResponse({"message":"Please enter a valid phone"}, status=500)
        try:
            Employee.objects.get(email=email)
            return JsonResponse({"message":"An employee with that email already exists!"}, status=500)
        except Employee.DoesNotExist:
            new_emp=Employee(first_name=firstName,last_name=lastName,email=email,phone=phone,active=True)
            new_emp.save()
        return JsonResponse({"message":"New Employee added","new":1,"id":new_emp.id},status=201)
        #data.get("id")
    # post=Post.objects.get(id=data.get("id"))
    pass
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "abduHR/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "abduHR/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "abduHR/register.html")
