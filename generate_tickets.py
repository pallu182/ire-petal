#!/usr/bin/python

import commands

# Take location where REL ticket needs to be generated
ticket_location = raw_input("Enter the directory name where RELEASE ticket needs to be generated : ")

# Input user id 1 and user id2
user1 = raw_input("Enter userid1 : ")
user2 = raw_input("Enter userid2 : ")

# Product name input
prod_names = raw_input("Enter the product list in comma seperated list : ")
# for each product name 
for prod in prod_names.split(",") :
    prod.strip()
    # get otp of userid1
    otp1 = raw_input("Enter the OTP of %s :" %user1)
    # get otp of userid2
    otp2 = raw_input("Enter the OTP of %s :" %user2 )

    ticloc = ticket_location.strip() + "/" + "%s_REL.tic" %prod

    print "/router/bin/code_sign swims ticket create -products %s \
         -reason tst -username1 %s -authType OTP -password1 %s -ticketType RELEASE \
         -username2 %s -password2 %s -out %s " %(prod,user1,otp1,user2,otp2,ticloc)
    # generate ticket in the directory
    commands.getstatusoutput("/router/bin/code_sign swims ticket create -products %s \
    -reason tst -username1 %s -authType OTP -password1 %s -ticketType RELEASE \
    -username2 %s -password2 %s -out %s " %(prod,user1,otp1,user2,otp2,ticloc))

