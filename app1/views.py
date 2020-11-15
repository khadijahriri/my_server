from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User,PendingWish,GrantedWish
import bcrypt
# Create your views here.
def reg_log(request):
    return  render(request,"login.html")
def registration(request):
    if request.method == "POST": 
        required_errors = User.objects.fields_required_validator(request.POST)
        max_length_errors = User.objects.fields_max_length_validator(request.POST)
        confirm_password_errors = User.objects.confirm_password(request.POST)
        if len(required_errors) > 0:
            for key, value in required_errors.items():
                messages.error(request, value)
            return redirect('/')
        if len(confirm_password_errors) > 0:
            for key, value in confirm_password_errors.items():
                messages.error(request, value)
            return redirect('/')
        if len(max_length_errors) > 0:
            for key, value in max_length_errors.items():
                messages.error(request, value)
            return redirect('/')
        if len(required_errors) == 0 and len(max_length_errors) == 0:
            user_password = request.POST['password']
            hash1 =  bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(user_password.encode(), hash1).decode()     
            user =User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash,salt=hash1)
            messages.success(request, "Account successfully created. You can login now.")
            return redirect('/')
def login(request):
    if request.method == "POST": 
        required_errors = User.objects.fields_required_validator(request.POST)
        if len(required_errors) > 0:
            for key, value in required_errors.items():
                messages.error(request, value)
            return redirect('/')
        user = User.objects.filter(email=request.POST['email']) 
    if user:
        logged_user = user[0] 
        
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect(f'/wishes')
        else: 
            messages.error(request, "Wrong Password")
            return redirect('/')
    if len(user)==0:
        messages.error(request, "Account dose not exist")
        return redirect('/')
def main(request):
    the_user = User.objects.get(id=request.session['userid'])
    user_pending_wishs= the_user.pending_wishes.all()
    users_granted_wishs= GrantedWish.objects.all()
    data ={
        'user_on_template': the_user,
        'users_granted_wishs_on_template':users_granted_wishs,
        
    }
    return  render(request,"main.html",data)
def make_a_wish_page(request):
    the_user = User.objects.get(id=request.session['userid'])
    data ={
        'user_on_template': the_user,
    }
    return  render(request,"new.html",data)
def make_a_wish(request):
    if request.method == "POST":
        required_errors = PendingWish.objects.fields_required_validator(request.POST)
        max_length_errors = PendingWish.objects.fields_max_length_validator(request.POST)
        if len(required_errors) > 0:
            for key, value in required_errors.items():
                messages.error(request, value)
            return redirect('/make_a_wish_page')
        if len(max_length_errors) > 0:
            for key, value in max_length_errors.items():
                messages.error(request, value)
        # redirect the user back to the form to fix the errors
            return redirect('/make_a_wish_page')
        if len(required_errors) == 0 and len(max_length_errors) == 0:
            the_user = User.objects.get(id=request.session['userid'])
            wish =PendingWish.objects.create(item=request.POST['item'],desc=request.POST['desc'],wisher=the_user)
            return redirect('/wishes')
    return redirect('/make_a_wish_page')

def display(request):
    count1=0
    count2=0
    count3=0
    the_user = User.objects.get(id=request.session['userid'])
    for ojects in GrantedWish.objects.all():
        count1=count1 +1
    for ojects in the_user.granted_wishes.all():
        count2=count2 +1
    for ojects in the_user.pending_wishes.all():
        count3=count3 +1
    number_of_granted_wishes=count1
    number_of_user_granted_wishes=count2
    number_of_user_pending_wishes=count3
    data ={
        'user_on_template': the_user,
        'granted_wishes_on_template': number_of_granted_wishes,
        'user_granted_wishes_on_template': number_of_user_granted_wishes,
        'user_pending_wishes_on_template': number_of_user_pending_wishes,

    }
    return  render(request,"stats.html",data)
def edit_page(request,wish_id):
    the_user = User.objects.get(id=request.session['userid'])
    the_wish = PendingWish.objects.get(id=wish_id)
    data ={
        'user_on_template': the_user,
        'wish_on_template':the_wish,
    }
    return  render(request,"update.html",data)
def edit(request,wish_id):
    if request.method == "POST":
        required_errors = PendingWish.objects.fields_required_validator(request.POST)
        max_length_errors = PendingWish.objects.fields_max_length_validator(request.POST)
        if len(required_errors) > 0:
            for key, value in required_errors.items():
                messages.error(request, value)
            return redirect(f'/edit_page/{wish_id}')
        if len(max_length_errors) > 0:
            for key, value in max_length_errors.items():
                messages.error(request, value)
            return redirect(f'/edit_page/{wish_id}')
        if len(required_errors) == 0 and len(max_length_errors) == 0:
            wish =PendingWish.objects.get(id=wish_id)
            wish.item=request.POST['item']
            wish.desc=request.POST['desc']
            wish.save()
            return redirect('/wishes')
    return redirect(f'/edit_page/{wish_id}')
def grant_wish(request,wish_id):
    the_old_pending_wish=PendingWish.objects.get(id=wish_id)
    the_new_granted_wish =GrantedWish.objects.create(item=the_old_pending_wish.item,desc=the_old_pending_wish.desc,wisher=the_old_pending_wish.wisher,the_time_wish_was_created=the_old_pending_wish.created_at)
    the_old_pending_wish.delete()
    return redirect('/wishes')
def remove_wish(request,wish_id):
    the_wish = PendingWish.objects.get(id=wish_id)
    the_wish.delete()
    return redirect('/wishes')
def like(request,wish_id):
    already_liked_it=False
    the_user = User.objects.get(id=request.session['userid'])
    the_granted_wish = GrantedWish.objects.get(id=wish_id)
    for user in the_granted_wish.users_who_like_this_wish.all():
        if user.id == the_user.id :
            already_liked_it=True
    if already_liked_it == False:
        the_granted_wish.number_of_likes = the_granted_wish.number_of_likes +1
        the_granted_wish.users_who_like_this_wish.add(the_user)
        the_granted_wish.save()
    return redirect('/wishes')
def loging_out(request):
    request.session['userid'] =0
    return redirect('/')

