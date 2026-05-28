from email.message import EmailMessage
import random
import smtplib
import ssl
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.shortcuts import render,redirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from datetime import *
from django.utils import timezone

from ctapp.models import *
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os
import math
from django.db.models import Count
from .models import PoliceStation, District
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.
def _parse_coordinate(value):
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def index(request):
    today = date.today()
    return render(request,'index.html',{'today':today})
def user_login(request):
     return render(request,'login.html')
def user_registration(request):
     today = date.today()
     return render(request,'user_registration.html',{'today':today})
# def user_registration(request):
  
#     return render(request,'user_registration.html',{'today':today})
def admin_logout(request):
    logout(request)
    request.session.delete()
    return redirect('user_login')
def user_logout(request):
    logout(request)
    request.session.delete()
    return redirect('user_login')
def user_action(request):
   
    username=request.POST.get("username")
    username_exists = Login.objects.filter(username=username).exists() or User.objects.filter(username=username).exists()
    data = {
    'username_exists': username_exists,
    'error': "Username Already Exists" if username_exists else ""
    }
    if(data["username_exists"]==False):
        tbl1=Login()
        username=request.POST.get("username")
        tbl1.username=request.POST.get("username")
        password=request.POST.get("password")
        tbl1.password=password
        tbl1.user_type="User"
        tbl1.status="Approved"
        tbl1.save()
        obj=Login.objects.get(username=username,password=password)

        u=UserInfo()

        u.login_id = obj.login_id
        u.name=request.POST.get("Name")
        u.phone_number =request.POST.get("phone")
        u.email_id=request.POST.get("Email")
        u.dob=request.POST.get("dob")
        u.address=request.POST.get("address")
       
        u.save()
        messages.add_message(request, messages.INFO, 'Registered successfully.')
        return redirect('user_registration')
    else:
        messages.add_message(request, messages.INFO, 'User name is already Exist. Sorry Registration Failed.')
        return redirect('user_registration')
def login_action(request):
    u=request.POST.get("username")
    p=request.POST.get("password")
    obj=authenticate(username=u,password=p)
    if obj is not None:
        if obj.is_superuser == 1:
            request.session['aname'] = u
            request.session['slogid'] = obj.id
            return redirect('admin_home')
        else:
          messages.add_message(request, messages.INFO, 'Invalid User.')
          return redirect('user_login')
    else:
        newp=p
        try:
            obj1=Login.objects.get(username=u,password=newp)

            if obj1.user_type=="User":
                if(obj1.status=="Approved"):
                    request.session['uname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('user_home')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('user_login')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('user_login')
            elif obj1.user_type=="Police":
                if(obj1.status=="Approved"):
                    request.session['pname'] = u
                    request.session['slogid'] = obj1.login_id
                    return redirect('police_home')
                elif(obj1.status=="Not Approved"):
                  messages.add_message(request, messages.INFO, 'Waiting For Approval.')
                  return redirect('user_login')
                else:
                  messages.add_message(request, messages.INFO, 'Invalid User.')
                  return redirect('user_login')
            elif obj1.user_type == "PoliceStation":
                if obj1.status == "Approved":
                    request.session["stname"] = u
                    request.session["slogid"] = obj1.login_id
                    return redirect("station_home")
                elif obj1.status in ["Submitted", "Not Approved"]:
                    messages.add_message(request, messages.INFO, "Waiting For Approval.")
                    return redirect("user_login")
                else:
                    messages.add_message(request, messages.INFO, "Invalid User.")
                    return redirect("user_login")
            else:
                 messages.add_message(request, messages.INFO, 'Invalid User.')
                 return redirect('user_login')
        except Login.DoesNotExist:
         messages.add_message(request, messages.INFO, 'Invalid User.')
         return redirect('user_login') 
def admin_home(request):
    if 'aname' in request.session:
       
        return render(request, 'Master/index.html')
    
    else:
      return redirect('user_login')
def user_home(request):
    if 'uname' in request.session:
        user = get_user(request.session["slogid"])
        chat_rooms = _decorate_chat_rooms(_ensure_user_chat_rooms(user), "user")
        active_chat_room = chat_rooms[0] if chat_rooms else None
        return render(
            request,
            'User/index.html',
            {
                "user_data": user,
                "chat_rooms": chat_rooms[:5],
                "chat_room_count": len(chat_rooms),
                "active_chat_room": active_chat_room,
            },
        )
    
    else:
      return redirect('user_login')
  
def save_category(request):
    if 'aname' in request.session:
        
        tbl=Category()
        tbl.category=request.POST.get("category")
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('add_category')
    else:
        return redirect('login')
def add_category(request):
 if 'aname' in request.session:
    data=Category.objects.all()
    return render(request,'Master/category.html',{'data':data})
 else:
      return redirect('login')
def edit_category(request,id):
 if 'aname' in request.session:
    data=Category.objects.get(category_id=id)
    return render(request,'Master/edit_category.html',{'data':data})
 else:
      return redirect('login')


def update_category(request,id):
 if 'aname' in request.session:
    tbl=Category.objects.get(category_id=id)
    tbl.category=request.POST.get("category")
    tbl.save()
    messages.add_message(request, messages.INFO, 'Updated successfully.')
    return redirect('add_category')
 else:
      return redirect('login')
def delete_category(request,id):
 if 'aname' in request.session:
    tbl=Category.objects.get(category_id=id)
    tbl.delete()
    messages.add_message(request, messages.INFO, 'Deleted successfully.')
    return redirect('add_category')
 else:
      return redirect('login')
           
      
def users_list(request):
    if 'aname' in request.session:
     data=UserInfo.objects.all()
     return render(request,'Master/users_list.html',{'data':data})
    else:
      return redirect('user_login')
 
def profile(request):
    if 'uname' in request.session:
        data=get_user(request.session['slogid'])
       
        return render(request,'User/profile.html',{'data':data})
    else:
       return redirect('user_login')
    # ----------------End Feedback -------------------------------------------------



def add_complaints(request):
    if 'uname' in request.session:
            crime = Category.objects.all() 
            state = State.objects.all() 
            current_datetime = datetime.now()
            context = {'crime_types': crime,'state':state,'current_datetime': current_datetime}
            return render(request, 'User/add_complaints.html',context)
    else:
        return redirect('user_login')
def submit_complaint(request):
    if 'uname' in request.session:
                        
                user=get_user(request.session['slogid'])
                category_id = request.POST.get('crimeType')
                district_id = request.POST.get('district')
                police_station_id = request.POST.get('police_station')
                place = request.POST.get('place')
                subject = request.POST.get('subject')
                complaint_text = request.POST.get('complaintText')
                crime_datetime = request.POST.get('crimeDatetime')
                latitude = _parse_coordinate(request.POST.get("latitude"))
                longitude = _parse_coordinate(request.POST.get("longitude"))
           
                if latitude is None or longitude is None:
                    messages.add_message(request, messages.INFO, 'Please select a crime location on the map.')
                    return redirect('add_complaints')

                # Fetch related objects
                category = Category.objects.get(category_id=category_id)
                district = District.objects.get(district_id=district_id)
                police_station = PoliceStation.objects.filter(police_station_id=police_station_id).first()

                document = request.FILES.get('document')
                url1 = None

                if document:
                    split_tup = os.path.splitext(document.name)
                    file_extension = split_tup[1]
                    dir_path = settings.MEDIA_ROOT
                    count = 0
                    for path in os.listdir(dir_path):
                        if os.path.isfile(os.path.join(dir_path, path)):
                            count += 1
                    filecount=count+1
                    filename=str(filecount)+file_extension
                    obj=FileSystemStorage()
                    file=obj.save(filename,document)
                    url1=obj.url(file)
                # Save the complaint
                complaint = Crime.objects.create(
                    user=user,
                    category=category,
                    district=district,
                    police_station=police_station,
                    place=place,
                    subject=subject,
                    complaint_text=complaint_text,
                    crime_datetime=crime_datetime,
                    supporting_document=url1,
                    latitude = latitude,
                    longitude = longitude,
                    
                )
                
                # Redirect or send a success response
                messages.add_message(request, messages.INFO, 'Added successfully.')
                return redirect('add_complaints')
    else:
        return redirect('user_login')
def display_police_station(request):
    district_id = request.GET.get("district_id")
    try:

        dist = PoliceStation.objects.filter(district_id = district_id)
    except Exception:
        data=[]
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(dist.values('police_station_id', 'place')), safe = False)
def display_police(request):
    police_station_id = request.GET.get("police_station_id")
    try:

        dist = PoliceOfficer.objects.filter(police_station_id = police_station_id)
    except Exception:
        data=[]
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(dist.values('police_officer_id', 'name')), safe = False)
def view_complaints(request):
    if 'uname' in request.session:
            user=get_user(request.session['slogid'])
            crime=Crime.objects.filter(user=user)
            context = {'crime': crime,}
            return render(request, 'User/view_complaints.html',context)
    else:
        return redirect('user_login')
