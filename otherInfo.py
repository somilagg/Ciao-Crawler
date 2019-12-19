class otherInfo:    
    def __init__(self,language):
        self.langIndex = 0
        self.lang = ["UK",
                "Spain",
                "Germany",
                "France",
                "Italy",
                "Netherlands",
                "Sweden"]
        
        #set langIndex
        for l in range(0,7):
            if self.lang[l] == language:
                self.langIndex = l
                break
        self.visitedList = open("visitedList_" + self.lang[self.langIndex] + ".txt","r+")
        
        
    def stat_crawler(self,user):
        bigList = {}
       
        #info = open(str(user.getIDNum()) + "_stats.txt","w+")
        thisurl = "http://" + self.p1Lang[self.langIndex] + "/member_view.php/MemberId/" + str(user.getIDNum()) + "/TabId/3/"
        response = self.acc.opener.open(thisurl)
        html = response.read()
       
        #reviews written
        reviews_written = re.search('(?<=Reviews written</a></td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+',html)
   
        #exceptional
        pattern = '(?<="exceptional" Ratings given</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        exceptionalRatings = re.search(pattern.decode("UTF-8"),html)
       
        #very helpful
        pattern = '(?<="very helpful" Ratings given</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        veryHelpfulRatings = re.search(pattern.decode("UTF-8"),html)
       
        #helpful
        pattern = '(?<="helpful" Ratings given</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        helpfulRatings = re.search(pattern.decode("UTF-8"),html)
       
        #somewhat helpful
        pattern = '(?<="somewhat helpful" Ratings given</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        somewhatHelpfulRatings = re.search(pattern.decode("UTF-8"),html)
       
        #not helpful
        pattern = '(?<="not helpful" Ratings given</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        notHelpfulRatings = re.search(pattern.decode("UTF-8"),html)
       
        #off topic
        pattern = '(?<="off topic" Ratings given</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        offTopicRatings = re.search(pattern.decode("UTF-8"),html)
       
        #exceptional
        pattern = '(?<="exceptional" Ratings received</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        exceptionalRatings2 = re.search(pattern.decode("UTF-8"),html)
       
        #very helpful
        pattern = '(?<="very helpful" Ratings received</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        veryHelpfulRatings2 = re.search(pattern.decode("UTF-8"),html)
       
        #helpful
        pattern = '(?<="helpful" Ratings received</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        helpfulRatings2 = re.search(pattern.decode("UTF-8"),html)
        
        #somewhat helpful
        pattern = '(?<="somewhat helpful" Ratings received</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        somewhatHelpfulRatings2 = re.search(pattern.decode("UTF-8"),html)
   
        #not helpful
        pattern = '(?<="not helpful" Ratings received</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        notHelpfulRatings2 = re.search(pattern.decode("UTF-8"),html)
       
        #off topic
        pattern = '(?<="off topic" Ratings received</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">)\w+'
        offTopicRatings2 = re.search(pattern.decode("UTF-8"),html)
       
        #questions
        pattern = '(?<=Questions posted</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">).*?(?=</span>)'
        questions = re.search(pattern,html)
       
        #answers
        pattern = '(?<=Answers posted</td>\n<td class="maintabCOLxs4 bgwhite"><span class="grey">).*?(?=</span>)'
        answers = re.search(pattern,html)
       
        #make bigList
        bigList.update({'reviews written' : reviews_written.group(0)})
        bigList.update({'exceptional given' : exceptionalRatings.group(0)})
        bigList.update({'very helpful given' : veryHelpfulRatings.group(0)})
        bigList.update({'helpful given' : helpfulRatings.group(0)})
        bigList.update({'somewhat helpful given' : somewhatHelpfulRatings.group(0)})
        bigList.update({'not helpful given' : notHelpfulRatings.group(0)})
        bigList.update({'off topic given' : offTopicRatings.group(0)})
        bigList.update({'exceptional received' : exceptionalRatings2.group(0)})
        bigList.update({'very helpful received' : veryHelpfulRatings2.group(0)})
        bigList.update({'helpful received' : helpfulRatings2.group(0)})
        bigList.update({'somewhat helpful received' : somewhatHelpfulRatings2.group(0)})
        bigList.update({'not helpful received' : notHelpfulRatings2.group(0)})
        bigList.update({'off topic received' : offTopicRatings2.group(0)})
        bigList.update({'questions' : questions.group(0)})
        bigList.update({'answers' : answers.group(0)})
       
        #ending
        outputFile = open(user.getIDNum() + '_stats.json','w')
        json.dump(bigList,outputFile)
        outputFile.close()   
        print "DONE WITH STATISTICS"
       
        #return statement
        return int(reviews_written.group(0))
    #---------------->   
    #takes in a list of reviews for a user and crawls all the information from that review
    #info - list of urls that lead to all the reviews
    #---------------->
    def review_crawler(self,info):
       
        #variables
        biggerList = []
       
        #15 reviews per page
        for review in info:
           
            #website for every review
            response = urllib2.urlopen(review)
            html = response.read()
           
            #review number
            trueValue = 0
            for i in range(0,7):
                i = 7-i
                try:
                    int(review[len(review)-i:])
                    break
                except ValueError:
                    pass
            trueValue = i
            idName = review[len(review)-trueValue:]
           
            #product name
            pattern = '(?<=alt=").*?(?=" data-large-image)'
            prodName = re.search(pattern,html)
           
            #overall review of product
            pattern = '(?<=<span class="text">).*?(?=</span>)'
            overallReview = re.search(pattern,html)
           
            #four categories of the review and their star ratings
            pattern = '(?<=<dt>).*?(?=</dt>)'
            categories = re.findall(pattern,html)
            pattern = '(?<=<dd class="ratingValue).*?(?="></dd>)'
            stars = re.findall(pattern,html)
           
            #pros
            pattern = '(?<=Pro</span>\n[ ]{12}<strong>).*?(?=</strong>)'
            pros = re.search(pattern,html)
           
            #cons
            pattern = '(?<=Cons</span>\n[ ]{12}<strong>).*?(?=</strong>)'
            cons = re.search(pattern,html)
           
            #title of review
            pattern = '(?<=<h3>&quot;).*?(?=&quot)'
            title = re.search(pattern,html)
           
            #content of review - MUST REMOVE TAGS
            pattern = '(?<=<span class="text">).*?(?=(?s)</span>)'
            content = re.findall(pattern,html)
            newContent = content[len(content)-1]
           
            #overall rating review
            pattern = '(?<="ratingStampText">).*?(?=</div>)'
            rating = re.search(pattern,html)
           
            #community evaluation: number of times read + overall percentage
            pattern = '(?<=This review was read ).*?(?= times and was)'
            numRead = re.search(pattern,html)
            pattern = '(?<=div>\n[ ]{16}).*?(?= :)'
            reviewRating = re.search(pattern,html)
           
            #comments: name of users + timestamps
            pattern = '(?<="commentItem">\n[ ]{4}<a href="/Member__).*?(?=")'
            commentNames = re.findall(pattern,html)
            pattern = '(?<="published">published ).*?(?=</span>)'
            timestamps = re.findall(pattern,html)
           
            #make bigList
            bigList = {}
            categories2 = []
            comments = []
            bigList.update({'id' : idName})
            bigList.update({'product name' : prodName.group(0)})
            bigList.update({'overall review' : overallReview.group(0)})
            for cat in range(0,len(categories)):
                category = {'name' : categories[cat],'stars' : str(int(stars[cat])/20)}
                categories2.append(category)
            bigList.update({'categories' : categories2})
            bigList.update({'pros' : pros.group(0)})
            bigList.update({'cons' : cons.group(0)})
            bigList.update({'title' : title.group(0)})
            try:
                bigList.update({'content' : newContent})
            except AttributeError:
                bigList.update({'content' : "None"})
            bigList.update({'rating' : rating.group(0)})
            bigList.update({'times read' : numRead.group(0)})
            bigList.update({'review rating' : reviewRating.group(0)})
            biggerList.append(bigList)
           
            #counter
            self.counter += 1
   
        #return statement
        return biggerList          
    #---------------->
    #collects the urls for all the reviews, gets the information using review_crawler, and outputs it as a json file
    #user - account in question, used to get id number
    #numWritten - gives a limit, used to determine when the loop will stop iterating
    #---------------->
    def review_info(self,user,numWritten):
       
        #variables
        biggerList = []
        pos = 0
       
        #starting html
        thisurl = "http://" + self.p1Lang[self.langIndex] + "/member_view.php/MemberId/" + str(user.getIDNum()) + "/TabId/1/Start/" + str(pos)
        response = self.acc.opener.open(thisurl)
        html = response.read()
        while re.match('(?<=class="diamond"></div><a href=").*?(?="  class="review">)',html) != "None":
           
            #get the page html
            thisurl = "http://" + self.p1Lang[self.langIndex] + "/member_view.php/MemberId/" + str(user.getIDNum()) + "/TabId/1/Start/" + str(pos)
            response = self.acc.opener.open(thisurl)
            html = response.read()
           
            #put all the reviews into one list from one page
            reviews = re.findall('(?<=class="diamond"></div><a href=").*?(?="  class="review">)',html)
            biggerList.append(self.review_crawler(reviews))
           
            #move on to the next page
            if pos > numWritten:
                break
            pos += 15
       
        #ending
        outputFile = open(user.getIDNum() + '_reviews.json','w')
        json.dump(biggerList,outputFile)
        outputFile.close()
        print "DONE WITH REVIEWS: " + str(numWritten)
#-------------------