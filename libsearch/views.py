from django.shortcuts import render
import pyrebase
from django.contrib import auth
from datetime import datetime, timedelta

config = {
    'apiKey': "AIzaSyDxHv3EuZHmpLKjgf4N3IErKW5y0nCthpk",
    'authDomain': "libsearch-debbc.firebaseapp.com",
    'databaseURL': "https://libsearch-debbc-default-rtdb.firebaseio.com/",
    'projectId': "libsearch-debbc",
    'storageBucket': "libsearch-debbc.appspot.com",
    'messagingSenderId': "669897047223",
    'appId': "1:669897047223:web:103b40141fc0c6b259a132",
    'measurementId': "G-JV811CFVC8"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()

def books(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        user=""
        book = database.child('books').get()
        for books in book.each():
            if searched in books.key():
                user = user + " " + books.key()
        users = user.split()
        return render(request,"books.html",{'searched':searched,'books':users})

    else:
        return render(request,"books.html")

def logIn(request):
    return render(request, "logIn.html")

def postsign(request):
    session_id =request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try :
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "Invalid Credentials"
        return render(request,"logIn.html",{"message":message})

    flag=0
    allusers = database.child('users').get()
    for user in allusers.each():
        if session_id == user.key():
            if email == database.child('users').child(user.key()).child('details').child('email').get().val():
                flag=1
                break
    
    if flag :
        status=database.child('users').child(session_id).child('details').child('status').get().val()
        if status=="inactive":
            status=""
        return render(request, "welcome.html",{"session_id":session_id,"status":status})

    else :
        message = "Invalid Credentials"
        return render(request,"logIn.html",{"message":message})

def borrow(request):
    session_id = request.POST.get('session_id')
    searched = request.POST.get('searched')
    flag=0
    message=""
    book = database.child('books').get()
    for books in book.each():
        if searched == books.key():
            flag=1
            break
    if flag:
        if int(database.child('books').child(searched).child('stock').get().val())==0:
            message="Book is Out of Stock"

        else:
            if int(database.child('books').child(searched).child('requests').get().val())>=10:
                message="Book has many pending requests"
            else:
                borrow = database.child('users').child(session_id).child('details').child('borrow').get().val()
                reques = database.child('users').child(session_id).child('details').child('request').get().val()
                if borrow==2:
                    message="You had already borrowed 2 books"
                else:
                    if reques:
                        message="Your previous request is still pending"
                    else:
                        req_count = int(database.child('books').child(searched).child('requests').get().val())
                        req_count = req_count + 1
                        reqby = database.child('books').child(searched).child('reqby').get().val() + " " + session_id
                        database.child('books').child(searched).update({"requests":req_count,"reqby":reqby,"req_stat":""})
                        database.child('users').child(session_id).child('details').update({"request":1,"request_book":searched})
                        message="Request Sent"
        
    else:
        message="Book not found"
    
    return render(request,"welcome.html",{"message":message,"session_id":session_id})

def logout(request): 
    auth.logout(request)
    return render(request,'logIn.html')

def signup(request):
    return render(request,'signup.html')

def postsignup(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email,passw)
    except:
        message="Please input valid email and password"
        return render(request,"signup.html",{"message":message})

    names = name.split()
    name=""
    for nam in names:
        name = name + nam
    flag = 0
    allusers = database.child('users').get()
    for user in allusers.each():
        if name == user.key():
            flag=1
            break
    
    if flag:
        message="Userid already exists"
        return render(request,"signup.html",{"message":message})

    else:        
        data={"book1_d":"","book2_d":"","req_stat":"","email":email,"status":"active","borrow":0,"book1":"","book2":"","request":0,"request_book":""}
        database.child("users").child(name).child("details").set(data)
        return render(request,"logIn.html")

def book_detail(request):
    book = request.POST.get('book')
    pname = database.child('books').child(book).child('pname').get().val()
    aname =database.child('books').child(book).child('aname').get().val()
    stock = database.child('books').child(book).child('stock').get().val()
    if stock=="0":
        stock=""
    return render(request,"book_detail.html",{"book":book,'stock':stock,"aname":aname,"pname":pname})

def log(request):
    return render(request,"logIn.html")

def profile(request):
    session_id = request.POST.get('session_id')
    book1=database.child('users').child(session_id).child('details').child('book1').get().val()
    book2=database.child('users').child(session_id).child('details').child('book2').get().val()
    email=database.child('users').child(session_id).child('details').child('email').get().val()
    reques_book = database.child('users').child(session_id).child('details').child('request_book').get().val()
    book2_d=database.child('users').child(session_id).child('details').child('book2_d').get().val()
    book1_d=database.child('users').child(session_id).child('details').child('book1_d').get().val()
    req_stat=database.child('users').child(session_id).child('details').child('req_stat').get().val()
    return render(request,"profile.html",{"name":session_id,"book1":book1,"book2":book2,"reques_book":reques_book,"email":email,"book1_d":book1_d,"book2_d":book2_d,"req_stat":req_stat})

def librarian(request):
    return render(request,"librarian.html")

def admin(request):
    return render(request,"admin.html")

def home(request):
    return render(request,"home.html")

def librarianpage(request):
    session_id=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try :
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "Invalid Credentials"
        return render(request,"librarian.html",{"message":message})

    lib_ids = database.child('librarians').get()
    flag=0
    for lib_id in lib_ids.each():
        if session_id == lib_id.key():
            flag=1
            break
    if flag:
        book = database.child('librarians').child(session_id).child('role').child('book').get().val()
        newbook = database.child('librarians').child(session_id).child('role').child('newbook').get().val()
        respond = database.child('librarians').child(session_id).child('role').child('respond').get().val()
        if book =="no":
            book=""
        if newbook =="no":
            newbook=""
        if respond =="no":
            respond=""
        return render(request,"lib_page.html",{"session_id":session_id,"book":book,"newbook":newbook,"respond":respond})

    else:
        message="You are not a Librarian"
        return render(request,"librarian.html",{"message":message})

def adminpage(request):
    session_id=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try :
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "Invalid Credentials"
        return render(request,"admin.html",{"message":message})

    admin_ids = database.child('admins').get()
    flag=0
    for admin_id in admin_ids.each():
        if session_id == admin_id.key():
            flag=1
            break
    if flag:
        return render(request,"adminpage.html",{"session_id":session_id})

    else:
        message="You are not an Admin"
        return render(request,"admin.html",{"message":message})



def book_sign(request):
    session_id= request.POST.get('session_id')
    return render(request,"book_sign.html",{"session_id":session_id})

def addbook(request):
    name = request.POST.get('name')
    stock = int(request.POST.get('stock'))
    session_id = request.POST.get('session_id')
    if(stock > 0):
        books = database.child('books').get()
        flag =0
        for book in books.each():
            if name == book.key():
                flag=1
                break
        if flag:
            stock = stock + database.child('books').child(name).child('stock').get().val()
            database.child('books').child(name).update({"stock":stock})
            message="Book added"
        else:
            message="No such book exist in Library"

        return render(request,"lib_page.html",{"session_id":session_id,"message":message})
    else:
        message="Atleast add 1 copy"
        return render(request,"lib_page.html",{"session_id":session_id,"message":message})    

def newbook(request):
    name = request.POST.get('name')
    aname = request.POST.get('aname')
    pname = request.POST.get('pname')
    session_id = request.POST.get('session_id')
    books = database.child('books').get()
    flag =0
    for book in books.each():
        if name == book.key():
            flag=1
            break
    if flag:
        message="Book already exist in the Library"
        return render(request,"lib_page.html",{"session_id":session_id,"message":message})
    else:
        reques=0
        data = {"stock":0,"aname":aname,"pname":pname,"requests":reques,"reqby":""}
        database.child("books").child(name).set(data)
        message="Book registered successfully"
        return render(request,"lib_page.html",{"session_id":session_id,"message":message})

def reqs(request):
    books = database.child('books').get()
    req=""
    for book in books.each():
        if int(database.child('books').child(book.key()).child('requests').get().val()):
            req = book.key() + "-" + str(database.child('books').child(book.key()).child('requests').get().val()) + "(Requests) "
    
    reques=req.split()
    return render(request,"requests.html",{"reques":reques})

def book_req(request):
    reqs=request.POST.get('book')
    name=""
    for req in reqs:
        if req=="-":
            break
        else:
            name= name + req

    req = str(database.child('books').child(name).child('reqby').get().val())
    nnames = req.split()
    req = database.child('books').child(name).child('requests').get().val()
    aname = database.child('books').child(name).child('aname').get().val()
    pname = database.child('books').child(name).child('pname').get().val()

    return render(request,"detailed_req.html",{"name":name,"aname":aname,"pname":pname,"reques":req,"nnames":nnames})

def accept(request):
    name = request.POST.get('name')
    book = database.child('users').child(name).child('details').child('request_book').get().val()
    stock = int(database.child('books').child(book).child('stock').get().val())
    if stock == 0:
        message="Book is out of stock"
    else:
        presentday = datetime.now()
        dueday = presentday + timedelta(7) 
        reqs = str(database.child('books').child(book).child('reqby').get().val())
        nnames = reqs.split()
        reqs=""
        for nname in nnames:
            if(nname==name):
                continue
            else:
                reqs=reqs+" "+nname
        
        nnames=reqs.split()        
        req = int(database.child('books').child(book).child('requests').get().val())
        req=req-1
        database.child('books').child(book).update({"reqby":reqs,"requests":req})
        aname = database.child('books').child(book).child('aname').get().val()
        pname = database.child('books').child(book).child('pname').get().val()
        borrow=int(database.child('users').child(name).child('details').child('borrow').get().val())
        borrow=borrow+1
        message=book + " has been successfully issued to " + name + " for 1 week"
        database.child('users').child(name).child('details').update({"request":0,"request_book":""})
        if(borrow==1):
            database.child('users').child(name).child('details').update({"borrow":1,"book1":book,"book1_d":dueday.strftime('%d-%m-%Y')})
        else:
            database.child('users').child(name).child('details').update({"borrow":2,"book2":book,"book2_d":dueday.strftime('%d-%m-%Y')})
    return render(request,"detailed_req.html",{"message":message,"name":book,"aname":aname,"pname":pname,"reques":req,"nnames":nnames})


def reject(request):
    name = request.POST.get('name')
    book = database.child('users').child(name).child('details').child('request_book').get().val()
    reqs = database.child('books').child(book).child('reqby').get().val()
    nnames = reqs.split()
    reqs=""
    for nname in nnames:
        if(nname==name):
            continue
        else:
            reqs=reqs+" "+nname
    
    nnames=reqs.split()        
    req = int(database.child('books').child(book).child('requests').get().val())
    req=req-1
    database.child('books').child(book).update({"reqby":reqs,"requests":req})
    aname = database.child('books').child(book).child('aname').get().val()
    pname = database.child('books').child(book).child('pname').get().val()
    reqs="Your last request of "+book+" was rejected"
    message="Request of "+name+" has been rejected for "+book
    database.child('users').child(name).child('details').update({"request":0,"request_book":"","req_stat":reqs})
    return render(request,"detailed_req.html",{"message":message,"name":book,"aname":aname,"pname":pname,"reques":req,"nnames":nnames})

def book1(request):
    name = request.POST.get('name')
    presentday = datetime.now()
    date_format = "%d-%m-%Y"
    dueday = datetime.strptime(database.child('users').child(name).child('details').child('book1_d').get().val(),date_format)
    delta = presentday-dueday
    delt = int(delta.days)
    if delt<1:
        message="Book has submitted on time"
    else:
        delt = delt*10
        message="Book and fine of Rs."+str(delt)+" (Rs.10 per day) has submitted"

    book = database.child('users').child(name).child('details').child('book1').get().val()
    stock = int(database.child('books').child(book).child('stock').get().val())
    stock = stock +1
    database.child('books').child(book).update({"stock":stock})

    book = database.child('users').child(name).child('details').child('book2').get().val()
    book_d = database.child('users').child(name).child('details').child('book2_d').get().val()
    if book:
        database.child('users').child(name).child('details').update({"borrow":1,"book1":book,"book1_d":book_d,"book2":"","book2_d":""})
    else :
        database.child('users').child(name).child('details').update({"borrow":0,"book1":"","book1_d":"","book2":"","book2_d":""})

    book2=database.child('users').child(name).child('details').child('book2').get().val()
    email=database.child('users').child(name).child('details').child('email').get().val()
    reques_book = database.child('users').child(name).child('details').child('request_book').get().val()
    book2_d=database.child('users').child(name).child('details').child('book2_d').get().val()
    req_stat=database.child('users').child(name).child('details').child('req_stat').get().val()
    return render(request,"profile.html",{"message":message,"name":name,"book1":book,"book2":book2,"reques_book":reques_book,"email":email,"book1_d":book_d,"book2_d":book2_d,"req_stat":req_stat})

def book2(request):
    name = request.POST.get('name')
    presentday = datetime.now()
    date_format = "%d-%m-%Y"
    dueday = datetime.strptime(database.child('users').child(name).child('details').child('book2_d').get().val(),date_format)
    delta = presentday-dueday
    delt = int(delta.days)
    if delt<1:
        message="Book has submitted on time"
    else:
        delt = delt*10
        message="Book and fine of Rs."+str(delt)+" (Rs.10 per day) has submitted"

    book = database.child('users').child(name).child('details').child('book2').get().val()
    stock = int(database.child('books').child(book).child('stock').get().val())
    stock = stock +1
    database.child('books').child(book).update({"stock":stock})

    database.child('users').child(name).child('details').update({"borrow":1,"book2":"","book2_d":""})
    book=database.child('users').child(name).child('details').child('book1').get().val()
    book_d=database.child('users').child(name).child('details').child('book1_d').get().val()
    book2=""
    email=database.child('users').child(name).child('details').child('email').get().val()
    reques_book = database.child('users').child(name).child('details').child('request_book').get().val()
    book2_d=""
    req_stat=database.child('users').child(name).child('details').child('req_stat').get().val()
    return render(request,"profile.html",{"message":message,"name":name,"book1":book,"book2":book2,"reques_book":reques_book,"email":email,"book1_d":book_d,"book2_d":book2_d,"req_stat":req_stat})

def users(request):
    stat = request.POST.get('status')
    user = database.child('users').get()
    userss=""
    if stat == "active":
        for use in user.each():
            if database.child('users').child(use.key()).child('details').child('status').get().val()=="active":
                userss = userss + " " + use.key()
        usersss = userss.split()
        return render(request,"ausers.html",{"users":usersss})

    else:
        for use in user.each():
            if database.child('users').child(use.key()).child('details').child('status').get().val()=="inactive":
                userss = userss + " " + use.key()
        usersss = userss.split()
        return render(request,"iusers.html",{"users":usersss})

def librarians(request):
    lib_ids = database.child('librarians').get()
    lib=""
    for lib_id in lib_ids.each():
        lib = lib + " " +lib_id.key()
    libs = lib.split()
    return render(request,"librarians.html",{"librarians":libs})

def librarian_profile(request):
    session_id = request.POST.get('librarian')
    email = database.child('librarians').child(session_id).child('email').get().val()
    book=database.child('librarians').child(session_id).child('role').child('book').get().val()
    newbook=database.child('librarians').child(session_id).child('role').child('newbook').get().val()
    respond=database.child('librarians').child(session_id).child('role').child('respond').get().val()
    if book =="no":
        book=""
    if newbook =="no":
        newbook=""
    if respond =="no":
        respond=""
    return render(request,"librarian_profile.html",{"name":session_id,"email":email,"book":book,"newbook":newbook,"respond":respond})

def user_profile(request):
    session_id = request.POST.get('user')
    book1=database.child('users').child(session_id).child('details').child('book1').get().val()
    book2=database.child('users').child(session_id).child('details').child('book2').get().val()
    email=database.child('users').child(session_id).child('details').child('email').get().val()
    reques_book = database.child('users').child(session_id).child('details').child('request_book').get().val()
    book2_d=database.child('users').child(session_id).child('details').child('book2_d').get().val()
    book1_d=database.child('users').child(session_id).child('details').child('book1_d').get().val()
    status = database.child('users').child(session_id).child('details').child('status').get().val()
    return render(request,"user_profile.html",{"name":session_id,"book1":book1,"book2":book2,"reques_book":reques_book,"email":email,"book1_d":book1_d,"book2_d":book2_d,"status":status})

def astatus(request):
    name = request.POST.get('name')
    if database.child('users').child(name).child('details').child('status').get().val()=="active":
        message="User is already Active"
    else:
        database.child('users').child(name).child('details').update({"status":"active"})
        message="User is now Active"

    book1=database.child('users').child(name).child('details').child('book1').get().val()
    book2=database.child('users').child(name).child('details').child('book2').get().val()
    email=database.child('users').child(name).child('details').child('email').get().val()
    reques_book = database.child('users').child(name).child('details').child('request_book').get().val()
    book2_d=database.child('users').child(name).child('details').child('book2_d').get().val()
    book1_d=database.child('users').child(name).child('details').child('book1_d').get().val()
    return render(request,"user_profile.html",{"message":message,"name":name,"book1":book1,"book2":book2,"reques_book":reques_book,"email":email,"book1_d":book1_d,"book2_d":book2_d,"status":"active"})

def istatus(request):
    name = request.POST.get('name')
    if database.child('users').child(name).child('details').child('status').get().val()=="inactive":
        message="User is already Inactive"
    else:
        database.child('users').child(name).child('details').update({"status":"inactive","book1":"","book2":"","book1_d":"","book2_d":"","borrow":0})
        message="User is now Inactive"

    book1=database.child('users').child(name).child('details').child('book1').get().val()
    book2=database.child('users').child(name).child('details').child('book2').get().val()
    email=database.child('users').child(name).child('details').child('email').get().val()
    reques_book = database.child('users').child(name).child('details').child('request_book').get().val()
    book2_d=database.child('users').child(name).child('details').child('book2_d').get().val()
    book1_d=database.child('users').child(name).child('details').child('book1_d').get().val()
    return render(request,"user_profile.html",{"message":message,"name":name,"book1":book1,"book2":book2,"reques_book":reques_book,"email":email,"book1_d":book1_d,"book2_d":book2_d,"status":"inactive"})

def rol1Y(request):
    name= request.POST.get('name')
    database.child('librarians').child(name).child('role').update({"book":"yes"})
    email = database.child('librarians').child(name).child('email').get().val()
    newbook=database.child('librarians').child(name).child('role').child('newbook').get().val()
    respond=database.child('librarians').child(name).child('role').child('respond').get().val()
    book="yes"
    if newbook =="no":
        newbook=""
    if respond =="no":
        respond=""
    return render(request,"librarian_profile.html",{"message":"Role changed successfully","name":name,"email":email,"book":book,"newbook":newbook,"respond":respond})
 
def rol1N(request):
    name= request.POST.get('name')
    print(name)
    database.child('librarians').child(name).child('role').update({"book":"no"})
    email = database.child('librarians').child(name).child('email').get().val()
    newbook=database.child('librarians').child(name).child('role').child('newbook').get().val()
    respond=database.child('librarians').child(name).child('role').child('respond').get().val()
    book=""
    if newbook =="no":
        newbook=""
    if respond =="no":
        respond=""
    return render(request,"librarian_profile.html",{"message":"Role changed successfully","name":name,"email":email,"book":book,"newbook":newbook,"respond":respond})

def rol2Y(request):
    name= request.POST.get('name')
    database.child('librarians').child(name).child('role').update({"newbook":"yes"})
    email = database.child('librarians').child(name).child('email').get().val()
    book=database.child('librarians').child(name).child('role').child('book').get().val()
    respond=database.child('librarians').child(name).child('role').child('respond').get().val()
    newbook="yes"
    if book =="no":
        book=""
    if respond =="no":
        respond=""
    return render(request,"librarian_profile.html",{"message":"Role changed successfully","name":name,"email":email,"book":book,"newbook":newbook,"respond":respond})

def rol2N(request):
    name= request.POST.get('name')
    database.child('librarians').child(name).child('role').update({"newbook":"no"})
    email = database.child('librarians').child(name).child('email').get().val()
    book=database.child('librarians').child(name).child('role').child('book').get().val()
    respond=database.child('librarians').child(name).child('role').child('respond').get().val()
    newbook=""
    if book =="no":
        book=""
    if respond =="no":
        respond=""
    return render(request,"librarian_profile.html",{"message":"Role changed successfully","name":name,"email":email,"book":book,"newbook":newbook,"respond":respond})

def rol3Y(request):
    name= request.POST.get('name')
    database.child('librarians').child(name).child('role').update({"respond":"yes"})
    email = database.child('librarians').child(name).child('email').get().val()
    book=database.child('librarians').child(name).child('role').child('book').get().val()
    newbook=database.child('librarians').child(name).child('role').child('newbook').get().val()
    respond="yes"
    if book =="no":
        book=""
    if newbook =="no":
        newbook=""
    return render(request,"librarian_profile.html",{"message":"Role changed successfully","name":name,"email":email,"book":book,"newbook":newbook,"respond":respond})

def rol3N(request):
    name= request.POST.get('name')
    database.child('librarians').child(name).child('role').update({"respond":"no"})
    email = database.child('librarians').child(name).child('email').get().val()
    book=database.child('librarians').child(name).child('role').child('book').get().val()
    newbook=database.child('librarians').child(name).child('role').child('newbook').get().val()
    respond=""
    if book =="no":
        book=""
    if newbook =="no":
        newbook=""
    return render(request,"librarian_profile.html",{"message":"Role changed successfully","name":name,"email":email,"book":book,"newbook":newbook,"respond":respond})

def newlib(request):
    return render(request,"new_librarian.html")

def new_librarian(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    book=request.POST.get('book')
    newbook=request.POST.get('newbook')
    respond=request.POST.get('respond')

    try:
        user=authe.create_user_with_email_and_password(email,passw)
    except:
        message="Please input valid email and password"
        return render(request,"new_librarian.html",{"message":message})

    names = name.split()
    name=""
    for nam in names:
        name = name + nam
    flag = 0
    alllibs = database.child('librarians').get()
    for lib in alllibs.each():
        if name == lib.key():
            flag=1
            break
    
    if flag:
        message="Librarian name already exists"
        return render(request,"new_librarian.html",{"message":message})

    else: 
        if book == "on":
            book = "yes"
        else:
            book = "no" 

        if newbook == "on":
            newbook = "yes"
        else:
            newbook = "no" 

        if respond == "on":
            respond = "yes"
        else:
            respond = "no"  
          
        data={"email":email}
        database.child("librarians").child(name).set(data)
        data={"book":book,"newbook":newbook,"respond":respond}
        database.child("librarians").child(name).child("role").set(data)
        return render(request,"new_librarian.html",{"message":"Librarian created successfully"})


