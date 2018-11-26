from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import urllib3
import unicodedata



dict_details = {}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def loop_through_links(links):
    key_bool,key,value,names,email_id = True,[],[],[],''
    req  = urllib3.PoolManager()
    res = req.request('GET',links)
    soup = BeautifulSoup(res.data, 'html.parser')
    contact_detail = soup.find_all("div",class_ = "col-12")
    #contact_detail = soup.find_all("div",class_ = "col-lg-6 col-md-6 col-sm-12 col-xs-12")
    for contact in contact_detail:
       try:
            if contact.find("h4").get_text() == "Contact Details":
                email_id = contact.find("p").get_text().replace(" Email ID: ","")
                print(email_id)
       except AttributeError:
                continue
    try :
      info = soup.find("div",class_="container information").text
      comp_details = soup.find("div",class_="col-lg-12 col-md-12 col-sm-12 col-xs-12")
      comp_tbodies = comp_details.find_all("tbody")
      for comp_tbody in comp_tbodies:
          p_texts = comp_tbody.find_all("p")
          for p_text in p_texts:
             text = p_text.get_text()
             #print(key_bool)
             if key_bool == True:
                 key.append(text)
             else:
                 value.append(text)
             key_bool = not key_bool

      tables = soup.find_all("table",class_="table table-striped")
      for table in tables:
          #print(table.get_text())
          tbody = tables[7].find("tbody")
          trs = tbody.find_all("tr",class_="accordion-toggle main-row")
          for tr in trs:
              tds = tr.find_all("td")
              for td in tds:
                p = td.find("p")
                text = p.text
                names.append(text)
    except AttributeError:
      pass
    #print(names)
    return key,value,names,email_id



def get_details(account):
    try:
        dict_det,name,details,email_id= {},[],[],[]
        replace_list = ['.','inc','ltd','corporation','corp','com','co','industry','pty','pt','private','&',"'",',llc','au','org','net','inc','in']
        links,phone,name,branch= [],[],[],[]
        #array_words = word_tokenize(account)
        input_,link = account.replace(" ","+")+"+zauba",[]
        url = "https://www.google.co.in/search?q="+input_+"&oq="+input_+"+&aqs=chrome.0.69i59j69i60j69i57j0l3.6896j0j4&sourceid=chrome&ie=UTF-8"
        req  = urllib3.PoolManager()
        res = req.request('GET',url)
    except UnicodeEncodeError:
         return details,list(set(name)),list(set(email_id))
    for replace in replace_list:
        account = account.lower().replace(replace,'')
    soup = BeautifulSoup(res.data, 'html.parser')
    div_container = soup.find_all("div",class_ = "g")
    for div in div_container:
        #print(div)
        a_tag = str(div.find('a'))
        #print(a_tag)
        start = a_tag.find("https")
        end = a_tag.find(";")
        link_a = a_tag[start:end]
        if link_a.find("www.zaubacorp.com")> -1 and link_a.lower().replace("-","").find(account)>-1 :
            links.append(link_a.replace("&amp",""))
    for link in links:
        key,value,names,email = loop_through_links(link)
        if email != '':
           email_id.append(email)
        for i in range(0,len(key)-1):
            key_ = key[i].replace(".",'')
            dict_det[key_] = value[i]
        details.append(dict_det)
        #print(names)
        i=1
        while i < len(names):
            #print(names[i])
            name.append(names[i])
            i = i+5
    #print(details,set(name))
    return details,list(set(name)),list(set(email_id))

#get_details("LähiTapiola")
