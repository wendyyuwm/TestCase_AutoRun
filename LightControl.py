__author__ = '310208599'

#!/usr/bin/python
import configparser
#import requests
import time,os
import json

AutoTest = 1
Log_File = None

def write_log(str):
    if AutoTest == 1:
        Log_File.write(str)

def process_testcase(root, file, groupno, lightslist):
    testcasename = os.path.join(root, file)
    cf = configparser.ConfigParser()
    cf.read(testcasename)
    sections = cf.sections()  #read all the sections on config files, on this configfile, it means the step
    for section in sections:
        print('section:', section)
        seconds = 5
        lightscontrol = False
        appendurl = cf.get(section, "url")  # get the url from the config file
        method = cf.get(section, "method")  # get the method from the config file
        body = cf.get(section, "body")  # get the body from the config file
        base_url = 'http://' + bridgeIp + username
        if "time" in cf.options(section):
            seconds = int(cf.get(section,"time"))
        #print(body)
        if body.find('lights') != -1:
            last = body.index('[')
            nbody = body[0:last]+str(json.dumps(lightslist))+'}'
            body = nbody

        if appendurl.startswith("/groups"):
            appendurl = "/groups/"+groupno+"/actions"

        if '/lights' and '/state' in appendurl:
            lightscontrol = True
            l = len(lightslist)
            print("l is",l)
            for i in range(l):
                appendurl = "/lights/"+lightslist[i]+"/state"
                light_control(seconds,base_url, appendurl, method, body)
                # #url = 'http://' + bridgeIp + username + appendurl
                # seconds = 5
                # if "time" in cf.options(section):
                #     seconds = int(cf.get(section,"time"))
                # url = 'http://' + bridgeIp + username + appendurl
                # content = str(url+'\t'+method+'\t'+body+'\n')
                # print(content)
                # write_log(content)
                #
                # if method == 'put':
                #  #    requests.put(url, body)
                #     pass
                # time.sleep(seconds)



        if lightscontrol == False:
            light_control(seconds,base_url, appendurl, method, body)
            # if "time" in cf.options(section):
            #     seconds = int(cf.get(section,"time"))
            # else:
            #     seconds = 5
            # url = 'http://' + bridgeIp + username + appendurl
            # content = str(url+'\t'+method+'\t'+body+'\n')
            # print(content)
            # write_log(content)
            # if method == 'put':
            # #     requests.put(url, body)
            #     pass
            # time.sleep(seconds)


def light_control(seconds,base_url, appendurl, method, body):
    url = base_url + appendurl
    content = str(url+'\t'+method+'\t'+body+'\n')
    print(content)
    write_log(content)
                                                    
    if method == 'put':
    #    requests.put(url, body)
        pass
    time.sleep(seconds)
        



try:
    cfp = configparser.ConfigParser()
    cfp.read("Test.cfg")
    bridgeIp = cfp.get('Config', 'BridgeIp')
    username = cfp.get('Config', 'validuser')
    dir = cfp.get('Config','dir')
    AutoTest = int(cfp.get('Config', "autotest"))
    groupno = cfp.get('Config','groupNo')
    lightsno = cfp.get('Config','lightsNo')
    lightslist = lightsno.split(',')
    
   
    if AutoTest == 1:

        Log_File = open('test.log','w')
        for root, dirs, files in os.walk(dir):
            for file in files:
                Log_File.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\t'+file+'\n')
                print(file + '\n')
                process_testcase(root, file, groupno,lightslist)
                result = file + " test Finished \n"
                Log_File.write(result)
                print(result)
                time.sleep(20)

        print("All test Finished")
        input("Press any key to quit...")
        Log_File.close()

    else:
        for root, dirs, files in os.walk(dir):
            #print (files)
            for config in files:
                print(config, end='\t')
            print('\n')
            while True:
                file = input("Please input the testcase name: ")
                if file not in files:
                    print("\nCan't find this config file")
                    input("Press any key to continue.\n")
                else:
                    process_testcase(root, file, groupno)
                    print(file + " test Finished \n")
                    input("Press any key to continue.\n")
                


except KeyboardInterrupt:
    input("\nPress any key to quit...")

except Exception as e:
     print("\nError:",e)
     input("Press any key to quit...")

finally:
    Log_File.close()