def crime_more(request,id):
    if 'uname' in request.session:
     
            crime=Crime.objects.get(pk=id)
            fir = FIR.objects.filter(crime_id=id).first() 
            
            context = {'crime': crime,'fir':fir}
            return render(request, 'User/crime_more.html',context)
    else:
        return redirect('user_login')
    

# ------------- Feedback ------------------------------------------


def feedback(request):
    if 'uname' in request.session:
        user=get_user(request.session['slogid'])
        data1 = Feedback.objects.filter(user=user)
        return render(request,'User/feedback.html',{'data1':data1})
    else:
       return redirect('user_login')
def save_feedback(request):
    if 'uname' in request.session:
        tbl=Feedback()
    
        tbl.user=UserInfo.objects.get(user_id=get_user(request.session['slogid']).user_id)
        # tbl.feedback_subject=request.POST.get("subject")
        tbl.feedback=request.POST.get("feedback")
        tbl.save()
        messages.add_message(request, messages.INFO, 'Added successfully.')
        return redirect('feedback')
    else:
       return redirect('user_login')

def delete_feedback(request,id):
    if 'uname' in request.session:
        tbl=Feedback.objects.get(feedback_id=id)
        tbl.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('feedback')
    else:
       return redirect('user_login')
    
def view_feedback(request):
    if 'aname' in request.session:
        
        data= Feedback.objects.filter(reply__isnull=True)
        return render(request,'Master/view_feedback.html',{'data':data})
    else:
       return redirect('user_login')
def feedback_replied_list(request):
    if 'aname' in request.session:
        data= Feedback.objects.filter(reply__isnull=False)
        return render(request,'Master/replied_feedback.html',{'data':data})
    else:
       return redirect('user_login')
def adm_reply_feedback(request,id):
    if 'aname' in request.session:

        return render(request,'Master/reply_feedback.html',{'id':id})
    else:
       return redirect('user_login')
def add_reply_feedback(request,id):
    tbl=Feedback.objects.get(feedback_id=id)
    tbl.reply=request.POST.get("reply")
    tbl.save()
    return redirect('feedback_replied_list')

def profile(request):
    if 'uname' in request.session:
        data=get_user(request.session['slogid'])
       
        return render(request,'User/profile.html',{'data':data})
    else:
       return redirect('user_login')
    
def police_home(request):
    if 'pname' in request.session:
        data = get_police_o(request.session['slogid'])
        p_type = data.p_type
        link = "CISI" if p_type in ['CI', 'DSP'] else ""
        station_chat_rooms = _decorate_chat_rooms(
            ChatRoom.objects.filter(police_station=data.police_station).select_related("user", "police_station"),
            "station",
        )
        
        return render(request, 'Police/index.html', {
            'pdata': data,
            'link': link,
            'chat_rooms': station_chat_rooms[:5],
            'chat_room_count': len(station_chat_rooms),
        })
    
    else:
        return redirect('user_login')


def station_home(request):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        chat_rooms = _decorate_chat_rooms(
            ChatRoom.objects.filter(police_station=station).select_related("user", "police_station"),
            "station",
        )
        pending_rooms = len(chat_rooms)
        unread_chat_count = sum(room.unread_count for room in chat_rooms)
        officers_count = PoliceOfficer.objects.filter(police_station=station).count()
        crimes = Crime.objects.filter(police_station=station)
        total_complaints = crimes.count()
        pending_count = crimes.filter(status="Pending").count()
        investigating_count = crimes.filter(status="Investigating").count()
        resolved_count = crimes.filter(status="Resolved").count()
        recent = crimes.order_by("-created_at")[:10]
        return render(
            request,
            "Station/index.html",
            {
                "station": station,
                "pending_rooms": pending_rooms,
                "unread_chat_count": unread_chat_count,
                "recent_chat_rooms": chat_rooms[:5],
                "officers_count": officers_count,
                "total_complaints": total_complaints,
                "pending_count": pending_count,
                "investigating_count": investigating_count,
                "resolved_count": resolved_count,
                "recent": recent,
            },
        )
    return redirect("user_login")


