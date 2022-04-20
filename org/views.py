from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, auth
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime, timedelta
from django.db.models import Avg, Count
from .models import Notice, Profile, Event, About, Settings, Carousel, PhotoGallery, Fee, Fund, ContactUs, Resource, Donation, Designation


def home(request):
    caro = Carousel.objects.all().filter(status='True')
    photo_gallery = PhotoGallery.objects.all().filter(home_visibility_status='True').order_by('-pk')
    try:
        settings = Settings.objects.latest('pk')
        context = {
            'setting': settings,
            'carousel': caro,
            'photo_gallery': photo_gallery,
        }
        return render(request, 'index.html', context)
    except ObjectDoesNotExist:
        return render(request, 'admin/site_setting.html')

def regsuper(request):
    if request.method == "POST":
        username = request.POST['username']

        password = request.POST['password']
        password2 = request.POST['password2']
        if password2 == password:
            if User.objects.filter(username=request.POST['username']).exists():
                return HttpResponse("Email Exist")
            elif User.objects.filter(email=request.POST['username']).exists():
                return HttpResponse("Email Exist")
            else:
                myuser = User.objects.create_user(username=username, email=username, password=password, is_superuser=True, is_staff=True)
                myuser.save()
                auth.login(request, myuser)
                return redirect('home')

        else:

            return HttpResponse('input error')

@permission_required('org.add_settings', raise_exception=True)
def regorg(request):
    if request.method == "POST":
        org_full_name = request.POST['org_full_name']
        org_nickname = request.POST['org_nickname']
        org_mail = request.POST['org_mail']
        org_institution = request.POST['org_institution']
        org_fb_link = request.POST['org_fb_link']
        org_linkedin_link = request.POST['org_linkedin_link']
        org_youtube_link = request.POST['org_youtube_link']
        org_active_session = request.POST['org_active_session']
        try:
            org_icon_image = request.FILES['org_icon_image']
        except MultiValueDictKeyError:
            org_icon_image = None
        org_location = request.POST['org_location']
        org_contact_number = request.POST['org_contact_number']
        org_homepage_description = request.POST['org_homepage_description']
        org_map_location = request.POST['org_map_location']
        settings = Settings(
            org_full_name=org_full_name,
            org_nickname=org_nickname,
            org_mail=org_mail,
            org_institution=org_institution,
            org_fb_link=org_fb_link,
            org_linkedin_link=org_linkedin_link,
            org_youtube_link=org_youtube_link,
            org_icon_image=org_icon_image,
            org_location=org_location,
            org_contact_number=org_contact_number,
            org_homepage_description=org_homepage_description,
            org_map_location=org_map_location,
            org_active_session=org_active_session,
        )
        settings.save()
        return redirect('home')

def signup(request):
    settings = Settings.objects.latest('pk')
    context = {
        'setting': settings,
    }
    if request.method == "POST":
        username = request.POST['username']

        password = request.POST['password']
        password2 = request.POST['password2']
        if password2 == password:
            if User.objects.filter(username=request.POST['username']).exists():
                return HttpResponse("Email Exist")
            elif User.objects.filter(email=request.POST['username']).exists():
                return HttpResponse("Email Exist")
            else:
                myuser = User.objects.create_user(username=username, email=username, password=password)
                myuser.save()
                auth.login(request, myuser)
                return redirect('/')

        else:

            return HttpResponse('input error')
    else:
        return render(request, 'signup.html', context)

def login(request):
    settings = Settings.objects.latest('pk')
    context = {
        'setting': settings,
    }
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == "POST":
        username = request.POST['username1']
        password = request.POST['password']

        myuser = auth.authenticate(username=username, password=password)
        if myuser is not None:
            auth.login(request, myuser)
            return redirect('notice')
        else:
            return redirect('login')

    else:
        return render(request, 'login.html', context)

