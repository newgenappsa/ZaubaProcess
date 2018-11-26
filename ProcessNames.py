from nltk import word_tokenize
from emailGenerator import username
from emailverifier import emailverifier


class ProcessNames:

    def __init__(self):
        self.replace_list = ["Mr.","Mrs.","Ms.","Dr."]
        self.email_list = []
        self.valid_mail = []
        self._name_list, self.rows = [], -1

    def name_provide(self,name_list):
        self._name_list = name_list
        print("name_list",self._name_list)

    def names_yahoo(self,name_list):
        self._name_list = [name["name"].replace(replace_str,"") for name in name_list for replace_str in self.replace_list if name["name"].find(replace_str)>-1]
        return self._name_list

    def email_generate(self,domain):
            for name in self._name_list:
                name = name.replace("'","").replace(".","")
                name_tokens = word_tokenize(name)
                print("name_tokens",name_tokens,len(name_tokens))
                if len(name_tokens)< 3:
                    print("here")
                    self.email_list.append(username(name_tokens[0],name_tokens[1],domain))
            return self.email_list

    def email_verified(self):
            for email in self.email_list:
                 print("@",email)
                 response = emailverifier.emailVerifier(email)
                 if response[0]["status"] == "verified":
                     self.valid_mail.append(email)
                     continue
                 elif response[1]["confidence"] > 65:
                     continue
                 elif int(response[1]["confidence"]) in range(50,55):
                     self.valid_mail.extend(email_pattern)
                     break
                 else:
                     break
            return self.valid_mail

    def email_exists(self,emails):
        print(emails)
        if self.rows == -1:
            for email in emails:
                print(email,emails.index(email))
                response = emailverifier.emailVerifier(email)
                if response[0]["status"] == "verified":
                    self.rows = emails.index(email)
                    print('email and row ',email,self.rows)
                    self.valid_mail.append(email)
                    return True
        else:
            print(emails[self.rows])
            response = emailverifier.emailVerifier(emails[self.rows])
            if response[0]["status"] == "verified":
                   self.valid_mail.append(emails[self.rows])
                   return True
            else:
                self.rows = -1
                self.valid_mail.append(self.email_exists(emails))
        print(self.valid_mail)


    def email_generate_verify(self,domain):
        emails = self.email_generate(domain)
        for email in emails:
            email_verified = self.email_exists(email)
        return self.valid_mail