def station_officers(request):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        officers = PoliceOfficer.objects.filter(police_station=station).order_by("-created_at")
        return render(request, "Station/officers_list.html", {"station": station, "officers": officers})
    return redirect("user_login")


def station_add_officer(request):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        return render(request, "Station/officer_add.html", {"station": station})
    return redirect("user_login")


def station_save_officer(request):
    if "stname" in request.session:
        if request.method != "POST":
            return redirect("station_officers")

        station = get_station(request.session["slogid"])

        username = request.POST.get("username")
        password = request.POST.get("password")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        mail_id = request.POST.get("mail_id")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth") or None
        qualification = request.POST.get("qualification")
        p_type = request.POST.get("p_type")

        username_exists = Login.objects.filter(username=username).exists() or User.objects.filter(username=username).exists()
        if username_exists:
            messages.add_message(request, messages.INFO, "Username already exists.")
            return redirect("station_add_officer")

        login = Login.objects.create(
            username=username,
            password=password,
            user_type="Police",
            status="Approved",
        )

        officer = PoliceOfficer(
            login=login,
            name=name,
            police_station=station,
            district=station.district,
            place=station.place,
            address=address,
            phone_number=phone,
            mail_id=mail_id,
            qualification=qualification,
            gender=gender,
            date_of_birth=date_of_birth,
            p_type=p_type,
        )

        photo = request.FILES.get("photo")
        if photo:
            split_tup = os.path.splitext(photo.name)
            file_extension = split_tup[1]
            dir_path = settings.MEDIA_ROOT
            count = sum(os.path.isfile(os.path.join(dir_path, path)) for path in os.listdir(dir_path))
            filename = str(count + 1) + file_extension
            obj = FileSystemStorage()
            file = obj.save(filename, photo)
            officer.photo = obj.url(file)

        proof = request.FILES.get("proof")
        if proof:
            split_tup = os.path.splitext(proof.name)
            file_extension = split_tup[1]
            dir_path = settings.MEDIA_ROOT
            count = sum(os.path.isfile(os.path.join(dir_path, path)) for path in os.listdir(dir_path))
            filename = str(count + 1) + file_extension
            obj = FileSystemStorage()
            file = obj.save(filename, proof)
            officer.proof = obj.url(file)

        officer.save()

        messages.add_message(request, messages.INFO, "Police officer created successfully.")
        return redirect("station_officers")
    return redirect("user_login")


def station_delete_officer(request, id):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        officer = get_object_or_404(PoliceOfficer, pk=id, police_station=station)
        login = officer.login
        officer.delete()
        if login:
            login.delete()
        messages.add_message(request, messages.INFO, "Deleted successfully.")
        return redirect("station_officers")
    return redirect("user_login")


def station_edit_officer(request, id):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        officer = get_object_or_404(PoliceOfficer, pk=id, police_station=station)
        return render(request, "Station/officer_edit.html", {"station": station, "officer": officer})
    return redirect("user_login")


def station_update_officer(request, id):
    if "stname" in request.session:
        if request.method != "POST":
            return redirect("station_officers")
        station = get_station(request.session["slogid"])
        officer = get_object_or_404(PoliceOfficer, pk=id, police_station=station)

        officer.name = request.POST.get("name")
        officer.phone_number = request.POST.get("phone")
        officer.mail_id = request.POST.get("mail_id")
        officer.address = request.POST.get("address")
        officer.qualification = request.POST.get("qualification")
        officer.gender = request.POST.get("gender")
        officer.date_of_birth = request.POST.get("date_of_birth") or None
        officer.p_type = request.POST.get("p_type")

        photo = request.FILES.get("photo")
        if photo:
            split_tup = os.path.splitext(photo.name)
            file_extension = split_tup[1]
            dir_path = settings.MEDIA_ROOT
            count = sum(os.path.isfile(os.path.join(dir_path, path)) for path in os.listdir(dir_path))
            filename = str(count + 1) + file_extension
            obj = FileSystemStorage()
            file = obj.save(filename, photo)
            officer.photo = obj.url(file)

        proof = request.FILES.get("proof")
        if proof:
            split_tup = os.path.splitext(proof.name)
            file_extension = split_tup[1]
            dir_path = settings.MEDIA_ROOT
            count = sum(os.path.isfile(os.path.join(dir_path, path)) for path in os.listdir(dir_path))
            filename = str(count + 1) + file_extension
            obj = FileSystemStorage()
            file = obj.save(filename, proof)
            officer.proof = obj.url(file)

        officer.save()
        messages.add_message(request, messages.INFO, "Updated successfully.")
        return redirect("station_officers")
    return redirect("user_login")


def station_complaints(request):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        crimes = Crime.objects.filter(police_station=station).order_by("-created_at")
        stats = crimes.values("status").annotate(c=Count("crime_id"))
        return render(request, "Station/complaints_list.html", {"station": station, "crimes": crimes, "stats": stats})
    return redirect("user_login")


def station_complaint_detail(request, id):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        crime = get_object_or_404(Crime, pk=id, police_station=station)
        officers = PoliceOfficer.objects.filter(police_station=station).order_by("name")
        fir = FIR.objects.filter(crime_id=crime).first()
        updates = CrimeUpdates.objects.filter(crime=crime).order_by("-created_at")
        return render(
            request,
            "Station/complaint_detail.html",
            {"station": station, "crime": crime, "officers": officers, "fir": fir, "updates": updates},
        )
    return redirect("user_login")


def station_assign_complaint(request, id):
    if "stname" in request.session:
        if request.method != "POST":
            return redirect("station_complaint_detail", id)
        station = get_station(request.session["slogid"])
        crime = get_object_or_404(Crime, pk=id, police_station=station)
        officer_id = request.POST.get("police_officer")
        officer = get_object_or_404(PoliceOfficer, pk=officer_id, police_station=station)
        crime.police_officer = officer
        crime.status = "Investigating"
        crime.save()

        Notification.objects.create(
            user=crime.user,
            police_station=station,
            crime=crime,
            title="Case assigned",
            body=f"Your complaint '{crime.subject}' has been assigned and is now Investigating.",
        )
        messages.add_message(request, messages.INFO, "Assigned successfully.")
        return redirect("station_complaint_detail", id)
    return redirect("user_login")


