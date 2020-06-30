import requests
import re
from bs4 import BeautifulSoup
import os
import time
import datetime


def monthname(mydate):
    mydate = datetime.datetime.now()
    m = mydate.strftime("%B")
    return(m)

def Brisbane(epoch):
    a = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(epoch))
    return(a)


def inputCSVfile(csvfile):
    list1= []
    with open(csvfile, 'r') as f:
        for i in f:
            j = i.split(',')
            
            le = len(j)
            j[le - 1] = (j[le- 1]).strip()
            list1.append(j)
        return(list1)

def createCSVfileWCD(inputlist , name):
    with open( name , 'w') as f:
        for i in inputlist:
            f.write(str(i))
            f.write('\n')
        return(f)
def createCSVfile(inputlist , name):
    with open( name , 'w') as f:
        for i in inputlist:
            k = 0
            for item in i:
                f.write(str(item) + ',')
                k = k+1
            f.write('\n')
        return(f)
headers  = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}

print('Enter Username')
login = input()
print('Enter Password')
passw = input()
login_data = { 'login': login,
               'password': passw,   
               'remember': '63072000'
               }

Working_Directory = os.getcwd().replace("\\","/")
print(Working_Directory )
t2 = 0
ii = 0
TU = "BCC Volume Data"
previousoutput = []
pt = 150000

