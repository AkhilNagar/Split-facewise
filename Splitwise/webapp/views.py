from django.shortcuts import render,redirect
import pyrebase
from webapp.forms import UserForm,UserProfileInfoForm
from webapp.forms import TransactionForm
from webapp.forms import TransactionHistory
from webapp.models import Transaction_Pairs,UserProfile
from webapp.models import Transaction_history
#from webapp.forms import UserProfileInfo
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.db.models import DateTimeField
from django.contrib import messages
from webapp import face_rec
import face_recognition
import threading
import time
import cv2


#FIREBASE CONNECTION
config={
    "apiKey": "AIzaSyDdxlfh7Qb_8fOiJn8hWbaqaSQT8_n-7Yc",
    "authDomain": "facerecognition-9506e.firebaseapp.com",
    "projectId": "facerecognition-9506e",
    "storageBucket": "facerecognition-9506e.appspot.com",
    "messagingSenderId": "713869339014",
    "appId": "1:713869339014:web:816b67e5f750eac2f2a407",
    "measurementId": "G-05MQESTD98",
    "databaseURL": "https://facerecognition-9506e-default-rtdb.firebaseio.com/",
    "serviceAccount":"serviceAccount.json",


}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
storage=firebase.storage()

#import all the views eg-from django.view.generic import(TemplateView,ListView)





@login_required
def special(request):
    return HttpResponse("You are logged in")

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied!")

    else:
        return render(request, 'login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
#HOME PAGE
def index(request):
    global person_n

    datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
    dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
    # obj=Transaction_Pairs.objects.filter(person1="hetvi")
    # n=Transaction_Pairs.objects.filter().count()
    # query=obj[:1]
    # obj1=query.get()
    # userlist=face_rec.compare(obj1.grp_pic)
    # print(userlist)

    # for i in obj:
    #     print(obj.users)
    #     print(UserProfile.objects.filter(users="A"))
    # day = database.child('Data').child('Day').get().val()
    # id = database.child('Data').child('Id').get().val()
    # projectname = database.child('Data').child('Projectname').get().val()
    # print(day)

    return render(request,'index.html',{"datap":datap,"dataopp":dataopp})

#REGISTRATION FUNCTION
def register(request):

    registered=False

    if request.method == "POST":
        print("method1")
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(request.FILES)
        print(profile_form.errors)
        if user_form.is_valid() and profile_form.is_valid():

            print("method2")
            user =user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            name=request.POST.get('username')
            if 'profile_pic' in request.FILES:
                print("method3")
                img=request.FILES['profile_pic']
                profile.profile_pic=img

                profile.users=name
                profile.face_encode=""
                profile.save()
                #face_rec.create_embed(name)
                # t1 = threading.Thread(face_rec.create_embed(name),args=())
                # t1.start()
                #time.sleep(2)
            encodejson=face_rec.create_embed(name)
            profile1=UserProfile.objects.get(users=name)
            profile1.face_encode=encodejson
            profile1.save()
            registered=True
            print(img)
            #Adds to firebase
            #storage.child("face.jpg").put(img)
            return redirect('index')

    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'registration.html',{'user_form':user_form,'registered':registered, 'profile_form':profile_form,})
    #add key value pair 'profile_form':profile_form,

