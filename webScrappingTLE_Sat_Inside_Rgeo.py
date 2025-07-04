import re
import requests
from bs4 import BeautifulSoup as bs
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


file = open("C:/Users/Joel/Documents/Python/email/txt/Sat_Inside_Rgeo_v2.txt", "r")
#print(file.read())
str_P_A_R=file.read()
#print(str_P_A_R)

NoradID= re.findall(r"(\d+)\nPerigee", str_P_A_R)
#print(NoradID)


def getting_tle(i):
    
        page = requests.get('https://www.n2yo.com/satellite/?s='+str(i)+'#results', verify=False)
        soup = bs(page.text, 'html.parser')
        pre_tags = soup.find("pre")
        str_pre_tags=str(pre_tags)
    #print(str_pre_tags)
        if len(str_pre_tags) > 15:
            Line1_TLE= str_pre_tags[7:76]
            #print(Line1_TLE)
            Line2_TLE= str_pre_tags[78:-7]
            #print(Line2_TLE)
            data= i+"\n"+ Line1_TLE+"\n"+ Line2_TLE+"\n\n"
            #print(data)
            textfile= open("C:\\Users\\Joel\\Documents\\Python\\email\\txt\\tle_sat_inside.txt", "a")
            textfile.write(data)
            textfile.close()
    #except:
    #    error_id=str(i)+","
    #    textfile= open("C:\\Users\\Joel\\Documents\\Python\\email\\txt\\tle_sat_inside_ERROR.txt", "a")
    #    textfile.write(error_id)
    #    textfile.close()

    
    
    #print(pre_tags)
    

for i in NoradID:
    print(i)
    getting_tle(i)
    