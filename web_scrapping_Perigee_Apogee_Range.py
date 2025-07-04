import re
import requests
from bs4 import BeautifulSoup as bs
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def getting_Perigee_Apogee(i):
    try:
        page = requests.get('https://www.n2yo.com/satellite/?s='+str(i), verify=False) #39035, 40025
    except:
        error_id=str(i)+","
        textfile= open("C:\\Users\\Joel\\Documents\\Python\\email\\Perigee_Apogee_ERROR.txt", "a")
        textfile.write(error_id)
        textfile.close()
    #print(page)
    #print(page.content)
    soup = bs(page.text, 'html.parser')
    #print(soup)

    td_tags= soup.find_all("td")
    #print(td_tags)

    str_td_tags=str(td_tags)
    #print(str_br_tags)

    pattern_finded_Perigee= re.findall(r"<b>Perigee</b>:\s.+.\d+\skm", str_td_tags) 
    pattern_finded_Apogee= re.findall(r"<b>Apogee</b>:\s.+\d+.\d+\skm", str_td_tags)
    #print(pattern_finded_Perigee)
    #print(len(pattern_finded_Perigee))
    #print(pattern_finded_Apogee)

    if len(pattern_finded_Perigee) > 0 and len(pattern_finded_Apogee) > 0:
    
        str_Perigee= pattern_finded_Perigee[0]
        str_Apogee= pattern_finded_Apogee[0]
        #print(str_Perigee)
        #print(str_Apogee)
        str_Perigee= str_Perigee[15:-2]
        str_Apogee= str_Apogee[14:-2]

        #print(str_Perigee)
        #print(str_Apogee)

        if len(str_Perigee) > 7:
            str_Perigee = str_Perigee.replace(",", "")
            #print(str_Perigee)
        if len(str_Apogee) > 7:
            str_Apogee = str_Apogee.replace(",", "")
            #print(str_Apogee)

        #print(float(str_Perigee))
        #print(float(str_Apogee))

        lim_sup= 35836.0
        lim_inf= 35736.0

        if float(str_Perigee) <= lim_sup and float(str_Perigee) >= lim_inf:
            write= str(i)+"\nPerigee: "+str_Perigee+"\nApogee: "+str_Apogee
            textfile= open("C:\\Users\\Joel\\Documents\\Python\\email\\Perigee_Apogee_Range_v2.txt", "a")
            textfile.write(write+"\n\n")
            textfile.close()
            #print("Apendeamos por Perigee")
        elif float(str_Apogee) <= lim_sup and float(str_Apogee) >= lim_inf:
            write= str(i)+"\nPerigee: "+str_Perigee+"\nApogee: "+str_Apogee
            textfile= open("C:\\Users\\Joel\\Documents\\Python\\email\\Perigee_Apogee_Range_v2.txt", "a")
            textfile.write(write+"\n\n")
            textfile.close()
            #print("Apendeamos por Apogee")
        #elif float(str_Apogee) >= lim_sup and float(str_Perigee) <= lim_inf:
        #    write= str(i)+"\nPerigee: "+str_Perigee+"\nApogee: "+str_Apogee
        #    textfile= open("C:\\Users\\Joel\\Documents\\Python\\email\\Perigee_Apogee_Range.txt", "a")
        #    textfile.write(write+"\n\n")
        #    textfile.close()
        #    #print("Apendeamos porque cruza Radio Geostacionario")

for i in range(1, 100000):
    print(i)
    getting_Perigee_Apogee(i)