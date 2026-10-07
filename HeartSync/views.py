from django.shortcuts import render,redirect
import csv
import os
from django.db.models import Q
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.db import transaction
from django.http import HttpResponse,HttpResponseRedirect
from HeartSync.models import *
from HeartSync.forms import *
def create_user(request):
    UMF = UserMF()
    UPMF = ProfileMF()
    d = {'UMF':UMF,'UPMF':UPMF}
    if request.method == 'POST':
        UMUMF = UserMF(request.POST)
        UMUPMF = ProfileMF(request.POST,request.FILES)
        if UMUMF.is_valid() and UMUPMF.is_valid():
            MUMF = UMUMF.save(commit=False)
            password = UMUMF.cleaned_data['password']
            MUMF.set_password(password)
            MUMF.save()

            MUPMF = UMUPMF.save(commit=False)
            MUPMF.username = MUMF
            city = UMUPMF.cleaned_data['city']
            interests = UMUPMF.cleaned_data['interests']
            #CO = City.objects.get(city_name = city)
            MUPMF.city = city
            #IO = Interest.objects.filter(interest_name__in=interests)
            MUPMF.save()
            MUPMF.interests.set(interests)
            return HttpResponse('created')
        else:
            print(UMUMF.errors)
            print(UMUPMF.errors)
            return HttpResponse('invalid data')

    return render(request,'createaccount.html',d)

def discover(request):
    username = request.session['username']
    UO = User.objects.get(username = username)
    UPO = UserProfile.objects.get(username = UO)
    passed_profiles = PassUser.objects.filter(who = UPO)
    passed_users = passed_profiles.values_list('whom',flat=True)
    AUPO = UserProfile.objects.exclude(username = UO).exclude(profile_id__in = passed_users)
    PPU = UserProfile.objects.filter(profile_id__in = passed_users)
    return render(request,'discover.html',{'AUPO':AUPO,'PPU':PPU})

def home(request):
    if request.session.get('username'):
        username = request.session['username']
        UO = User.objects.get(username=username)
        UPO = UserProfile.objects.get(username=UO)
        LO = Like.objects.filter(receiver = UPO)
        like_count = LO.count()
        passed_profiles = PassUser.objects.filter(who = UPO)
        passed_users = passed_profiles.values_list('whom',flat=True)
        AUPO = UserProfile.objects.exclude(username=UO).exclude(profile_id__in = passed_users)

        d = {'UPO':UPO,'AUPO':AUPO,'like_count':like_count}
        return render(request,'home.html',d)
    return render(request,'home.html')

def matches(request):
    username = request.session['username']
    UO = User.objects.get(username = username)
    UPO = UserProfile.objects.get(username = UO)
    #sent_likes = Like.objects.filter(sender = UPO)
    #receive_likes = Like.objects.filter(receiver =UPO)
    match_likes = Match.objects.filter(Q(first_user=UPO) | Q(second_user=UPO))
    matched_profiles = []
    for mo in match_likes:
        if mo.first_user == UPO:
            matched_profiles.append(mo.second_user)
        else:
            matched_profiles.append(mo.first_user)
    sent_likes = Like.objects.filter(sender = UPO).exclude(receiver__in = matched_profiles)
    receive_likes = Like.objects.filter(receiver =UPO).exclude(sender__in = matched_profiles)
    match_count = match_likes.count()
    sent_count = sent_likes.count()
    receive_count = receive_likes.count()
    d = {'sent_likes':sent_likes,'sent_count':sent_count,'receive_likes':receive_likes,'receive_count':receive_count,'matched_profiles':matched_profiles,'match_count':match_count}
    return render(request,'matches.html',d)

def like(request,profile_id):
    if request.method == 'POST':
        username = request.session.get('username')
        UO = User.objects.get(username=username)
        UPO = UserProfile.objects.get(username=UO)
        receiver = UserProfile.objects.get(profile_id=profile_id)
        LO = Like.objects.get_or_create(sender = UPO,receiver = receiver)
        reverse_like = Like.objects.filter(sender = receiver , receiver = UPO).exists()
        if reverse_like:
            if UPO.profile_id < receiver.profile_id:
                first_user = UPO
                second_user = receiver
            else:
                first_user = receiver
                second_user = UPO
            MO = Match.objects.get_or_create(first_user = first_user,second_user=second_user)
            print("It's a Match 💕")
    return redirect('home')

def pass_user(request,profile_id):
    if request.method == 'POST':
        username = request.session.get('username')
        UO = User.objects.get(username=username)
        UPO = UserProfile.objects.get(username=UO)
        whom = UserProfile.objects.get(profile_id=profile_id)
        PO , created = PassUser.objects.get_or_create(who = UPO , whom = whom)
    return redirect('home')

def user_login(request):
    if request.method == 'POST':
        un = request.POST['username']
        pw = request.POST['password']
        AUO = authenticate(username=un,password=pw)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username'] = un
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('User Not Active')
        else:
            return HttpResponse('User Not Found')
    return render(request,'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def insert_cities(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        'files',
        '01_cities.csv'
    )

    inserted_count = 0
    updated_count = 0

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.DictReader(file)

        with transaction.atomic():
            for row in data:
                city, created = City.objects.update_or_create(
                    city_id=int(row['city_id'].strip()),
                    defaults={
                        'city_name': row['city_name'].strip(),
                        'state': row['state'].strip(),
                        'country': row['country'].strip(),
                    }
                )

                if created:
                    inserted_count += 1
                else:
                    updated_count += 1

    return HttpResponse(
        f'Cities inserted: {inserted_count}, updated: {updated_count}'
    )