def station_update_case(request, id):
    if "stname" in request.session:
        if request.method != "POST":
            return redirect("station_complaint_detail", id)
        station = get_station(request.session["slogid"])
        crime = get_object_or_404(Crime, pk=id, police_station=station)

        new_status = request.POST.get("status")
        if new_status in ["Pending", "Investigating", "Resolved", "Assigned to Police"]:
            crime.status = new_status
        crime.place = request.POST.get("place", crime.place)
        crime.subject = request.POST.get("subject", crime.subject)
        crime.complaint_text = request.POST.get("complaint_text", crime.complaint_text)
        crime.save()

        Notification.objects.create(
            user=crime.user,
            police_station=station,
            crime=crime,
            title="Case updated",
            body=f"Your complaint '{crime.subject}' was updated. Current status: {crime.status}.",
        )
        messages.add_message(request, messages.INFO, "Updated successfully.")
        return redirect("station_complaint_detail", id)
    return redirect("user_login")


def station_add_fir(request, id):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        crime = get_object_or_404(Crime, pk=id, police_station=station)
        fir = FIR.objects.filter(crime_id=crime).first()
        if fir:
            return redirect("station_view_fir", id)
        return render(request, "Station/fir_add.html", {"station": station, "crime": crime})
    return redirect("user_login")


def station_save_fir(request, id):
    if "stname" in request.session:
        if request.method != "POST":
            return redirect("station_add_fir", id)
        station = get_station(request.session["slogid"])
        crime = get_object_or_404(Crime, pk=id, police_station=station)

        if FIR.objects.filter(crime_id=crime).exists():
            messages.add_message(request, messages.INFO, "FIR already exists.")
            return redirect("station_view_fir", id)

        FIR.objects.create(
            crime_id=crime,
            description=request.POST.get("description"),
            witness_details=request.POST.get("witness_details"),
            evidence_details=request.POST.get("evidence_details"),
        )
        crime.status = "Investigating"
        crime.save()

        Notification.objects.create(
            user=crime.user,
            police_station=station,
            crime=crime,
            title="FIR created",
            body=f"FIR has been created for your complaint '{crime.subject}'.",
        )
        messages.add_message(request, messages.INFO, "FIR created successfully.")
        return redirect("station_complaint_detail", id)
    return redirect("user_login")


def station_view_fir(request, id):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        crime = get_object_or_404(Crime, pk=id, police_station=station)
        fir = get_object_or_404(FIR, crime_id=crime)
        return render(request, "Station/fir_view.html", {"station": station, "crime": crime, "fir": fir})
    return redirect("user_login")


def police_chat_list(request):
    if "pname" in request.session:
        officer = get_police_o(request.session["slogid"])
        station = officer.police_station
        rooms = _decorate_chat_rooms(
            ChatRoom.objects.filter(police_station=station).select_related("user", "police_station"),
            "station",
        )
        return render(request, "Police/chat_list.html", {"pdata": officer, "rooms": rooms})
    return redirect("user_login")


def police_chat_room(request, id):
    if "pname" in request.session:
        officer = get_police_o(request.session["slogid"])
        station = officer.police_station
        room = get_object_or_404(ChatRoom, pk=id, police_station=station)
        _mark_chat_messages_read(room, "station")
        history = ChatMessage.objects.filter(room=room).order_by("created_at")[:200]
        rooms = _decorate_chat_rooms(
            ChatRoom.objects.filter(police_station=station).select_related("user", "police_station"),
            "station",
        )
        return render(
            request,
            "Police/chat_room.html",
            {"pdata": officer, "rooms": rooms, "room": room, "history": history},
        )
    return redirect("user_login")
    
 
def add_police_station(request):
    if 'aname' in request.session:
        state = State.objects.all()
        district = District.objects.all()

        return render(request, 'Master/add_police_station.html', {
            'data': state,
            'district': district
        })
    else:
        return redirect('user_login')
    
def admin_save_station(request):
    if "aname" in request.session:
        if request.method != "POST":
            return redirect("add_police_station")

        district_id = request.POST.get("district")
        place = request.POST.get("place")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        mail_id = request.POST.get("mail_id")

        PoliceStation.objects.create(
            district_id=district_id,
            station_name=place,
            place=place,
            address=address,
            phone_number=phone,
            mail_id=mail_id,
            status="approved",
        )

        messages.success(request, "Added successfully")
        return redirect("add_police_station")
    else:
        return redirect("user_login")
def display_district(request):
    state_id = request.GET.get("state_id")
    try:

        dist = District.objects.filter(state_id = state_id)
    except Exception:
        data=[]
        data['error_message'] = 'error'
        return JsonResponse(data)
    return JsonResponse(list(dist.values('district_id', 'district')), safe = False)

def list_police_station(request):
    if 'aname' in request.session:
            data=PoliceStation.objects.all()
            return render(request, 'Master/list_police_station.html',{'data':data})
    else:
        return redirect('user_login')
def edit_police_station(request,id):
    if 'aname' in request.session:
            data=PoliceStation.objects.get(police_station_id=id)
            return render(request, 'Master/edit_police_station.html',{'data':data})
    else:
        return redirect('user_login')
def update_police_station(request,id):
    if 'aname' in request.session:

       


        tbl=PoliceStation.objects.get(police_station_id=id)
    
        tbl.place=request.POST.get("place")
        tbl.address=request.POST.get("address")
        tbl.phone_number=request.POST.get("phone")
        tbl.mail_id=request.POST.get("mail_id")
        tbl.save()
        messages.add_message(request, messages.INFO, 'Updated successfully.')
        return redirect('list_police_station')
    else:
        return redirect('user_login')
def delete_police_station(request,id):
 if 'aname' in request.session:
        police_station =PoliceStation.objects.get(police_station_id=id)
        login = police_station.login
        police_station.delete()              
        login.delete()
        messages.add_message(request, messages.INFO, 'Deleted successfully.')
        return redirect('list_police_station')
 else:
      return redirect('login')
def police_registration(request):
    # Repurposed: Police Station self-registration (admin will approve)
    data = State.objects.all()
    return render(request, "police_registration.html", {"data": data, "district": []})


