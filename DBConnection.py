import pymongo
from ZaubaCorp1 import get_details
from selenium.common.exceptions import TimeoutException
from pymongo import monitoring,MongoClient
from ProcessNames import ProcessNames

#def update_organisation(doc,details):
#    details[""]

def save_in_people(details):
    col_org = db_sales["organisations"]
    col_people, col_names = db_sales["people"],db_sales["people_names"]
    doc = col_org.find_one({"name": details["name"]})
    print("id",doc["_id"])
    if doc != None:
          #update_organisation(doc,details)
          if "email" in details.keys():
                for email in details["email"]:
                        if type(email) == str and email != "" :
                            info = {}
                            info["organisation_id"] = doc["_id"]
                            info["email"] = email
                            info["email_type"] = "personal"
                            info["status"] = True
                            print(info)
                            col_people.insert_one(info)
                            doc["person_count"] = doc["person_count"]+ len(details["email"])
                            col_org.update({"_id":doc["_id"]},doc)
          if "Director Names" in details.keys():
                for name in details["Director Names"]:
                        if type(name) == str and name!= "":
                              info = {}
                              info["organisation_id"] = doc["_id"]
                              info["name"] = name
                              info["status"] = True
                              print(info)
                              col_names.insert(info)




def save_in_zauba_db(details):
        mycol = db_sales["Zauba_information_final"]
        mycol.save(details)
        save_in_people(details)



def createConnection():
        mycol = db_sales["hubspot_organisations"]
        i = 20
        for doc in mycol.find(no_cursor_timeout=True)[0:100]:
           information = {}
           i=i+1
           try:
                company_name = doc["name"]
                print("----",company_name,"------",i)
                details,name,email = get_details(company_name)
           except KeyError:
                 print("KeyError 'name'")
                 continue
           except TimeoutException:
                details,name,email = get_details(company_name)

           information["name"] = company_name
           try:
                information["domain"] = doc["domain"]
           except KeyError:
                pass
           if len(email)>0:
               information["email"] = email
           elif len(name)>0:
                   pn = ProcessNames(name)
                   verified_email = pn.email_generate_verify()
                   information["email"] = verified_email
           if len(name)>0:
               information["Director Names"] = name
           if len(details)>1:
                information["Details"] = details
           if len(information)>2:
               for name in information["Director Names"]:
                    name_arr = name.strip().split(" ")
                    for email in information["email"]:
                        if email.lower().find(name_arr[0].lower())>-1:
                            information["email name"] = name.strip()
               print("save")
               save_in_zauba_db(information)

#monitoring.register(ComandLogger())
myclient = pymongo.MongoClient("mongodb://localhost:27017/",serverSelectionTimeoutMS = 900000000)
db_sales = myclient["Intelligense_mongo"]
createConnection()
