from .AccountVerify import AccountVerify
import smtplib,dns
from dns import resolver
import re,random
import socket


weight = 0
def emailVerifier(email_address):
    #step 1
    addressToVerify = email_address
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    if match == None:
        print('Bad Syntax in ' + addressToVerify)
        raise ValueError('Bad Syntax')
    else:
        weight = random.uniform(20.0,30.0)


    #step 2 get the mx record(available record name)
    domain_name = email_address.split('@')[1]
    try:
        records = resolver.query(domain_name, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        host = socket.gethostname()
        server = smtplib.SMTP()
        code,msg = server.connect(mxRecord)
        server.quit()
        if code in range(200,225):
            weight = checkUsername(addressToVerify,mxRecord)
            print(weight)
            if weight >= 85:
               return [{'status':"verified"},{'confidence':weight}]
            else:
                return [{'status':"not verified"},{'confidence':weight}]
        else:
            weight = random.uniform(55.0,65.0)
            return [{'status':"not verified"},{'confidence':weight}]
    except resolver.NXDOMAIN:
       weight =  random.uniform(40.0,50.0)
       return [{'status':"not verified"},{'confidence':weight}]


def checkUsername(addressToVerify,mxRecord):
    print(mxRecord)
    ac = AccountVerify(addressToVerify)
    bool = True
    if mxRecord.find("google")> -1:
        bool = ac.gmail_verification()
    elif mxRecord.find("yahoo")> -1:
        bool = ac.yahoo_verification()
    elif mxRecord.find("outlook")> -1:
        bool = ac.outlook_verification()
    else:
        bool = ac.check_through_all()
    if bool == True:
        return random.uniform(85.0,99.0)
    else:
        return random.uniform(65.0,75.0)