def save_station(request):
    # Police station self-registration
    if request.method != "POST":
        return redirect("police_registration")

    username = request.POST.get("username")
    password = request.POST.get("password")
    station_name = request.POST.get("station_name")
    district_id = request.POST.get("district")
    place = request.POST.get("place")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    mail_id = request.POST.get("mail_id")

    username_exists = Login.objects.filter(username=username).exists() or User.objects.filter(username=username).exists()
    if username_exists:
        messages.add_message(request, messages.INFO, "User name is already Exist. Sorry Registration Failed.")
        return redirect("police_registration")

    login = Login.objects.create(
        username=username,
        password=password,
        user_type="PoliceStation",
        status="Submitted",
    )

    PoliceStation.objects.create(
        login=login,
        district_id=district_id,
        station_name=station_name,
        place=place,
        address=address,
        phone_number=phone,
        mail_id=mail_id,
        status="pending",
    )

    messages.add_message(request, messages.INFO, "Station registered successfully. Waiting for admin approval.")
    return redirect("police_registration")


def submitted_stations(request):
    if "aname" in request.session:
        stations = PoliceStation.objects.filter(status="pending")
        return render(request, "Master/submitted_stations.html", {"stations": stations})
    return redirect("user_login")


def approve_station(request, id):
    if "aname" in request.session:
        station = get_object_or_404(PoliceStation, pk=id)
        station.status = "approved"
        station.save()
        if station.login_id:
            station.login.status = "Approved"
            station.login.save()
        messages.add_message(request, messages.INFO, "Approved successfully.")
        return redirect("submitted_stations")
    return redirect("user_login")


def reject_station(request, id):
    if "aname" in request.session:
        station = get_object_or_404(PoliceStation, pk=id)
        station.status = "rejected"
        station.save()
        if station.login_id:
            station.login.status = "Rejected"
            station.login.save()
        messages.add_message(request, messages.INFO, "Rejected successfully.")
        return redirect("submitted_stations")
    return redirect("user_login")
def submitted_crimes(request):
    if 'aname' in request.session:
           
            crime=Crime.objects.filter(status="Pending")
            context = {'crime': crime,}
            return render(request, 'Master/view_crime.html',context)
    else:
        return redirect('user_login')


def adm_station_pending_cases(request):
    if "aname" in request.session:
        # Cases that are not yet assigned to a police station (or need station assignment)
        crimes = Crime.objects.filter(police_station__isnull=True).order_by("-created_at")
        return render(request, "Master/station_pending_cases.html", {"crime": crimes})
    return redirect("user_login")


def adm_to_assign_station(request, id):
    if "aname" in request.session:
        crime = get_object_or_404(Crime, pk=id)
        state = State.objects.all()
        return render(request, "Master/to_assign_station.html", {"state": state, "crime": crime, "id": id})
    return redirect("user_login")


def adm_assign_station(request, id):
    if "aname" in request.session:
        if request.method != "POST":
            return redirect("adm_to_assign_station", id)

        crime = get_object_or_404(Crime, pk=id)
        station_id = request.POST.get("police_station")
        station = get_object_or_404(PoliceStation, pk=station_id, status__in=["approved", "Approved"])

        crime.police_station = station
        # Keep original pending flow, but now station has access and can assign to officer
        if crime.status == "Pending":
            crime.status = "Pending"
        crime.save()

        Notification.objects.create(
            user=crime.user,
            police_station=station,
            crime=crime,
            title="Case assigned to station",
            body=f"Your complaint '{crime.subject}' has been assigned to {station.station_name or station.place}.",
        )
        messages.add_message(request, messages.INFO, "Assigned to police station successfully.")
        return redirect("adm_station_pending_cases")
    return redirect("user_login")
def adm_crime_more(request,id):
    if 'aname' in request.session:
     
            crime=Crime.objects.get(pk=id)
            fir=FIR.objects.get(crime_id=id)
            
            context = {'crime': crime,'fir':fir}
            return render(request, 'Master/crime_more.html',context)
    else:
        return redirect('user_login')
def assign_crimes(request,id):
    if 'aname' in request.session:
        crime=Crime.objects.get(pk=id)
        crime.status="Assigned to Police"
        crime.police_officer_id=request.POST.get('police')
        crime.save()
        messages.add_message(request, messages.INFO, 'Assigned to Police successfully.')
        return redirect('submitted_crimes')
    else:
        return redirect('user_login')
def to_assign_crimes(request,id):
    if 'aname' in request.session:
        data=State.objects.all()
        crime=Crime.objects.get(crime_id=id)
     
        return render(request, 'Master/to_assign_crimes.html',{'state':data,'id':id,'crime':crime})
    else:
        return redirect('user_login')
def assigned_crimes(request):
    if 'aname' in request.session:
           
            crime=Crime.objects.filter(status="Assigned to Police")
            context = {'crime': crime,}
            return render(request, 'Master/view_assigned_crime.html',context)
    else:
        return redirect('user_login')
def transfer(request):
    if 'aname' in request.session:
            state = State.objects.all() 
            context = {'state': state}
            return render(request, 'Master/transfer.html',context)
    else:
        return redirect('user_login')
def transfer_details(request):
    if 'aname' in request.session:
            state = State.objects.all() 
            context = {'state': state}
            return render(request, 'Master/transfer.html',context)
    else:
        return redirect('user_login')
def save_transfer(request):
    if 'aname' in request.session:
        police_id = request.POST.get('police')
        new_police_id = request.POST.get('police1')
        police_station_id = request.POST.get('police_station')
        assigned_station_id = request.POST.get('police_station1')
        new_station_id = request.POST.get('police_station2')
        if police_station_id != assigned_station_id:
            messages.error(request, 'New assigned officer must be in the same police station as the current officer.')
            return redirect('transfer')

        if police_id == new_police_id:
            messages.error(request, 'New assigned police officer must be different from the current officer.')
            return redirect('transfer')

        if police_station_id == new_station_id:
            messages.error(request, 'Cannot transfer to the same police station.')
            return redirect('transfer')

        #Crime Change
        crime=Crime.objects.filter(police_officer=request.POST.get('police')).update(police_officer_id=request.POST.get('police1'))
      
        # transfer

        p=PoliceOfficer.objects.get(police_officer_id=request.POST.get('police'))
        p.police_station_id=request.POST.get('police_station2')
        p.save()
        messages.add_message(request, messages.INFO, 'Assigned to Police successfully.')
        return redirect('transfer')  
    else:
        return redirect('user_login')
