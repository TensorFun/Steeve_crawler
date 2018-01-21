import requests
import re
from bs4 import BeautifulSoup
import json
import pandas as pd
domain_name = 'https://www.dice.com'

Key_work = 'Backend'
Key_location = 'New York, NY'

herf = []
## page 1-30
for i in range(13):
    print('Deal'+str(i+1)+'page')
    response_page = requests.get('https://www.dice.com/jobs/q-'+Key_work+'-l-'+Key_location+'-radius-30-startPage-'+str(i+1)+'-jobs?')
    soup = BeautifulSoup(response_page.text,'lxml')
    # page contains 30 url
    for i in range(30):
        herf.append(domain_name + soup.find("",{"id":"position"+str(i)}).get('href'))
        
for i,work in enumerate(herf):
    try:
        response_work = requests.get(work)
        soup = BeautifulSoup(response_work.text,'lxml')
        jobTitle = soup.find("",{"class":"jobTitle"}).text
        jobEmployer = soup.find("",{"class":"employer"}).text.replace('\n','').replace('\t','')
        jobLocation = soup.find("",{"class":"location"}).text.replace('\n','')
        jobPostTime = soup.find("",{"class":"posted hidden-xs"}).text
        out = []
        foo = soup.find_all("",{"class":"row job-info"})
        for o in foo:
            out.append(o.text.replace('\n','').replace('\t',''))
            
    except AttributeError:
        jobTitle='None'
        jobEmployer='None'
        jobLocation='None'
        jobPostTime='None'
        foo='None'
    
        
    try:
        skills = out[0]
        employmentType = out[1]
        baseSalary = out[2]   
    except IndexError:
        skills = 'None'
        employmentType = 'None'
        baseSalary = 'None'
        
    
    str1 = str(soup.find("",{"id":"jobdescSec"}))
    soup = BeautifulSoup(str1.replace('<br/>','\n'),'lxml')
    jobDescription = soup.text
    url = work ##
    if i ==0:
        data = {Key_work:[{"jobTitle":jobTitle,
                 "jobEmployer":jobEmployer,
                 "jobLocation":jobLocation,
                 "jobPostTime":jobPostTime,
                 "skills":skills,
                 "employmentType":employmentType,
                 "baseSalary":baseSalary,
                 "jobDescription":soup.text,
                 "url":url}]}
    else:
        add_data = {     "jobTitle":jobTitle,
                         "jobEmployer":jobEmployer,
                         "jobLocation":jobLocation,
                         "jobPostTime":jobPostTime,
                         "skills":skills,
                         "employmentType":employmentType,
                         "baseSalary":baseSalary,
                         "jobDescription":soup.text,
                         "url":url                          }
        data[Key_work].append(add_data)
    if i%10==0:
        print('deal with'+ str(i) +' work is OK')

with open("Backend-NY.json","w") as f:
    json.dump(data,f)
    print('ok')
