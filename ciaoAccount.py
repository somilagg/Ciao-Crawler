# -*- coding: utf-8 -*-

import cookielib
import urllib
import urllib2
import ssl
import socket
 
class ciaoAccount(object):
 
    def __init__(self, login, password,language):
        """ Start up... """
        self.login = login
        self.password = password
        self.context = ssl._create_unverified_context()
 
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0, context=self.context),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'))
        ]
 
        # need this twice - once to set cookies, once to log in...
        self.loginToCiao(language)
        self.loginToCiao(language)
    #---------------->
    #logs in to ciao account
    #language - language that the website is in to change the url
    #---------------->
    def loginToCiao(self,language):
       
        #Handle login. This should populate our cookie jar.
        login_data = urllib.urlencode({
            'login_name' : self.login,
            'login_password' : self.password,
        })
        try:
            response = self.opener.open("https://" + language + "/login.php", login_data)
            return ''.join(response.readlines())
        except socket.error as error:
            # if error.errno == errno.WSAECONNRESET:
            print socket.error
            sleep(300)
            self.loginToCiao(language)



class ID:
    
    def __init__(self,num,hop):
        self.idNum = num
        self.hopNum = hop
    #---------------->
    #get hop number
    #---------------->
    def getHopNum(self):
        return self.hopNum
    #---------------->
    #get ID number
    #---------------->
    def getIDNum(self):
        return self.idNum
    #---------------->
    #set ID number
    #---------------->
    def setIDNum(self,num):
        idNum = self.num
    #---------------->
    #set hop number
    #---------------->
    def setHopNum(self,hop):
        hopNum = self.hop
        
#UK          = 6961916
#Spain       = 1463102
#Germany     = 7196815
#France      = 499750  // [Errno 10054] An existing connection was forcibly closed by the remote host
#Italy       = 779161 
#Netherlands = 5237623 // [Errno 10054] An existing connection was forcibly closed by the remote host
#Sweden      = 5273483 // [Errno 10054] An existing connection was forcibly closed by the remote host
 
import socket
import errno
import httplib
import bs4 as bs
import urllib2
import json
import re
import cookielib
from time import sleep
from collections import deque
 
