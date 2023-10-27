
def Login(request):
    if (request.method == "POST"):
        ip_add = "{0}".format(request.get_host())
        print("ip", ip_add)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        username = request.POST.get("username")
        passw = request.POST.get("password")
        password = passw.encode("utf-8")
        ln = LoginIP(username=username, IP_Address=ip_add)
        ln.save()

        user = Allusers.objects.get(username=username)
        print("get", user.username)
        whash = user.password
        if user.is_superuser == True:
            user = auth.authenticate(username=username, password=passw)
            auth.login(request, user)
            messages.success(request, 'Login sucessfully!..')
            print("admin login")
            return HttpResponseRedirect("/admin/")
        # else:
        #     print(username)
        #     print(whash)
        #     user = auth.authenticate(username=username,password=passw)
        #     print("usdff",user)
        #     print("normal user")
        userid = user.users_id
        global useridlist
        status = user.is_active
        print("user", user.username)
        hash = whash.encode("utf-8")
        if result['success'] and bcrypt.checkpw(password, hash):
            if (user is not None):
                print("usersdffsd", user.username)
                # ir=Userpermissions.objects.filter(userid=userid).values('permissionid')[0]['permissionid']
                useridlist[0] = userid
                useridlist[1] = user.email
                useridlist[2] = user.username
                permissionname = Permissions.objects.filter(permissionid=Userpermissions.objects.filter(
                    userid=userid).values('permissionid')[0]['permissionid']).values('permission_name')[0]['permission_name']
                if permissionname == 'influencer_permission' and status == False:
                    return HttpResponseRedirect("/index1/")

                # elif ay.exists() and pr.adsagency_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the manager admin path
                # elif user.Role_Type == "Manager" and pr.Manager_permission == True:
                #     return HttpResponseRedirect("/index2/")

                # # Enter the Relationship Manager admin path
                # elif user.Role_Type == "Relationship Manager" and pr.RM_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the Accountant admin path
                # elif user.Role_Type == "Accountant" and pr.Account_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the KYC admin path
                # elif user.Role_Type == "KYC Manager" and pr.KycManager_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the  admin path
                # elif user.Role_Type == "Admin" and pr.Admin_permission == True:
                #     # return HttpResponseRedirect("/")

                # # Enter the  Super admin path
                # elif user.Role_Type == "Super Admin" and pr.Superadmin_permission == True:
                #     # return HttpResponseRedirect("/")
                else:
                    return HttpResponseRedirect("/")
            else:
                messages.error(request, "Username or Password is Incorrect")
        else:
            messages.error(request,
                           'Invalid reCAPTCHA. Please try again.')
    fot = FooterDetail.objects.all()
    return render(request, "Normal-User/login.html", {"footer": fot, "message": 'Login sucessfully!..'})