#TRANSACTION
def transaction(request):
    numpeople=0
    amt=0
    progress=False
    ifimage=False

    if request.method == "POST":
        transact_form=TransactionForm(request.POST,request.FILES)
        print(transact_form.errors)
        if transact_form.is_valid():
            reason=request.POST["reason"]

            if 'grp_pic' in request.FILES:
                print("Found grp_pic")
                img=request.FILES['grp_pic']
                ifimage=True
            progress=True
            person1_=request.user.get_username()
            #now = date.datetime.now()
            amt=request.POST["amount"]
            amt1=float(amt)
            people=request.POST["people"]

            #Get list of users after processing
            #user_list=face_rec.recognise_faces(img)
            #If preview is clicked show Images
            # Add more names manually
            if ifimage == True:
                user_list=face_rec.compare(img)
            else:
                user_list=[]

            if(request.user.get_username() in user_list):
                user_list.remove(request.user.get_username())
            a=0
            for x in range(0,len(people)):
                if people[x]==',':
                    temp=people[a:x]
                    a=x + 1
                    if(temp not in user_list):
                        user_list.append(temp)
                    temp=""
            if(people[a:] not in user_list):
                user_list.append(people[a:])
            print(user_list)
            numpeople_=len(user_list)+1




            for i in range(1,numpeople_):
                person2_=user_list[i-1]
                contrib=(amt1)/float(numpeople_)
                t_pair_count = Transaction_Pairs.objects.filter(person1=person1_,person2=person2_).count() + Transaction_Pairs.objects.filter(person1=person2_,person2=person1_).count()
                if t_pair_count==1:
                    #obj=(Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person2_,) if Transaction_Pairs.objects.filter(person1=person2_,person2=request.user.get_username()).count()==0 else Transaction_Pairs.objects.get(person1=person2_,person2=request.user.get_username()))
                    if Transaction_Pairs.objects.filter(person1=person2_,person2=request.user.get_username()).count()==0:
                        obj=Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person2_,)
                        flag=1
                    else:
                        obj=Transaction_Pairs.objects.get(person1=person2_,person2=request.user.get_username())
                        flag=0
                    if flag==1:
                        famt1=float(obj.amount)
                    elif flag==0:
                        famt1=-float(obj.amount)
                    amt_=float(obj.amount)
                    if flag==1:
                        amt_+=contrib
                        obj.amount=amt_
                    elif flag==0:
                        famt1+=contrib
                        obj.amount=famt1*(-1.0)
                        if obj.amount<0:
                            temp=obj.person1
                            obj.person1=obj.person2
                            obj.person2=temp
                            obj.amount=famt1


                    if ifimage==True:
                        obj.grp_pic=img
                    obj.save()

                    t_pair_count=0
                elif t_pair_count==0:
                    if ifimage==True:
                        transact=Transaction_Pairs(person1=person1_,person2=person2_,amount=contrib,grp_pic=img)
                        transact.save()
                        t_pair_count=0
                    else:
                        transact=Transaction_Pairs(person1=person1_,person2=person2_,amount=contrib)
                        transact.save()
                        t_pair_count=0
                else:
                    break
                history=Transaction_history(person1=person1_,person2=person2_,reason=reason,amount=contrib)
                history.save()
        #datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
        #dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
        #return render(request,'webapp/index.html',{'transact_form':transact_form,'progress':progress,"datap":datap,'dataopp':dataopp})
        return redirect('index')

    else:
        transact_form=TransactionForm()
        datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
        dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
        return render(request,'transaction.html',{'transact_form':transact_form,'progress':progress,"datap":datap,"dataopp":dataopp})

#DISPLAY DETECTED IMAGES
def display(request):
    img=""
    userlist=[]
    if request.method == "POST":
        img = request.FILES['img']

        userlist=face_rec.showface(img)
        print(img)

    return render(request,'image.html',{"img":img,"userlist":userlist})

person_n=""

#SHOWS TRANSACTION HISTORY
def history(request):
    global person_n

    datah=Transaction_history.objects.filter(person1=request.user.get_username())
    dataopp= Transaction_history.objects.filter(person2=request.user.get_username())
    if request.method == 'POST':
        transact_history=TransactionHistory(data=request.POST)

        if transact_history.is_valid():
            person_n=request.POST["person_name"]
            if person_n=="":
                messages.error(request,'Person Not found')
                flag1=False
            else:
                flag1=True
    else:
        transact_history=TransactionHistory()
        return render(request,'history.html',{'transact_history':transact_history,"datah":datah,"dataopp":dataopp})

    datah=Transaction_history.objects.filter(person1=request.user.get_username(),person2=person_n)
    dataopp= Transaction_history.objects.filter(person2=request.user.get_username(),person1=person_n)

    if Transaction_Pairs.objects.filter(person1=request.user.get_username(),person2=person_n).count()==0 and Transaction_Pairs.objects.filter(person1=person_n,person2=request.user.get_username()).count()==0 :
        messages.error(request,'Person Not found')
        return render(request,'history.html',{'transact_history':transact_history,"datah":datah,"dataopp":dataopp})

    elif Transaction_Pairs.objects.filter(person1=person_n,person2=request.user.get_username()).count()==0:
        famt1=Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person_n,)
        flag=True
    elif Transaction_Pairs.objects.filter(person1=request.user.get_username(),person2=person_n).count()==0:
        famt1=Transaction_Pairs.objects.get(person1=person_n,person2=request.user.get_username())
        flag=False




    #famt1=(Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person_n,) and flag=1)
    if flag==True:
        famt=float(famt1.amount)
    elif flag==False:
        famt=-float(famt1.amount)
    return render(request,'history.html',{"flag":flag,"flag1":flag1, "dataopp":dataopp,"person_n":person_n,"famount":famt,"datah":datah,"transact_history":transact_history})