def insert_interests(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        'files',
        '02_interests.csv'
    )

    inserted_count = 0
    updated_count = 0

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.DictReader(file)

        with transaction.atomic():
            for row in data:
                interest, created = Interest.objects.update_or_create(
                    interest_id=int(row['interest_id'].strip()),
                    defaults={
                        'interest_name': row['interest_name'].strip()
                    }
                )

                if created:
                    inserted_count += 1
                else:
                    updated_count += 1

    return HttpResponse(
        f'Interests inserted: {inserted_count}, '
        f'updated: {updated_count}'
    )

def insert_profiles(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        'files',
        '03_user_profiles.csv'
    )

    inserted_count = 0
    updated_count = 0

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.DictReader(file)

        with transaction.atomic():
            for row in data:
                city = City.objects.get(
                    city_id=int(row['city_id'].strip())
                )

                profile, created = UserProfile.objects.update_or_create(
                    profile_id=int(row['profile_id'].strip()),
                    defaults={
                        'name': row['name'].strip(),
                        'email': row['email'].strip(),
                        'gender': row['gender'].strip(),
                        'age': int(row['age'].strip()),
                        'bio': row['bio'].strip(),
                        'profession': row['profession'].strip(),
                        'city': city,
                        'is_active': (
                            row['is_active'].strip().upper() == 'TRUE'
                        ),
                    }
                )

                interest_names = row['interest_names'].split('|')
                interests = Interest.objects.filter(
                    interest_name__in=interest_names
                )

                profile.interests.set(interests)

                if created:
                    inserted_count += 1
                else:
                    updated_count += 1

    return HttpResponse(
        f'Profiles inserted: {inserted_count}, '
        f'updated: {updated_count}'
    )

def insert_likes(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        'files',
        '04_likes.csv'
    )

    inserted_count = 0
    updated_count = 0

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.DictReader(file)

        with transaction.atomic():
            for row in data:
                sender = UserProfile.objects.get(
                    profile_id=int(row['sender_id'].strip())
                )

                receiver = UserProfile.objects.get(
                    profile_id=int(row['receiver_id'].strip())
                )

                like, created = Like.objects.update_or_create(
                    id=int(row['id'].strip()),
                    defaults={
                        'sender': sender,
                        'receiver': receiver,
                    }
                )

                if created:
                    inserted_count += 1
                else:
                    updated_count += 1

    return HttpResponse(
        f'Likes inserted: {inserted_count}, '
        f'updated: {updated_count}'
    )

def insert_matches(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        'files',
        '05_matches.csv'
    )

    inserted_count = 0
    updated_count = 0

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.DictReader(file)

        with transaction.atomic():
            for row in data:
                first_user = UserProfile.objects.get(
                    profile_id=int(row['first_user_id'].strip())
                )

                second_user = UserProfile.objects.get(
                    profile_id=int(row['second_user_id'].strip())
                )

                match, created = Match.objects.update_or_create(
                    id=int(row['id'].strip()),
                    defaults={
                        'first_user': first_user,
                        'second_user': second_user,
                        'is_active': (
                            row['is_active'].strip().upper() == 'TRUE'
                        ),
                    }
                )

                if created:
                    inserted_count += 1
                else:
                    updated_count += 1

    return HttpResponse(
        f'Matches inserted: {inserted_count}, '
        f'updated: {updated_count}'
    )

def insert_messages(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        'files',
        '06_messages.csv'
    )

    inserted_count = 0
    updated_count = 0

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.DictReader(file)

        with transaction.atomic():
            for row in data:
                match = Match.objects.get(
                    id=int(row['match_id'].strip())
                )

                sender = UserProfile.objects.get(
                    profile_id=int(row['sender_id'].strip())
                )

                if sender not in [match.first_user, match.second_user]:
                    raise ValueError(
                        f'{sender.name} does not belong to match {match.id}'
                    )

                message, created = Message.objects.update_or_create(
                    id=int(row['id'].strip()),
                    defaults={
                        'match': match,
                        'sender': sender,
                        'message': row['message'].strip(),
                        'is_read': (
                            row['is_read'].strip().upper() == 'TRUE'
                        ),
                    }
                )

                if created:
                    inserted_count += 1
                else:
                    updated_count += 1

    return HttpResponse(
        f'Messages inserted: {inserted_count}, '
        f'updated: {updated_count}'
    )

def insert_blocks(request):
    file_path = os.path.join(
        settings.BASE_DIR,
        'files',
        '07_blocks.csv'
    )

    inserted_count = 0
    updated_count = 0

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = csv.DictReader(file)

        with transaction.atomic():
            for row in data:
                blocker = UserProfile.objects.get(
                    profile_id=int(row['blocker_id'].strip())
                )

                blocked_user = UserProfile.objects.get(
                    profile_id=int(row['blocked_user_id'].strip())
                )

                block, created = Block.objects.update_or_create(
                    id=int(row['id'].strip()),
                    defaults={
                        'blocker': blocker,
                        'blocked_user': blocked_user,
                    }
                )

                if created:
                    inserted_count += 1
                else:
                    updated_count += 1

    return HttpResponse(
        f'Blocks inserted: {inserted_count}, '
        f'updated: {updated_count}'
    )

def show_user(request):
    AUO = UserProfile.objects.all()
    d = {'AUO':AUO}
    return render(request,'users.html',d)