def p_assigned_crimes(request):
    if 'pname' in request.session:
        data = get_police_o(request.session['slogid'])
        police_officer_id = data.police_officer_id

        crime_list = Crime.objects.filter(status="Assigned to Police", police_officer_id=police_officer_id)
        fir_records = FIR.objects.filter(crime_id__in=crime_list).values_list('crime_id', flat=True)

        context = {'crime': crime_list, 'fir_records': fir_records}
        return render(request, 'Police/view_assigned_crime.html', context)
    else:
        return redirect('user_login')
def crime_updates(request,id):
    if 'pname' in request.session:
        
            CrimeUpdatesdata = CrimeUpdates.objects.filter(crime_id=id)
            context = {'CrimeUpdates': CrimeUpdatesdata,'id':id}
            return render(request, 'Police/crime_updates.html',context)
    else:
        return redirect('user_login')
def save_updates(request,id):
    if 'pname' in request.session:
        data=get_police_o(request.session['slogid'])
        police_officer_id=data.police_officer_id
        crime=CrimeUpdates()
        crime.crime_id=id
        crime.police_officer_id=police_officer_id
        crime.crime_updates=request.POST.get('updates')
        filedoc = request.FILES.get('filedoc')
        if filedoc:
            split_tup = os.path.splitext(filedoc.name)
            file_extension = split_tup[1]

            # Get media directory path
            dir_path = settings.MEDIA_ROOT
            count = sum(os.path.isfile(os.path.join(dir_path, path)) for path in os.listdir(dir_path))

            # Generate a unique filename
            filecount = count + 1
            filename = str(filecount) + file_extension

            # Save file
            obj = FileSystemStorage()
            file = obj.save(filename, filedoc)
            url1 = obj.url(file)
            crime.filedoc = url1  # Store file URL in database

        crime.save()
        messages.add_message(request, messages.INFO, 'Updated Successfully.')
        return redirect('crime_updates',id)
    else:
        return redirect('user_login')
def p_crime_more(request,id):
    if 'pname' in request.session:
     
            crime=Crime.objects.get(pk=id)
            context = {'crime': crime,}
            return render(request, 'Police/crime_more.html',context)
    else:
        return redirect('user_login')
def adm_updates(request,id):
    if 'aname' in request.session:
        
            CrimeUpdatesdata = CrimeUpdates.objects.filter(crime_id=id)
            context = {'CrimeUpdates': CrimeUpdatesdata}
            return render(request, 'Master/crime_updates.html',context)
    else:
        return redirect('user_login')



'''def district_wise(request):
    if 'aname' in request.session:
        hotspots = (
            Crime.objects.values('district__district', 'place')
            .annotate(crime_count=Count('crime_id'))
            .order_by('-crime_count')[:3]  # Limit to top 3
        )

        # Convert data into a format for Chart.js
        districts = [hotspot["district__district"] for hotspot in hotspots]
        places = [hotspot["place"] for hotspot in hotspots]
        crime_counts = [hotspot["crime_count"] for hotspot in hotspots]

        context = {
            "districts": districts,
            "places": places,
            "crime_counts": crime_counts,
        }
        return render(request, "Master/district_hotspots.html", context)
    else:
        return redirect("user_login")




def place_wise(request):
    if 'aname' in request.session:
        hotspots = (
            Crime.objects.values('place', 'district__district')
            .annotate(crime_count=Count('crime_id'))
            .order_by('-crime_count')[:3]  # Limit to top 3 places
        )

        # Convert data into format for Chart.js
        places = [hotspot["place"] for hotspot in hotspots]
        districts = [hotspot["district__district"] for hotspot in hotspots]
        crime_counts = [hotspot["crime_count"] for hotspot in hotspots]

        context = {
            "places": places,
            "districts": districts,
            "crime_counts": crime_counts,
        }
        return render(request, "Master/place_hotspots.html", context)
    else:
        return redirect("user_login")'''


from django.db.models import Count

def district_wise(request):
    if 'aname' in request.session:
        hotspots = (
            Crime.objects.values('district__district')  # Group only by district
            .annotate(crime_count=Count('crime_id'))  # Sum all crime counts per district
            .order_by('-crime_count')[:3]  # Limit to top 3 districts
        )

        # Convert data into a format for Chart.js
        districts = [hotspot["district__district"] for hotspot in hotspots]
        crime_counts = [hotspot["crime_count"] for hotspot in hotspots]

        context = {
            "districts": districts,
            "crime_counts": crime_counts,
        }
        return render(request, "Master/district_hotspots.html", context)
    else:
        return redirect("user_login")



from django.db.models import Count
from collections import defaultdict

def place_wise(request):
    if 'aname' in request.session:
        # Fetch crime data and normalize place names
        raw_hotspots = (
            Crime.objects.values('place')
            .annotate(crime_count=Count('crime_id'))
            .order_by('-crime_count')
        )

        # Aggregate crime counts manually to avoid duplicates
        crime_summary = defaultdict(int)
        for entry in raw_hotspots:
            normalized_place = entry["place"].strip().lower()  # Normalize place name
            crime_summary[normalized_place] += entry["crime_count"]

        # Convert dictionary to lists
        places = list(crime_summary.keys())
        crime_counts = list(crime_summary.values())

        context = {
            "places": places,
            "crime_counts": crime_counts,
        }
        return render(request, "Master/place_hotspots.html", context)
    else:
        return redirect("user_login")




def adm_google_map_view_spot(request, latitude, longitude):
    if 'aname' in request.session:
     
            context = {'latitude': latitude,'longitude': longitude,}
            return render(request, 'Master/google_map_view_spot.html',context)
    else:
        return redirect('user_login')
def p_google_map_view_spot(request, latitude, longitude):
    if 'pname' in request.session:
     
            context = {'latitude': latitude,'longitude': longitude,}
            return render(request, 'Police/google_map_view_spot.html',context)
    else:
        return redirect('user_login')
def add_fir(request, id):
    if 'pname' in request.session:
        crime = get_object_or_404(Crime, crime_id=id)
        return render(request, 'Police/fir.html', {'crime': crime})
    else:
        return redirect('user_login')
def save_fir(request,id):
    if request.method == "POST":
        crime_id = id
        description = request.POST.get('description')
        witness_details = request.POST.get('witness_details')
        evidence_details = request.POST.get('evidence_details')

        crime = get_object_or_404(Crime, crime_id=crime_id)

        # Check if FIR already exists
        if FIR.objects.filter(crime_id=crime).exists():
            messages.warning(request, "FIR already exists for this crime.")
            return redirect('view_fir', crime_id)

        FIR.objects.create(
            crime_id=crime,
            description=description,
            witness_details=witness_details,
            evidence_details=evidence_details
        )
        messages.success(request, "FIR added successfully.")
        return redirect('view_fir', crime_id)

    return redirect('p_assigned_crimes')   