#BALANCES ACCOUNTS
def nullify(request):
    global person_n
    '''
    print("HI1")
    if request.method == 'GET':
        print("HI2")
        obj=(Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person_n,) if Transaction_Pairs.objects.filter(person1=person_n,person2=request.user.get_username()).count()==0 else Transaction_Pairs.objects.get(person1=person_n,person2=request.user.get_username()))
        obj.amount=0
        obj.save()
        datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
        dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
        return render(request,'webapp/index.html',{"datap":datap,"dataopp":dataopp})
    else:
        return render(request,'webapp/index.html',{"datap":datap,"dataopp":dataopp})
'''
    if request.GET.get('mybtn') or request.GET.get('mybtn1')  and person_n !="":
        amtr=int(request.GET.get('mytextbox'))
        obj=(Transaction_Pairs.objects.get(person1=request.user.get_username(),person2=person_n,) if Transaction_Pairs.objects.filter(person1=person_n,person2=request.user.get_username()).count()==0 else Transaction_Pairs.objects.get(person1=person_n,person2=request.user.get_username()))
        if request.GET.get('mybtn') and obj.amount==0.0:
            messages.warning(request,"You cannot receive money!")
        elif request.GET.get('mybtn') and amtr!=0 and obj.amount!=0.0:
            #last if is so the value doesnt go from money owed 0 to negative
            obj.amount-=amtr
        elif request.GET.get('mybtn') and amtr==0:
            messages.info(request,"Enter an amount!")
            return render(request,'history.html')

            #return HttpResponse("Enter an amount!") #I want it to be an alert


        elif request.GET.get('mybtn1') and obj.amount!=0.0:
            obj.amount=0
            messages.success(request,"Full amount received")

        elif request.GET.get('mybtn1') and obj.amount==0.0:
            messages.warning(request,"You cannot receive money!")

        obj.save()
        return redirect('index')




        #datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
        #dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
        person_n=""
        return redirect('index')

#REDUCE NET NUMBER OF TRANSACTIONS AMONGST FRIEND GROUPS
def settle(request):

    if request.method=='GET':
        c1=Transaction_Pairs.objects.filter(person1=request.user.get_username()).count()
        c2=Transaction_Pairs.objects.filter(person2=request.user.get_username()).count()
        if c1>0 and c2==0:
            obj1=Transaction_Pairs.objects.filter(person1=request.user.get_username())
            for i in obj1:
                obj2=obj1.exclude(person2=i.person2)
                counter1=Transaction_Pairs.objects.filter(person1=i.person2).count()
                counter2=Transaction_Pairs.objects.filter(person2=i.person2).count()
                check=0
                if counter1 > 0:
                    obj3=Transaction_Pairs.objects.filter(person1=i.person2)
                    obj3=obj3.exclude(person2=i.person1)
                if counter2 > 0:
                    check=1
                    obj3=Transaction_Pairs.objects.filter(person2=i.person2)
                    obj3=obj3.exclude(person1=i.person1)
                for j in obj2:
                    for k in obj3:
                        if(check==1):
                            if(j.person2==k.person1):
                                if(j.amount==k.amount):
                                    print("Entered")
                                    temp_amount=j.amount
                                    j.amount=0
                                    k.amount=0
                                    i.amount+=temp_amount
                                    i.save()
                                    j.save()
                                    k.save()
                        if(check==0):
                            if(j.person2==k.person2):
                                if(j.amount==k.amount):
                                    print("Entered")
                                    temp_amount=j.amount
                                    j.amount=0
                                    k.amount=0
                                    i.amount+=temp_amount
                                    i.save()
                                    j.save()
                                    k.save()
        if c1>0 and c2>0:
            obj1=Transaction_Pairs.objects.filter(person2=request.user.get_username())
            obj2=Transaction_Pairs.objects.filter(person1=request.user.get_username())
            for i in obj1:
                for j in obj2:
                    if(i.amount==j.amount):
                        temp_amount=i.amount
                        i.amount=0
                        j.amount=0
                        obj3=Transaction_Pairs.objects.filter(person1=i.person1,person2=j.person2)
                        for k in obj3:
                            k.amount+=temp_amount
                            i.save()
                            j.save()
                            k.save()
        if c2>0 and c1==0:
            obj1=Transaction_Pairs.objects.filter(person2=request.user.get_username())
            for i in obj1:
                obj2=obj1.exclude(person1=i.person1)
                for j in obj2:
                    obj3=Transaction_Pairs.objects.filter(person1=i.person1,person2=j.person1)
                    for k in obj3:
                        if(j.amount==k.amount):
                            temp_amount=j.amount
                            j.amount=0
                            k.amount=0
                            i.amount+=temp_amount
                            i.save()
                            j.save()
                            k.save()

        #datap= Transaction_Pairs.objects.filter(person1=request.user.get_username())
        #dataopp= Transaction_Pairs.objects.filter(person2=request.user.get_username())
        #return render(request, 'webapp/index.html',{'datap':datap,'dataopp':dataopp})
        return redirect('index')