def about(request):
    settings = Settings.objects.latest('pk')
    session = settings.org_active_session
    if session:
        pass
    else:
        session = None
    abouts = About.objects.filter(active_session=session).order_by('designation_priority')
    sessions = About.objects.all().values('active_session').distinct()

    if request.method == "POST":
        u_profile = request.POST['user_profile']
        profile = Profile.objects.get(id=u_profile)
        if profile.image:
            pass
        else:
            profile.image = None
        u_designation = request.POST['designation']
        priorities = Designation.objects.filter(designation=u_designation).values('priority')
        u_priority = priorities
        u_session = request.POST['active_session']
        p = About(
            user=profile,
            designation=u_designation,
            active_session=u_session,
            designation_priority=u_priority,
        )
        p.save()
        return redirect(about)
    context = {
        'setting': settings,
        'about': abouts,
        'session': sessions,
    }
    return render(request, 'about.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def blog(request):
    settings = Settings.objects.latest('pk')
    session = settings.org_active_session
    if session:
        pass
    else:
        session = None
    abouts = About.objects.filter(active_session=session).order_by('designation_priority')
    sessions = About.objects.all().values('active_session').distinct()
    #users = User.objects.all()
    #designation = Designation.objects.all().values('designation').distinct()
    # if request.method=="POST":
    context = {
        'setting': settings,
        'about': abouts,
        'session': sessions,
        #'user': users,
        #'designation': designation,

    }
    return render(request, 'blog.html', context)

def userprofile(request, id):
    obj = get_object_or_404(User, pk=id)

    settings = Settings.objects.latest('pk')
    context = {

        'setting': settings,
        'obj': obj,
    }

    return render(request, 'profile.html', context)

def userprofileedit(request, id):

    if request.method == "POST":
        full_name = request.POST['full_name']
        university_or_institute = request.POST['university_or_institute']
        discipline = request.POST['discipline']
        batch = request.POST['batch']
        student_id = request.POST['student_id']
        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            image = None
        blood_group = request.POST['blood_group']
        contact_number = request.POST['contact_number']
        profession = request.POST['profession']
        hometown = request.POST['hometown']
        current_city = request.POST['current_city']
        fb_link = request.POST['fb_link']
        linkedin = request.POST['linkedin']

        q = get_object_or_404(Profile, pk=id)
        q.full_name = full_name
        q.university_or_institute = university_or_institute
        q.discipline = discipline
        q.batch = batch
        q.student_id = student_id
        q.blood_group = blood_group
        q.contact_number = contact_number
        q.profession = profession
        q.hometown = hometown
        q.current_city = current_city
        q.fb_link = fb_link
        q.linkedin = linkedin
        q.save()
        return redirect('/')

    setting = Settings.objects.latest('pk')
    prof = get_object_or_404(Profile, pk=id)
    context = {
        'setting': setting,
        'profile': prof,


    }
    return render(request, 'editprofile.html', context)

def userprofileedit2(request, id):
    setting = Settings.objects.latest('pk')
    prof = get_object_or_404(Profile, pk=id)
    context = {
        'setting': setting,
        'profile': prof,

    }
    if request.method == "POST":
        image = request.FILES['image']
        q = get_object_or_404(Profile, pk=id)
        q.image = image
        q.save()
        return render(request, 'editprofile.html', context)

    return render(request, 'uploadphoto.html', context)

def contact(request):
    settings = Settings.objects.latest('pk')
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        comment = request.POST['comment']

        contact = ContactUs(
            name=name,
            email=email,
            phone=phone,
            comment=comment,
        )
        contact.save()
        return redirect('home')
    context = {
        'setting': settings,
    }
    return render(request, 'contact.html', context)

def event(request):
    now = datetime.now()
    today = now + timedelta(hours=2)
    #From = now + timedelta(hours=2)

    week = today + timedelta(hours=168)
    weeks = today + timedelta(hours=169)
    month = week + timedelta(days=30)
    previous = today - timedelta(hours=10)
    present = Event.objects.filter(date__range=[today, week]).order_by('-pk')
    #running = Event.objects.filter(date__range=[today, week]).filter(date__range=[date,]).order_by('-pk')

    past = Event.objects.filter(date__range=["2018-12-10 13:56:02", previous]).order_by('-pk')
    coming = Event.objects.filter(date__range=[weeks, month]).order_by('-pk')
    settings = Settings.objects.latest('pk')
    context = {
        'coming': coming,
        'setting': settings,
        'present': present,
        'past': past,
    }
    return render(request, 'event.html', context)

def notice(request):
    notices = Notice.objects.all().order_by('-pk')
    settings = Settings.objects.latest('pk')
    context = {
        'setting': settings,
        'notice': notices,
    }
    return render(request, 'notice.html', context)

def photos(request):
    settings = Settings.objects.latest('pk')
    tag = PhotoGallery.objects.all().values('category').distinct()
    context = {
        'setting': settings,
        'tag': tag,
    }
    return render(request, 'photos.html', context)

def session(request, active_session):
    #obj = get_object_or_404(About, pk=id)
    settings = Settings.objects.latest('pk')

    obj = About.objects.all().filter(active_session=active_session)
    sessions = About.objects.all().values('active_session').distinct()
    context = {
        'setting': settings,
        'obj': obj,
        'session': sessions,
        'sessions': active_session,

    }
    return render(request, 'abouts.html', context)

def event_detail(request, id):
    events = get_object_or_404(Event, pk=id)
    settings = Settings.objects.latest('pk')
    participated = False
    details = Donation.objects.all().filter(event_id=id).order_by('-pk')
    count = Donation.objects.all().filter(event_id=id).count()
    if request.user.is_authenticated:
        user = request.user
        taken = Donation.objects.filter(event_id=id).filter(user_id=user)
        if taken:
            participated = True


    context = {
        'setting': settings,
        'event': events,
        'taken': participated,
        'details': details,
    }
    return render(request, 'event_details.html', context)

def payment(request):

    settings = Settings.objects.latest('pk')
    context = {
        'setting': settings,
    }
    return render(request, 'payment.html', context)

def payment2(request):
    if request.method == "POST":
        feetype = request.POST['type']
        year = request.POST['year']
        txnid = request.POST['txnid']
        amount = request.POST['amount']
        month = request.POST['month']
        method = request.POST['method']

        p = Fee(
            member=request.user.profile,
            feetype=feetype,
            year=year,
            txnid=txnid,
            amount=amount,
            month=month,
            method=method,

        )
        p.save()
        return redirect(home)

@permission_required('org.view_fund', raise_exception=True)
def orgadmin(request):
    settings = Settings.objects.latest('pk')
    fund = Fund.objects.latest('pk')
    paid = Fee.objects.filter(recived="False").order_by("-pk")
    context = {
        'setting': settings,
        'paid': paid,
        'fund': fund,
    }
    return render(request, 'admin/admin.html', context)

@permission_required('org.view_fund', raise_exception=True)
def addfund(request, id):
    if request.method == "POST":
        pay_user = get_object_or_404(Fee, pk=id)
        fund = Fund.objects.latest('pk')
        fund.current_balance = fund.current_balance + pay_user.amount
        fund.save()
        pay_user.recived = True
        pay_user.status = "Accepted"
        pay_user.save()
        return redirect('fundview')

@permission_required('org.view_fund', raise_exception=True)
def Reject(request, id):
    if request.method == "POST":
        pay_user = get_object_or_404(Fee, pk=id)
        fund = Fund.objects.latest('pk')
        fund.current_balance = fund.current_balance + 0
        fund.save()
        pay_user.recived = True
        pay_user.status = "Rejected"
        pay_user.save()
        return redirect('fundview')

@permission_required('org.add_notice', raise_exception=True)
def addnotice(request):
    if request.method == "POST":
        title = request.POST['title']
        text = request.POST['text']
        registration_link = request.POST['registration_link']
        facebook_link = request.POST['facebook_link']
        youtube_link = request.POST['youtube_link']

        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            image = None
        try:
            file = request.FILES['file']
        except MultiValueDictKeyError:
            file = None


        notices = Notice(
            title=title,
            text=text,
            registration_link=registration_link,
            facebook_link=facebook_link,
            youtube_link=youtube_link,
            image=image,
            file=file,

        )
        notices.save()
        return redirect(notice)

@permission_required('org.delete_notice', raise_exception=True)
def deletenotice(request, id):
    p = Notice.objects.get(pk=id)
    p.delete()
    return redirect(notice)

@permission_required('org.change_notice', raise_exception=True)
def editnotice(request, id):
    p = Notice.objects.get(pk=id)
    settings = Settings.objects.latest('pk')
    context = {
        'setting': settings,
        'notice': p,
    }
    if request.method == "POST":
        title = request.POST['title']
        text = request.POST['text']
        registration_link = request.POST['registration_link']
        facebook_link = request.POST['facebook_link']
        youtube_link = request.POST['youtube_link']
        try:
            image = request.FILES['image']
            p.image = image
        except MultiValueDictKeyError:
            pass
        try:
            file = request.FILES['file']
            p.file = file
        except MultiValueDictKeyError:
            pass

        p.title = title
        p.text = text
        p.registration_link = registration_link
        p.facebook_link = facebook_link
        p.youtube_link = youtube_link

        p.save()
        return redirect(notice)


    return render(request, 'admin/editnotice.html', context)

@permission_required('org.add_event', raise_exception=True)
def addevent(request):
    if request.method == "POST":
        event_name = request.POST['event_name']
        description = request.POST['description']
        facebook_link = request.POST['facebook_link']
        youtube_link = request.POST['youtube_link']
        contact_number = request.POST['contact_number']
        date = request.POST['date']
        event_type = request.POST['event_type']
        event_location = request.POST['event_location']
        event_platform = request.POST['event_platform']
        target_amount = request.POST['target_amount']
        online_event_link = request.POST['online_event_link']
        participation_fee = request.POST['participation_fee']


        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            image = None

        events = Event(
            event_name=event_name,
            description=description,
            facebook_link=facebook_link,
            youtube_link=youtube_link,
            image=image,
            contact_number=contact_number,
            date=date,
            event_type=event_type,
            event_location=event_location,
            event_platform=event_platform,
            target_amount=target_amount,
            online_event_link=online_event_link,
            participation_fee=participation_fee,
        )
        events.save()
        return redirect(event)

@permission_required('org.change_event', raise_exception=True)
def editevent(request, id):
    p = Event.objects.get(pk=id)
    settings = Settings.objects.latest('pk')
    context = {
        'setting': settings,
        'event': p,
    }
    if request.method == "POST":
        event_name = request.POST['event_name']
        description = request.POST['description']
        facebook_link = request.POST['facebook_link']
        youtube_link = request.POST['youtube_link']
        contact_number = request.POST['contact_number']
        date = request.POST['date']
        event_type = request.POST['event_type']
        event_location = request.POST['event_location']
        event_platform = request.POST['event_platform']
        target_amount = request.POST['target_amount']
        online_event_link = request.POST['online_event_link']
        participation_fee = request.POST['participation_fee']

        try:
            image = request.FILES['image']
            p.image = image
        except MultiValueDictKeyError:
            pass

        p.event_name = event_name
        p.description = description
        p.facebook_link = facebook_link
        p.youtube_link = youtube_link
        p.contact_number = contact_number
        p.date = date
        p.event_location = event_location
        p.event_platform = event_platform
        p.target_amount = target_amount
        p.online_event_link = online_event_link
        p.participation_fee = participation_fee
        p.save()
        return redirect(event)

    return render(request, 'admin/editevent.html', context)

@permission_required('org.delete_event', raise_exception=True)
def deleteevent(request, id):
    events = Event.objects.get(pk=id)
    events.delete()
    return redirect(event)

@permission_required('org.change_event', raise_exception=True)
def eventphoto(request, id):
    setting = Settings.objects.latest('pk')
    events = get_object_or_404(Event, pk=id)
    context = {
        'setting': setting,
        'obj': events,

    }
    if request.method == "POST":
        image = request.FILES['image']
        q = get_object_or_404(Event, pk=id)
        q.image = image
        q.save()
        return redirect(event)

    return render(request, 'admin/uploadeventphoto.html', context)

@permission_required('org.change_notice', raise_exception=True)
def noticephoto(request, id):
    setting = Settings.objects.latest('pk')
    events = get_object_or_404(Notice, pk=id)
    context = {
        'setting': setting,
        'obj': events,

    }
    if request.method == "POST":
        image = request.FILES['image']
        q = get_object_or_404(Notice, pk=id)
        q.image = image
        q.save()
        return redirect(notice)

    return render(request, 'admin/uploadnoticephoto.html', context)

def error_404_view(request, exception):
    settings = Settings.objects.latest('pk')
    context = {
        'setting': settings,
    }
    return render(request, 'site_setting.html', context)

@permission_required('org.view_fund', raise_exception=True)
def fundview(request):
    settings = Settings.objects.latest('pk')
    fund = Fund.objects.latest('pk')
    paid = Fee.objects.filter(recived="False").order_by("-pk")
    context = {
        'setting': settings,
        'paid': paid,
        'fund': fund,
    }
    return render(request, 'admin/fund.html', context)

@permission_required('org.view_fund', raise_exception=True)
def settingview(request):
    settings = Settings.objects.latest('pk')
    if request.method == "POST":
        org_full_name = request.POST['org_full_name']
        org_nickname = request.POST['org_nickname']
        org_mail = request.POST['org_mail']
        org_institution = request.POST['org_institution']
        org_fb_link = request.POST['org_fb_link']
        org_linkedin_link = request.POST['org_linkedin_link']
        org_youtube_link = request.POST['org_youtube_link']
        org_location = request.POST['org_location']
        org_active_session = request.POST['org_active_session']
        try:
            org_icon_image = request.FILES['org_icon_image']
            settings.org_icon_image = org_icon_image
        except MultiValueDictKeyError:
            pass
        org_contact_number = request.POST['org_contact_number']
        org_homepage_description = request.POST['org_homepage_description']
        org_map_location = request.POST['org_map_location']

        settings.org_full_name = org_full_name
        settings.org_nickname = org_nickname
        settings.org_mail = org_mail
        settings.org_institution = org_institution
        settings.org_fb_link = org_fb_link
        settings.org_linkedin_link = org_linkedin_link
        settings.org_youtube_link = org_youtube_link
        settings.org_location = org_location
        settings.org_contact_number = org_contact_number
        settings.org_homepage_description = org_homepage_description
        settings.org_map_location = org_map_location
        settings.org_active_session = org_active_session

        settings.save()
        return redirect('home')
    context = {
        'setting': settings,
    }
    return render(request, 'admin/editsettings.html', context)

@permission_required('org.view_contactus', raise_exception=True)
def messageview(request):
    settings = Settings.objects.latest('pk')
    message = ContactUs.objects.filter(visited=False).order_by('-pk')
    context = {
        'setting': settings,
        'message': message,
    }
    return render(request, 'admin/contactmessage.html', context)

@permission_required('org.view_carousel', raise_exception=True)
def carousel(request):
    settings = Settings.objects.latest('pk')
    Carousels = Carousel.objects.all().order_by('-pk')
    context = {
        'setting': settings,
        'carousel': Carousels,

    }
    return render(request, 'admin/carousel.html', context)

@permission_required('org.add_carousel', raise_exception=True)
def addcarousel(request):
    if request.method == "POST":
        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            image = None
        image_name = request.POST['image_name']

        car = Carousel(
            image=image,
            image_name=image_name,
        )
        car.save()
        return redirect('carouselview')

@permission_required('org.change_carousel', raise_exception=True)
def carouselON(request, id):
    car = get_object_or_404(Carousel, pk=id)
    if request.method == "POST":
        car.status = True
        car.save()
        return redirect('carouselview')

@permission_required('org.change_carousel', raise_exception=True)
def carouselOFF(request, id):
    car = get_object_or_404(Carousel, pk=id)
    if request.method == "POST":
        car.status = False
        car.save()
        return redirect('carouselview')

@permission_required('org.delete_carousel', raise_exception=True)
def carouselDelete(request, id):
    if request.method == "POST":
        car = get_object_or_404(Carousel, pk=id)
        car.delete()
        return redirect('carouselview')

def previous(request):
    settings = Settings.objects.latest('pk')
    sessions = About.objects.all().values('active_session').distinct()
    context = {
        'setting': settings,
        'session': sessions,
    }
    return render(request, 'previous_about.html', context)

@permission_required('org.add_photogallery', raise_exception=True)
def galleryview(request):
    if request.method == "POST":
        tag = request.POST['tag']
        settings = Settings.objects.latest('pk')
        photo = PhotoGallery.objects.all().filter(category=tag)
        tag = PhotoGallery.objects.all().values('category').distinct()
        context = {
            'setting': settings,
            'photo': photo,
            'tag': tag,
        }
        return render(request, 'admin/gallery.html', context)
    else:
        settings = Settings.objects.latest('pk')
        tag = PhotoGallery.objects.all().values('category').distinct()
        context = {
            'setting': settings,
            'tag': tag,
        }
        return render(request, 'admin/gallery.html', context)

@permission_required('org.add_about', raise_exception=True)
def executiveview(request):
    settings = Settings.objects.latest('pk')
    session = About.objects.all().values('active_session').distinct()
    profiles = Profile.objects.all()
    designation = Designation.objects.all().order_by('priority')
    if request.method == "POST":
        sessions = request.POST['active_session']
        about = About.objects.all().filter(active_session=sessions).order_by('designation_priority')
        context = {
            'setting': settings,
            'about': about,
            'session': session,
            'profile': profiles,
            'designation': designation,
        }
        return render(request, 'admin/designation.html', context)

    else:



        context = {
            'setting': settings,
            'session': session,
            'profile': profiles,
            'designation': designation,

        }
        return render(request, 'admin/designation.html', context)

@permission_required('org.add_designation', raise_exception=True)
def add_designation(request):
    if request.method == "POST":
        designation = request.POST['designation']
        priority = request.POST['priority']

        des = Designation(
            designation=designation,
            priority=priority,
        )
        des.save()
        return redirect(executiveview)

@permission_required('org.change_designation', raise_exception=True)
def edit_designation(request, id):
    des = get_object_or_404(Designation, pk=id)
    if request.method == "POST":
        designation = request.POST['designation']
        priority = request.POST['priority']
        des.designation = designation
        des.priority = priority
        des.save()
        return redirect(executiveview)
    settings = Settings.objects.latest('pk')
    context = {
        'setting': settings,
        'designation': des,
    }
    return render(request, 'admin/designation_change.html', context)

def save_designation(request, id):
    if request.method == "POST":
        designation = get_object_or_404(Designation, pk=id)
        designation.delete()
        return redirect(executiveview)

@permission_required('org.delete_about', raise_exception=True)
def delete_about(request, id):
    events = About.objects.get(pk=id)
    events.delete()
    return redirect(executiveview)

@permission_required('org.change_photogallery', raise_exception=True)
def photosEdit(request, id):
    photo = get_object_or_404(PhotoGallery, pk=id)
    if request.method == "POST":
        phot = get_object_or_404(PhotoGallery, pk=id)
        image_caption = request.POST['image_caption']
        try:
            image = request.FILES['image']
            phot.image = image
        except MultiValueDictKeyError:
            pass
        home_visibility_status = request.POST['home_visibility_status']
        category_visible = request.POST['category_visible']
        category = request.POST['category']

        phot.image_caption = image_caption

        phot.category = category
        phot.home_visibility_status = home_visibility_status
        phot.category_visible = category_visible
        phot.save()
        return redirect(galleryview)
    settings = Settings.objects.latest('pk')
    context = {
        'setting': settings,
        'photo': photo,
    }
    return render(request, 'admin/photo_edit.html', context)

@permission_required('org.delete_photogallery', raise_exception=True)
def photosOFF(request, id):
    photo = get_object_or_404(PhotoGallery, pk=id)
    if request.method == "POST":
        photo.delete()
        return redirect('galleryview')

@permission_required('org.add_photogallery', raise_exception=True)
def save_photo(request):
    if request.method == "POST":
        image_caption = request.POST['image_caption']
        image = request.FILES['image']
        home_visibility_status = request.POST['home_visibility_status']
        category_visible = request.POST['category_visible']
        category = request.POST['category']

        photo = PhotoGallery(
            image_caption=image_caption,
            image=image,
            home_visibility_status=home_visibility_status,
            category_visible=category_visible,
            category=category
        )
        photo.save()
        return redirect(galleryview)

def viewphoto(request, category):
    settings = Settings.objects.latest('pk')
    obj = PhotoGallery.objects.all().filter(category=category)
    tag = PhotoGallery.objects.all().values('category').distinct()
    context = {
        'setting': settings,
        'tag': tag,
        'photos': obj,
    }
    return render(request, 'photos.html', context)

def participate(request, id):
    p = get_object_or_404(Event, pk=id)
    user = request.user


    if request.method == "POST":
        user = request.user
        if user:
            pass
        else:
            user = None
        try:
            balance = request.POST['participation_fee']
            p.current_amount = p.current_amount + int(balance)
            p.save()
        except MultiValueDictKeyError:
            pass

        try:
            amount = request.POST['participation_fee']
        except MultiValueDictKeyError:
            amount = 0

        try:
            transaction = request.POST['transaction_id']
        except MultiValueDictKeyError:
            transaction = None
        try:
            method = request.POST['method']
        except MultiValueDictKeyError:
            method = None

        donate = Donation(
            user=user,
            event=p,
            amount=amount,
            transaction=transaction,
            method=method,
        )
        donate.save()
        return redirect('event')

def resource(request):
    if request.method == "POST":
        try:
            file_cover_photo = request.FILES['file_cover_photo']
        except MultiValueDictKeyError:
            file_cover_photo = None

        try:
            file = request.FILES['file']
        except MultiValueDictKeyError:
            file = None

        file_name = request.POST['file_name']
        file_type = request.POST['file_type']
        file_drive_link = request.POST['file_drive_link']
        file_youtube_link = request.POST['file_youtube_link']
        file_tag = request.POST['file_tag']

        res = Resource(
            file_name=file_name,
            file_tag=file_tag,
            file_type=file_type,
            file=file,
            file_cover_photo=file_cover_photo,
            file_drive_link=file_drive_link,
            file_youtube_link=file_youtube_link,
        )
        res.save()
        return redirect('resource')

    settings = Settings.objects.latest('pk')
    type = Resource.objects.all().values('file_type').distinct()
    context = {
        'setting': settings,
        'type': type,
    }
    return render(request, 'resource.html', context)

def file(request, file_type):
    settings = Settings.objects.latest('pk')
    type = Resource.objects.all().values('file_type').distinct()
    show = Resource.objects.filter(file_type=file_type).order_by('-pk')
    tag = Resource.objects.filter(file_type=file_type).values('file_tag').distinct()
    context = {
        'setting': settings,
        'type': type,
        'show': show,
        'tag': tag,
        'file_type': file_type,
    }
    return render(request, 'resource_common.html', context)

def tagged(request, file_type, file_tag):
    settings = Settings.objects.latest('pk')
    type = Resource.objects.all().values('file_type').distinct()
    show = Resource.objects.filter(file_type=file_type).filter(file_tag=file_tag).order_by('-pk')
    tag = Resource.objects.filter(file_type=file_type).values('file_tag').distinct()

    context = {
        'setting': settings,
        'type': type,
        'show': show,
        'tag': tag,
        'file_type': file_type,
    }

    return render(request, 'resource_common.html', context)