def view_fir(request, id):
    if 'pname' in request.session:
        fir = get_object_or_404(FIR, crime_id=id)
        return render(request, 'Police/view_fir.html', {'fir': fir})
    else:
        return redirect('user_login') 
def p_profile(request):
    if 'pname' in request.session:
        data=get_police_o(request.session['slogid'])
        police_officer_id=data.police_officer_id
        profile = get_object_or_404(PoliceOfficer, police_officer_id=police_officer_id)
        return render(request, 'Police/profile.html', {'profile': profile})
    else:
        return redirect('user_login') 
    
def p_other_crimes(request):
    if 'pname' in request.session:
        data = get_police_o(request.session['slogid'])  # Get logged-in police officer data
        p_type = data.p_type
        crimes=[]

        # DSP & CI can see all crimes in their district
        if p_type in ['DSP']:
            crimes = Crime.objects.filter(district=data.district)
            link = "CISI"
        elif p_type in ['CI']:
            # Other officers can only see crimes in their police station
            crimes = Crime.objects.filter(police_station=data.police_station)
            link = ""

        return render(request, 'Police/p_other_crimes.html', {
            'pdata': data,
            'crimes': crimes,
            'p_type': p_type
        })
    
    else:
        return redirect('user_login')
    
def forget_password(request):
    return render(request,'forget_password.html')

