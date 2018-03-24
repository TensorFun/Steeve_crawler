
# coding: utf-8

# In[2]:


import requests
import re
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool
import time 
domain_name = 'https://www.dice.com'


# In[3]:


## Input you want
Key_work = 'Frontend'
Key_location =''
key_main=domain_name+'/jobs/'+'q-'+Key_work+'-l-'+Key_location+'-radius-30-startPage-1-jobs?'
key_main


# In[4]:


## Calculate Job Pages
response_main = requests.get(key_main)
soup = BeautifulSoup(response_main.text,'lxml')
pages = int(str(soup.find("",{"id":"posiCountId"}).text).replace(',',''))//30
print('Total have '+str(pages)+' pages')


# In[5]:


## Add all pages's work
herf = []
page=0
for i in range(pages-10):
    page=i+1
    response_page = requests.get(domain_name+'/jobs/'+'q-'+Key_work+'-l-'+Key_location+'-radius-30-startPage-'+str(page)+'-jobs?')
    soup1 = BeautifulSoup(response_page.text,'lxml')
    # every page contains 30 urls
    for i in range(30):
        tmp = domain_name + soup1.find("",{"id":"position"+str(i)}).get('href')
        herf.append(tmp)
        
    if page%30==0:
        print('page '+ str(page)+' is finished')
                                
print("Total have : ",len(herf))


# In[6]:


def fetch_article_content(url):
    try:
        response_work = requests.get(url)
        soup = BeautifulSoup(response_work.text,'lxml')
        jobTitle = soup.find("",{"class":"jobTitle"}).text
        jobEmployer = soup.find("",{"class":"employer"}).text.replace('\n','').replace('\t','')
        jobLocation = soup.find("",{"class":"location"}).text.replace('\n','')
        jobPostTime = soup.find("",{"class":"posted hidden-xs"}).text
        jobID = soup.find("",{"class":"company-header-info"}).text
        jobID = jobID.replace('\n','').split(':')[2].strip().replace('-','')
        ## tag job-info is a array .
        foo = soup.find_all("",{"class":"row job-info"})
        
        out = []
        for o in foo:
            out.append(o.text.replace('\n','').replace('\t',''))
            
    except AttributeError:
        jobTitle='None'
        jobEmployer='None'
        jobLocation='None'
        jobPostTime='None'
        foo='None'
        jobID='None'
        #jobDescription=''   
        
    try:
        jobskillss = out[0]
        jobemploymentType = out[1]
        jobbaseSalary = out[2]

    except IndexError:
        jobskillss = 'None'
        jobemploymentType = 'None'
        jobbaseSalary = 'None'
        
## Jobdescription
    str1 = str(soup.find("",{"id":"jobdescSec"}))
    soup = BeautifulSoup(str1.replace('<br/>','\n').replace('</li>','\n').replace('</strong>','\n').replace('</p>','\n').replace('<p>','\n'),'lxml')
    jobDescription = soup.text
    joburl = url
    
    return((jobTitle,jobEmployer,jobLocation,jobPostTime,jobID,jobskillss,jobemploymentType,jobbaseSalary,joburl,jobDescription))


# In[ ]:


def load_to_json(content_arry):
    flag=True
    for i in content_arry:
        jobTitle = i[0]
        jobEmployer = i[1]
        jobLocation = i[2]
        jobPostTime = i[3]
        jobID = i[4]
        jobskills = i[5]
        jobemploymentType = i[6]
        jobbaseSalary = i[7]
        joburl = i[8]
        jobDescription = i[9]
        
        if flag==True:
            data = {Key_work:[{
                         "jobID":jobID,
                         "jobTitle":jobTitle,
                         "jobEmployer":jobEmployer,
                         "jobLocation":jobLocation,
                         "jobPostTime":jobPostTime,
                         "jobskills":jobskills,
                         "jobemploymentType":jobemploymentType,
                         "jobbaseSalary":jobbaseSalary,
                         "joburl":joburl,
                         "jobDescription":jobDescription,
                             }]}
            flag=False
            
            
        else:
            add_data = {    "jobID":jobID,  
                            "jobTitle":jobTitle,
                            "jobEmployer":jobEmployer,
                            "jobLocation":jobLocation,
                            "jobPostTime":jobPostTime,
                            "jobskills":jobskills,
                            "jobemploymentType":jobemploymentType,
                            "jobbaseSalary":jobbaseSalary,
                            "joburl":joburl,
                            "jobDescription":jobDescription  }
            data[Key_work].append(add_data)
    return data


# In[ ]:


#testing
post_links = herf
#post_links = herf[1:100]
start = time.time()
with Pool(processes=20) as pool:
    contents = pool.map(fetch_article_content, post_links)
end = time.time()
print(end-start)


# In[ ]:


result = load_to_json(contents)


# In[ ]:


#過濾條件#

#rules = ['android']
#rules = ['backend','software engineer','back-end']
rules = ['frontend','front-end','UI','web design','web designer','front end']
#rules = ['system analyst','systems analyst']
#rules = ['network security','security engineer','systems security']
#rules = ['project management']


# In[ ]:


data = {Key_work:[]}
for i in range(len(result[Key_work])):
    jobtitle = result[Key_work][i]['jobTitle'].lower().replace('/',' ').replace(')','').replace('(','').replace(',','')
    #print(jobtitle)
    for rule in rules:
        if rule in jobtitle:
            data[Key_work].append(result[Key_work][i])


# In[ ]:


with open(Key_work+".json","w") as f:
    json.dump(data,f)
    print('Save to json is ok')


# In[ ]:


get_ipython().system('jupyter nbconvert --to script Crawer_dice.com.faster.ipynb')

