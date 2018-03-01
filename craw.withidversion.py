import requests
import re
from bs4 import BeautifulSoup
import json
domain_name = 'https://www.dice.com'

Key_work = 'Backend'
Key_location =''
key_main=domain_name+'/jobs/'+'q-'+Key_work+'-l-'+Key_location+'-radius-30-startPage-1-jobs?'

response_main = requests.get(key_main)
soup = BeautifulSoup(response_main.text,'lxml')
pages = int(str(soup.find("",{"id":"posiCountId"}).text).replace(',',''))//30
print('Total have '+str(pages)+' pages')


## Add all pages's work
herf = []
page=0
print('start')
for i in range(pages):
    page=i+1
    response_page = requests.get(domain_name+'/jobs/'+'q-'+Key_work+'-l-'+Key_location+'-radius-30-startPage-'+str(page)+'-jobs?')
    soup1 = BeautifulSoup(response_page.text,'lxml')
    # page contains 30 urls
    for i in range(30):
        tmp = domain_name + soup1.find("",{"id":"position"+str(i)}).get('href')
        herf.append(tmp)    
    print('page '+ str(page)+' is finished')
print(len(herf))


## Crawler Data
flag=True
controll=False
for i,work in enumerate(herf):
    ## Beause some works are broken or missing, I use "try except" to avoid error.
    try:
        response_work = requests.get(work)
        soup = BeautifulSoup(response_work.text,'lxml')
        ## Crawler we need tags
        jobTitle = soup.find("",{"class":"jobTitle"}).text
        ## replace some extra symbol
        jobEmployer = soup.find("",{"class":"employer"}).text.replace('\n','').replace('\t','')
        jobLocation = soup.find("",{"class":"location"}).text.replace('\n','')
        jobPostTime = soup.find("",{"class":"posted hidden-xs"}).text
        jobID = soup.find("",{"class":"company-header-info"}).text
        jobID = jobID.replace('\n','').split(':')[2].strip().replace('-','')
        out = []
        ## tag job-info is a array .
        foo = soup.find_all("",{"class":"row job-info"})
        for o in foo:
            out.append(o.text.replace('\n','').replace('\t',''))
            
    except AttributeError:
        jobTitle='None'
        jobEmployer='None'
        jobLocation='None'
        jobPostTime='None'
        foo='None'
        jobID='None'
        
    if jobLocation!=Key_location and controll==True:
        continue
    else:
        try:
            ## Beause the work of dice.com's html format is not fixed,I use "try except" to avoid error.
            skills = out[0]
            employmentType = out[1]
            baseSalary = out[2]

        except IndexError:
            skills = 'None'
            employmentType = 'None'
            baseSalary = 'None'

        ## Jobdescription
        str1 = str(soup.find("",{"id":"jobdescSec"}))
        soup = BeautifulSoup(str1.replace('<br/>','\n').replace('</li>','\n').replace('</strong>','\n').replace('</p>','\n').replace('<p>','\n'),'lxml')
        jobDescription = soup.text
        ## work's url
        url = work ##

        ## Save data to json format 
        
        if flag==True:
        
            data = {Key_work:[{
                     "jobID":jobID,
                     "jobTitle":jobTitle,
                     "jobEmployer":jobEmployer,
                     "jobLocation":jobLocation,
                     "jobPostTime":jobPostTime,
                     "skills":skills,
                     "employmentType":employmentType,
                     "baseSalary":baseSalary,
                     "jobDescription":soup.text,
                     "url":url}]}
            flag=False
        
        else:
            add_data = {    "jobID":jobID,  
                            "jobTitle":jobTitle,
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
        print('deal with '+ str(i) +' work is OK')

        
with open("Backend.nofilter.json","w") as f:
    json.dump(data,f)
    print('ok')