while True:
    try:
        with requests.Session() as s:
            url = "https://www.data.brisbane.qld.gov.au/"
            r = s.get(url, headers = headers)

            soup = BeautifulSoup(r.content, 'html.parser')
            login_data['form_build_id'] = soup.find('input', attrs = {'name': 'form_build_id'})['value']
            url1 = "https://www.data.brisbane.qld.gov.au/data/login_generic?came_from=/data/user/logged_in"
            r = s.post(url1, data = login_data, headers = headers)
            while True:
                try:
                    t = int(time.time())
                    datee = datetime.datetime.strptime(str(Brisbane(t)),"%d-%m-%Y %H:%M:%S" )
                    m = datee.month
                    y = datee.year
                    d = datee.day
                    
                    m_name = monthname(Brisbane(t))
                    if t2!=0:
                        if d!=d1:
                            File_Tracker_TU1 =[]
                            File_Tracker_VP1 =[]
                            File_Tracker_SA1 =[]
                    d1 = d
                    t2 = 1
                    ii= ii+1
                    ttt = str(d)+"-"+str(m)+"-"+str(y)
                    ttt1 = str(m_name)+" ,"+str(y)
                    ii= ii+1
                    TUdirectory = Working_Directory + "/" + TU + "/" + 'BCC Vol '+str(ttt1)
                    if not os.path.exists(TUdirectory):
                        os.makedirs(TUdirectory)
                    TUdirectory2= TUdirectory+ "/"+ 'BCC Vol '+str(ttt)
                    if not os.path.exists(TUdirectory2):
                        os.makedirs(TUdirectory2)

                    #1...............Parking - Stations : Number of vacant spaces at Brisbane City Council’s 2 parking station
                    # a) Parking — Stations — Available spaces — TXT
                    URL = "https://www.data.brisbane.qld.gov.au/data/dataset/56e19d91-d571-4b45-bfdf-f0f00aeb2343/resource/651f7be1-c183-48b5-96a8-fe372e91adab/download/traffic-data-at-int.json"
                    r1a = s.get(URL, headers = headers)
                    b = str(r1a.content)
                    Output = []
                    heading = ["Dbid" , "Recorded date" , "Recorded time" , "ct" , "Link_plan" , "Married" , "ss" , "tsc" , "lane" , "ds1" , "mf1" , "rf1" , "ds2" , "mf2" , "rf2" , "ds3" , "mf3" , "rf3" , "ds4" , "mf4" , "rf4" , "ds" , "mf5" , "rf5"]
                    Output.append(heading)
                    for matchedtext in re.findall(r'(?<={").*?(?<=},)', b):
                        dbid = re.findall(r'(?<=dbid":).*?(?=,")', matchedtext)

                        le = len(dbid)

                        recordeddate = re.findall(r'(?<=recorded":").*?(?=T)', matchedtext)
                        recordedtime = re.findall(r'(?<=T).*?(?=",")', matchedtext)
                        ct= re.findall(r'(?<="ct":).*?(?=,")', matchedtext)
                        link_plan= re.findall(r'(?<="link_plan":).*?(?=,")', matchedtext)
                        married= re.findall(r'(?<="married":").*?(?=",")', matchedtext)
                        ss= re.findall(r'(?<="ss":).*?(?=,")', matchedtext)
                        tsc= re.findall(r'(?<="tsc":).*?(?=,")', matchedtext)
                        lane= re.findall(r'(?<="lane":").*?(?=",")', matchedtext)
                        
                        if lane == []:
                            lane= re.findall(r'(?<="lane":").*?(?="})', matchedtext)
                        ds1= re.search('"ds1":(\d+)', matchedtext)
                        if ds1:
                            ds1 = [str(ds1.group(1))]
                        mf1= re.search('"mf1":(\d+)', matchedtext)
                        if mf1:
                            mf1 = [str(mf1.group(1))]
                        rf1= re.search('"rf1":(\d+)', matchedtext)
                        if rf1:
                            rf1 = [str(rf1.group(1))]
                        if rf1 == None:
                            rf1 = ['']
                        if mf1 == None:
                            mf1 = ['']
                        if ds1 == None:
                            ds1 = ['']

                        ds2= re.search('"ds2":(\d+)', matchedtext)
                        if ds2:
                            ds2 = [str(ds2.group(1))]
                        mf2= re.search('"mf2":(\d+)', matchedtext)
                        if mf2:
                            mf2 = [str(mf2.group(1))]
                        rf2= re.search('"rf2":(\d+)', matchedtext)
                        if rf2:
                            rf2 = [str(rf2.group(1))]
                        if rf2 == None:
                            rf2 = ['']
                        if mf2 == None:
                            mf2 = ['']
                        if ds2 == None:
                            ds2 = ['']

                        ds3= re.search('"ds3":(\d+)', matchedtext)
                        if ds3:
                            ds3 = [str(ds3.group(1))]
                        mf3= re.search('"mf3":(\d+)', matchedtext)
                        if mf3:
                            mf3 = [str(mf3.group(1))]
                        rf3= re.search('"rf3":(\d+)', matchedtext)
                        if rf3:
                            rf3 = [str(rf3.group(1))]
                        if rf3 == None:
                            rf3 = ['']
                        if mf3 == None:
                            mf3 = ['']
                        if ds3 == None:
                            ds3 = ['']

                        ds4= re.search('"ds4":(\d+)', matchedtext)
                        if ds4:
                            ds4 = [str(ds4.group(1))]
                        mf4= re.search('"mf4":(\d+)', matchedtext)
                        if mf4:
                            mf4 = [str(mf4.group(1))]
                        rf4= re.search('"rf4":(\d+)', matchedtext)
                        if rf4:
                            rf4 = [str(rf4.group(1))]

                        if rf4 == None:
                            rf4 = ['']
                        if mf4 == None:
                            mf4 = ['']
                        if ds4 == None:
                            ds4 = ['']
                            
                        ds5= re.search('"ds5":(\d+)', matchedtext)
                        if ds5:
                            ds5 = [str(ds5.group(1))]
                        mf5= re.search('"mf5":(\d+)', matchedtext)
                        if mf5:
                            mf5 = [str(mf5.group(1))]
                        rf5= re.search('"rf5":(\d+)', matchedtext)
                        if rf5:
                            rf5 = [str(rf5.group(1))]
                        if rf5 == None:
                            rf5 = ['']
                        if mf5 == None:
                            mf5 = ['']
                        if ds5 == None:
                            ds5 = ['']
                        index= 0
                        input2 = [dbid[index], recordeddate[index], recordedtime[index], ct[index], link_plan[index], married[index], ss[index], tsc[index], lane[index], ds1[index], mf1[index], rf1[index], ds2[index], mf2[index], rf2[index], ds3[index], mf3[index], rf3[index], ds4[index], mf4[index], rf4[index], ds5[index], mf5[index], rf5[index]]
                        Output.append(input2)


                    if Output!= previousoutput:
                        print('new feed', pt - time.time())
                        t23 = float(time.time())
                        datee = datetime.datetime.strptime(str(Brisbane(t23)),"%d-%m-%Y %H:%M:%S" )
                        Hour = datee.hour
                        Minute = datee.minute
                        Sec = datee.second

                        a = "Intersection Volume (BCC)"
                        createCSVfile(Output, TUdirectory2 + "/"  +a+ " "+ str(Hour)+" Hr " +str(Minute)+" min " +str(Sec)+' sec '+'.csv')
                        previousoutput = Output
                        pt = time.time()
                        s.keep_alive = False

                    if Output == previousoutput:
                        print('old feed')
                        time.sleep(5) 
                except:
                    continue
    except:
        continue