class ciao_crawler:
   
    def __init__(self,language):
       
        #variables
        self.counter = 0
        self.id = 0
        self.visited = {}
        self.queue = {}
        self.langIndex = 0
       
        #languages
        self.lang = ["UK",
                "Spain",
                "Germany",
                "France",
                "Italy",
                "Netherlands",
                "Sweden"]
       
        #url beginnings
        self.p1Lang = ["www.ciao.co.uk",
                  "www.ciao.es",
                  "www.ciao.de",
                  "www.ciao.fr",
                  "www.ciao.it",
                  "www.ciao-shopping.nl",
                  "www.ciao.se"]
       
        #member
        self.p2Lang = ["Member__",
                  "Usuario__",
                  "Mitglied__",
                  "Membre__",
                  "Iscritti__",
                  "Lid__",
                  "Medlem__"]
       
        #member profile
        self.p3Lang = ["Member profile ",
                  "Perf&iacute;l de ",
                  "Mitgliedsprofil ",
                  "Profil du membre ",
                  "Profilo dell&acute;iscritto ",
                  "Ledenprofiel ",
                  "Medlemsprofil "]
       
        #members who trust pt 1
        self.p4Lang = ["Members who trust ",
                  "Miembros que conf&iacute;an en ",
                  "Mitglieder, die ",
                  "Lecteurs satisfaits ",
                  "Autori che si fidano di ",
                  "Leden die ",
                  "Medlemmar som litar på "]
       
        #members who trust pt 2
        self.p5Lang = ["",
                  "",
                  " vertrauen",
                  "",
                  "",
                  " vertrouwen",
                  ""]
       
        #members __ trusts pt 1
        self.p6Lang = ["Members ",
                  "Miembros en quien conf&iacute;a ",
                  "Mitglieder, denen ",
                  "R&eacute;dacteurs favoris",
                  "Iscritti  fiduciati",
                  "Leden die ",
                  "Medlemmar "]
       
        #members __ trusts pt 2
        self.p7Lang = [" trusts",
                  "",
                  " vertraut",
                  "",
                  "",
                  " vertrouwt",
                  " litar på"]
       
        #account usernames
        self.usernameLang = ["somilA",
                  "etien123",
                  "testestGermany",
                  "testtestFrance",
                  "testtestItaly",
                  "testtestNetherlands",
                  "testtestSweden"]
       
        #account passwords
        self.passwordLang = ["sureshkumar",
                  "User123haha",
                  "2017T3st!5",
                  "2017T3st!3",
                  "2017T3st!6",
                  "2017T3st!7",
                  "2017T3st!1"]
       
        #set langIndex
        for l in range(0,7):
            if self.lang[l] == language:
                self.langIndex = l
                break
       
        #create the account
        self.acc = ciaoAccount(self.usernameLang[self.langIndex],self.passwordLang[self.langIndex],self.p1Lang[self.langIndex])
    #---------------->
    #gets the IDs of all the people the user trusts and puts the #s into a list
    #limit - number of people the user is trusted by, used to determine when the loop will stop iterating
    #vertex - the user getting information from
    #---------------->
    def getIDs(self,limit,vertex):
       
        #variables
        pos = 0
        origList = []
        idList = []
            
        #starting point created   
        thisurl = "http://" + self.p1Lang[self.langIndex]+ "/member_view.php/MemberId/" + str(vertex.getIDNum()) + "/TabId/5/subTabId/1/Start/" + str(pos)
        response = self.acc.opener.open(thisurl)
        html = response.read()
       
        #puts data into original list
        while re.match('(?<=alt="" /><a href="http://'
                            + self.p1Lang[self.langIndex]
                            + '/'
                            + self.p2Lang[self.langIndex]
                            + ').*?(?=" >)',html) != "None":
            thisurl = "http://" + self.p1Lang[self.langIndex] + "/member_view.php/MemberId/" + str(vertex.getIDNum()) + "/TabId/5/subTabId/1/Start/" + str(pos)
            response = self.acc.opener.open(thisurl)
           
            #find all users and put them into list
            html = response.read()
            ciaoId = re.findall('(?<=alt="" /><a href="http://'
                            + self.p1Lang[self.langIndex]
                            + '/'
                            + self.p2Lang[self.langIndex]
                            + ').*?(?=" >)',html)
            for string in ciaoId:
                origList.append(string)
            if pos > limit:
                break
            pos += 15
       
        #parses ID #s from the data
        trueValue = 0
        for x in origList:
            for i in range(0,7):
                i = 7-i
                try:
                    int(x[len(x)-i:])
                    break
                except ValueError:
                    pass
            trueValue = i
            new = ID(x[len(x)-trueValue:],vertex.getHopNum()+1)
            idList.append(new)
            
        #return statement
        return idList
    #---------------->
    #takes starting user and goes through structural analysis creation and NLP data collection
    #start - starting account id
    #hopLimit - tells us which hop to not go past
    #---------------->
    def bfs(self,start,hopLimit):
       
        #variables
        firstUser = ID(start,0)
        self.queue = [firstUser]
        self.visited = []
        idList = []
        edgeList = open("edgeList_" + self.lang[self.langIndex] + ".txt","w+")
        visitedList = open("visitedList_"+ self.lang[self.langIndex] + ".txt","w+")
        totalTrusts = 0
        deadAccounts = 0
       
        #while loop for hops
        while self.queue:
            self.queue = deque(self.queue)
            #move along the queue
            vertex = self.queue.popleft()
            if(vertex.getHopNum() >= hopLimit):
                break
            try:
                #vertex should not have been visited
                if vertex not in self.visited:
 
                    #get sizes of lists
                    thisurl = "http://" + self.p1Lang[self.langIndex] + "/member_view.php/MemberId/" + str(vertex.getIDNum()) + "/TabId/3/"
                    response = self.acc.opener.open(thisurl)
                    html = response.read()
                    name = re.search('(?<=<span class="greyb">'
                                        + self.p3Lang[self.langIndex]
                                        + ').*?(?=</span></div>)',html)
 
                    #try statement for accounts that don't exist
                    try: 
                        name2 = name.group(0)
                        if self.lang[self.langIndex] == "France" or self.lang[self.langIndex] == "Italy":
                            name2 = ""
                        pattern = '(?<=' + self.p6Lang[self.langIndex] + name2 + self.p7Lang[self.langIndex] + '</a></td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
                        num_trusts = re.search(pattern.decode('UTF-8'),html)
 
                        #if connections further equals 0
                        if num_trusts.group(0) == 0:
                            pass
                        else:
                            #add to total for average user calcuation
                            totalTrusts += int(num_trusts.group(0))
 
                            #getID Lists
                            idList = self.getIDs(int(num_trusts.group(0)),vertex)
                            for x in idList:
                                edgeList.write(str(vertex.getIDNum()) + "," + str(x.getIDNum()) + "\n")
 
                            #checks for repeats in queue
                            for queue in self.queue:
                                for num in idList:
                                    if queue == num:
                                        idList.remove(num)
 
                            #checks for repeats in visited
                            for visited in self.visited:
                                for num in idList:
                                    if visited == num:
                                        idList.remove(num)
 
                            #adds new IDs into queue
                            for x in idList:
                                self.queue.append(x)
                    except AttributeError:
                        print 'attribute error'
                        pass
 
                    #sleep statement
                    sleep(1)
 
                    #add account into visited
                    visitedList.write(str(vertex.getIDNum()) + "\n")
                    self.visited.append(vertex)
 
                    #print statements
                    print "Length of self visited: " + str(len(self.visited))
                    print "--------------------------------------------------"
                   
            except socket.error as error:
                # if error.errno == errno.WSAECONNRESET:
				print socket.error
				sleep(300)
				self.acc = ciaoAccount(self.usernameLang[self.langIndex],self.passwordLang[self.langIndex],self.p1Lang[self.langIndex])
				self.queue.appendleft(vertex)
				continue
                #else:
                #    raise
					
            except httplib.BadStatusLine:
                print "Http BadStatus Line"
                continue

            except urllib2.HTTPError:
                print "HTTP Error"
                print urllib2.HTTPError
                continue

            except urllib2.URLError:
                print "URL Error"
                print urllib2.URLError
                sleep(300)
                self.acc = ciaoAccount(self.usernameLang[self.langIndex],self.passwordLang[self.langIndex],self.p1Lang[self.langIndex])
                self.queue.appendleft(vertex)
                continue

        #ending
        edgeList.write("Average user trust: " + str(totalTrusts/len(self.visited)))
        print "Average user trust: " + str(totalTrusts/len(self.visited))
        print "DONE"
        edgeList.close()
        visitedList.close()
    #---------------->
    #crawls information off the statistics page and puts it into a json file
    #user - user from which the statistics are collected
    #---------------->
new = ciao_crawler("UK")
new.bfs(str(6961916),3);