def send_otp(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    c = Login.objects.filter(username=username,user_type='User').count()
    if(c>0):
        data = Login.objects.get(username=username,user_type='User')
        logid= data.login_id
        data2 = UserInfo.objects.get(login_id=logid)
        reg_email=data2.email_id
        if(str(email)==str(reg_email)):
            sub="Your OTP From CrimeTracker"
            msg=generate_otp(4)
            send_mail(email,msg,sub)
            msg1=msg
            return render(request,'check_otp.html',{'msg':msg1,'logid':logid})
        else:
            messages.add_message(request, messages.INFO, 'This is not your Registered Email Id')
            return redirect('user_login')
    else:
            messages.add_message(request, messages.INFO, 'Invalid User name')
            return redirect('user_login')
def check_otp_action(request):
     logid=request.POST.get("logid")
     otp=request.POST.get("otp")
   
     otpsend = request.POST.get("sendotp")
     if(int(otpsend)==int(otp)):
      
        return render(request,'new_password.html',{'logid':logid})
def change_psd(request):
     logid=request.POST.get("logid")
     password=request.POST.get("password")
     tbl = Login.objects.get(login_id=logid)
     tbl.password=password
     tbl.save()      
     messages.add_message(request, messages.INFO, 'Password has been changed')
     return redirect('user_login')
def send_mail(erc,msg,sub):
    email_sender="meryljo25@gmail.com"
    email_password="qdnngmrsibcxmbvz"
    email_receiver=erc
    subject=sub
    body=msg
    em=EmailMessage()
    em['From']="CrimeTracker"
    em['To']=email_receiver
    em['Subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())

def generate_otp(length): # Define the function with the parameter ‘length’
    otp = ""
    for _ in range(length): # Use for loop
        otp += str(random.randint(0, 9)) # 
    return otp
        

def get_user(logid):
     data=UserInfo.objects.get(login_id=logid)
     return data
def get_police_o(logid):
     data=PoliceOfficer.objects.get(login_id=logid)
     return data

def get_station(logid):
     data = PoliceStation.objects.get(login_id=logid)
     return data


def _ensure_user_chat_rooms(user):
    station_ids = list(
        Crime.objects.filter(user=user)
        .exclude(police_station__isnull=True)
        .values_list("police_station_id", flat=True)
        .distinct()
    )
    existing_station_ids = set(
        ChatRoom.objects.filter(user=user, police_station_id__in=station_ids).values_list("police_station_id", flat=True)
    )

    for station_id in station_ids:
        if station_id not in existing_station_ids:
            ChatRoom.objects.create(user=user, police_station_id=station_id)

    return ChatRoom.objects.filter(user=user).select_related("user", "police_station")


def _decorate_chat_rooms(rooms, viewer_role):
    decorated_rooms = []
    for room in rooms:
        last_message = room.messages.order_by("-created_at").first()
        unread_count = room.messages.filter(is_read=False).exclude(sender_type=viewer_role).count()
        room.last_message = last_message
        room.unread_count = unread_count
        room.last_activity = last_message.created_at if last_message else room.updated_at
        decorated_rooms.append(room)

    decorated_rooms.sort(key=lambda item: item.last_activity, reverse=True)
    return decorated_rooms


def _mark_chat_messages_read(room, viewer_role):
    ChatMessage.objects.filter(room=room).exclude(sender_type=viewer_role).filter(is_read=False).update(is_read=True)


def _get_chat_access(request, room_id):
    if "uname" in request.session:
        user = get_user(request.session["slogid"])
        room = get_object_or_404(ChatRoom.objects.select_related("user", "police_station"), pk=room_id, user=user)
        return room, "user"

    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        room = get_object_or_404(ChatRoom.objects.select_related("user", "police_station"), pk=room_id, police_station=station)
        return room, "station"

    if "pname" in request.session:
        officer = get_police_o(request.session["slogid"])
        room = get_object_or_404(
            ChatRoom.objects.select_related("user", "police_station"),
            pk=room_id,
            police_station=officer.police_station,
        )
        return room, "station"

    return None, None


def _serialize_chat_message(message):
    return {
        "message_id": message.chat_message_id,
        "sender_type": message.sender_type,
        "message": message.message,
        "created_at": timezone.localtime(message.created_at).isoformat(),
        "time_label": timezone.localtime(message.created_at).strftime("%b %d, %Y %I:%M %p"),
    }


def chat_room_messages_api(request, id):
    room, sender_type = _get_chat_access(request, id)
    if not room:
        return JsonResponse({"ok": False, "error": "Unauthorized"}, status=401)

    if request.method == "GET":
        _mark_chat_messages_read(room, sender_type)
        messages_data = [_serialize_chat_message(message) for message in ChatMessage.objects.filter(room=room).order_by("created_at")[:200]]
        return JsonResponse({"ok": True, "messages": messages_data})

    if request.method == "POST":
        message_text = (request.POST.get("message") or "").strip()
        if not message_text:
            return JsonResponse({"ok": False, "error": "Message is required."}, status=400)

        chat_message = ChatMessage.objects.create(room=room, sender_type=sender_type, message=message_text)
        room.updated_at = timezone.now()
        room.save(update_fields=["updated_at"])
        return JsonResponse({"ok": True, "message": _serialize_chat_message(chat_message)})

    return JsonResponse({"ok": False, "error": "Method not allowed."}, status=405)


def chat(request):
    # Route chat based on logged-in role, without changing citizen pages
    if "uname" in request.session:
        return redirect("user_chat")
    if "stname" in request.session:
        return redirect("station_chat_list")
    if "pname" in request.session:
        return redirect("police_chat_list")
    return redirect("user_login")


def user_chat(request, id=None):
    if "uname" in request.session:
        user = get_user(request.session["slogid"])
        station_id = request.GET.get("station_id")
        rooms = _decorate_chat_rooms(_ensure_user_chat_rooms(user), "user")
        selected_room = None

        if id is not None:
            selected_room = get_object_or_404(ChatRoom, pk=id, user=user)
        elif station_id:
            station = PoliceStation.objects.filter(police_station_id=station_id).first()
            if station:
                selected_room, _ = ChatRoom.objects.get_or_create(user=user, police_station=station)
                rooms = _decorate_chat_rooms(_ensure_user_chat_rooms(user), "user")
        elif rooms:
            selected_room = rooms[0]

        history = []
        if selected_room:
            _mark_chat_messages_read(selected_room, "user")
            history = ChatMessage.objects.filter(room=selected_room).order_by("created_at")[:200]
            rooms = _decorate_chat_rooms(_ensure_user_chat_rooms(user), "user")

        return render(
            request,
            "User/chat.html",
            {
                "user_data": user,
                "rooms": rooms,
                "selected_room": selected_room,
                "history": history,
            },
        )
    return redirect("user_login")


def station_chat_list(request):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        rooms = _decorate_chat_rooms(
            ChatRoom.objects.filter(police_station=station).select_related("user", "police_station"),
            "station",
        )
        return render(request, "Station/chat_list.html", {"station": station, "rooms": rooms})
    return redirect("user_login")


def station_chat_room(request, id):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        room = get_object_or_404(ChatRoom, pk=id, police_station=station)
        _mark_chat_messages_read(room, "station")
        history = ChatMessage.objects.filter(room=room).order_by("created_at")[:200]
        rooms = _decorate_chat_rooms(
            ChatRoom.objects.filter(police_station=station).select_related("user", "police_station"),
            "station",
        )
        return render(
            request,
            "Station/chat_room.html",
            {"station": station, "rooms": rooms, "room": room, "history": history},
        )
    return redirect("user_login")


def _haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    dphi = math.radians(float(lat2) - float(lat1))
    dlambda = math.radians(float(lon2) - float(lon1))

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def panic_send(request):
    # Citizen presses panic button: send GPS when available and still allow alerts without it
    if "uname" not in request.session or request.method != "POST":
        return JsonResponse({"ok": False, "error": "Unauthorized"}, status=401)

    user = get_user(request.session["slogid"])
    lat = request.POST.get("latitude")
    lon = request.POST.get("longitude")

    alert = PanicAlert.objects.create(user=user, latitude=lat, longitude=lon, status="new")
    alert_time = timezone.localtime(alert.created_at)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "panic_admin",
        {
            "type": "panic_message",
            "data": {
                "id": alert.panic_alert_id,
                "user": user.name,
                "phone": user.phone_number,
                "latitude": str(alert.latitude) if alert.latitude is not None else "",
                "longitude": str(alert.longitude) if alert.longitude is not None else "",
                "created_at": alert_time.strftime("%b %d, %Y %I:%M %p"),
                "status": alert.status,
            },
        },
    )

    return JsonResponse(
        {
            "ok": True,
            "id": alert.panic_alert_id,
            "location_received": alert.latitude is not None and alert.longitude is not None,
        }
    )


def adm_panic_alerts(request):
    if "aname" in request.session:
        alerts = PanicAlert.objects.all().order_by("-created_at")[:200]
        return render(request, "Master/panic_alerts.html", {"alerts": alerts})
    return redirect("user_login")


def adm_forward_panic(request, id):
    if "aname" not in request.session:
        return redirect("user_login")

    alert = get_object_or_404(PanicAlert, pk=id)

    # nearest station among approved stations with coordinates
    approved = PoliceStation.objects.filter(status__in=["approved", "Approved"])
    candidates = approved.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    nearest = None
    nearest_km = None
    if alert.latitude is not None and alert.longitude is not None:
        for s in candidates:
            d = _haversine_km(alert.latitude, alert.longitude, s.latitude, s.longitude)
            if nearest is None or d < nearest_km:
                nearest = s
                nearest_km = d

    if request.method == "POST":
        station_id = request.POST.get("police_station")
        if not station_id and nearest:
            station_id = nearest.police_station_id
        if not station_id:
            messages.add_message(request, messages.INFO, "No station selected (and no station has coordinates set).")
            return redirect("adm_forward_panic", id)

        station = get_object_or_404(PoliceStation, pk=station_id)
        alert.police_station = station
        alert.status = "forwarded"
        alert.save()
        alert_time = timezone.localtime(alert.created_at)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"panic_station_{station.police_station_id}",
            {
                "type": "panic_message",
                "data": {
                    "id": alert.panic_alert_id,
                    "user": alert.user.name,
                    "phone": alert.user.phone_number,
                    "latitude": str(alert.latitude) if alert.latitude is not None else "",
                    "longitude": str(alert.longitude) if alert.longitude is not None else "",
                    "created_at": alert_time.strftime("%b %d, %Y %I:%M %p"),
                    "status": alert.status,
                },
            },
        )

        messages.add_message(request, messages.INFO, "Forwarded to police station successfully.")
        return redirect("adm_panic_alerts")

    stations = approved.order_by("place")
    return render(
        request,
        "Master/panic_forward.html",
        {"alert": alert, "stations": stations, "nearest": nearest, "nearest_km": nearest_km},
    )


def station_panic_alerts(request):
    if "stname" in request.session:
        station = get_station(request.session["slogid"])
        alerts = PanicAlert.objects.filter(police_station=station).order_by("-created_at")[:200]
        return render(request, "Station/panic_alerts.html", {"station": station, "alerts": alerts})
    return redirect("user_login")
