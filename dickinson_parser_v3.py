import json

START_YEAR = 2014
MAX_SUCCESS_CHECKINS = 10

def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ").replace(";","")

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute,value))
    return L

def parseBusinessData():
    print("Parsing businesses...")
    #read the JSON file
    with open('.//yelp_business.JSON','r') as f:
        outfile =  open('.//yelp_business.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id'] #business id
            business_str =  "('" + cleanStr4SQL(data['business_id']) + "'," + \
                            "'" + cleanStr4SQL(data['name']) + "'," + \
                            "'" + cleanStr4SQL(data['address']) + "'," + \
                            "'" + cleanStr4SQL(data['city']) + "'," +  \
                            "'" + data['state'] + "'," + \
                            "'" + data['postal_code'] + "'," +  \
                            "0," + \
                            "0," + \
                            "0," + \
                            "0," + \
                            "0" 
            
            outfile.write(business_str + '),\n')
            line = f.readline()
            count_line +=1

    print(count_line)
    outfile.close()
    f.close()
                           

def parseCategories():
    print("Parsing categories...")
    #read the JSON file
    with open('.//yelp_business.JSON','r') as f:
        outfile =  open('.//yelp_categories.txt', 'w')
        line = f.readline()
        count_line = 0
        while line:
            data = json.loads(line)
            business = cleanStr4SQL(data['business_id'])

            for category in data['categories']:
                category_str = "('" + business + "','" + cleanStr4SQL(category) + "'),"
                outfile.write(category_str + '\n')

            line = f.readline()
            count_line +=1

    print(count_line)
    outfile.close()
    f.close()
        

def parseReviewData():
    print("Parsing reviews...")
    #reading the JSON file
    with open('.//yelp_review.JSON','r') as f:
        outfile =  open('.//yelp_review.txt', 'w')
        line = f.readline()
        count_line = 0
        failed_inserts = 0

        while line:
            data = json.loads(line)
            review_str = "('" + cleanStr4SQL(data['review_id']) + "'," +  \
                         "'" + cleanStr4SQL(data['business_id']) + "'," + \
                         str(data['stars']) + "," + \
                         cleanStr4SQL(data['date'])[0:4] + "," + \
                         "'" + cleanStr4SQL(data['text'])
            outfile.write(review_str +"'),\n")
            line = f.readline()
            count_line +=1

    print(count_line)
    outfile.close()
    f.close()

def parseUserData():
    print("Parsing users...")
    #reading the JSON file
    with open('.//yelp_user.JSON','r') as f:
        outfile =  open('.//yelp_user.txt', 'w')
        line = f.readline()
        count_line = 0
        while line:
            data = json.loads(line)
            user_id = data['user_id']
            user_str = \
                      "'" + user_id + "'," + \
                      "'" + cleanStr4SQL(data["name"]) + "'," + \
                      "'" + cleanStr4SQL(data["yelping_since"]) + "'," + \
                      str(data["review_count"]) + "," + \
                      str(data["fans"]) + "," + \
                      str(data["average_stars"]) + "," + \
                      str(data["funny"]) + "," + \
                      str(data["useful"]) + "," + \
                      str(data["cool"])
            outfile.write(user_str+"\n")

            for friend in data["friends"]:
                friend_str = "'" + user_id + "'" + "," + "'" + friend + "'" + "\n"
                outfile.write(friend_str)
            line = f.readline()
            count_line +=1

    print(count_line)
    outfile.close()
    f.close()

def parseCheckinData():
    print("Parsing checkins...")
    #reading the JSON file
    with open('.\yelp_checkin.JSON','r') as f:  # Assumes that the data files are available in the current directory. If not, you should set the path for the yelp data files.
        outfile = open('yelp_checkin.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        sum = 0
        while line:
            data = json.loads(line)
            business_id = data['business_id']
            for (dayofweek,time) in data['time'].items():
                for (hour,count) in time.items():
                    sum += count

            checkin_str = "UPDATE Business SET numCheckins = " + str(sum) + ",  bus_rating = bus_rating + " + str(min(sum,MAX_SUCCESS_CHECKINS)) + " WHERE bus_id = '" + business_id + "';"    
            outfile.write(checkin_str + "\n")
            sum = 0
            line = f.readline()
            count_line +=1
        print(count_line)
    outfile.close()
    f.close()

def parseReviewDataForUpdate():
    print("Parsing reviews for updating business table...")
    #reading the JSON file
    with open('.//yelp_review.JSON','r') as f:
        outfile =  open('.//yelp_reviewUpdate.txt', 'w')
        line = f.readline()
        count_line = 0
        lastBusinessId = ""
        averageRating = 0.0
        data = json.loads(line)
        sum = data['stars']
        count = 1
        lastBusinessId = data['business_id']
        while line:
            data = json.loads(line)
            if data['business_id'] == lastBusinessId:
                sum += data['stars']
                count += 1
            else:
                averageRating = round(10 * sum / count)
                averageRating /= 10.0
                update_str = "UPDATE Business SET reviewcount = reviewcount + " + str(count) + ", reviewrating = ((" + str(averageRating*count) + " + (reviewrating * reviewcount)) / (reviewcount + " + str(count) + ")) WHERE bus_id = '" + cleanStr4SQL(data['business_id']) + "';" 
                outfile.write(update_str + '\n')
                lastBusinessId = data['business_id']
                sum = data['stars']
                count = 1
            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()

def updatePopularityAndSuccess():
    print("Parsing review data to update business popularity and success...")
    with open('yelp_review.JSON','r') as f:
        outfile = open('yelp_update.txt','w')
        line = f.readline()
        count_line = 0
        popularity = 0
        success = 0
        data = json.loads(line)
        stars = data['stars']
        yearSum = [0] * 17
        year = 0
        multiplier = 0
        lastBusinessID = data['business_id']
        update_str = ""
        while line:
            if data['date'][0:4] == "2017":
                multiplier = 3
            elif data['date'][0:4] == "2016":
                multiplier = 2
            elif data['date'][0:4] == "2015":
                multiplier = 1
            else:
                multiplier = 0

            popularity += multiplier * ((int(stars / 3) * 2) + stars - 4) # Popularity formula per year as outlined in Popularity Metrics

            year = START_YEAR - int(data['date'][0:4])
            yearSum[year] += ((int(stars / 3) * 2) + stars - 4)
            data = json.loads(line)
            if data['business_id'] != lastBusinessID:
                for i in range(0,len(yearSum)):
                    if yearSum[i] > 10:
                        yearSum[i] = 10
                    success += yearSum[i]
                    yearSum[i] = 0
                update_str = "UPDATE Business SET bus_rating = bus_rating + " + str(success) + ", popularity = popularity + " + str(popularity) + " WHERE bus_id = '" + lastBusinessID + "';"
                outfile.write(update_str + '\n')

                success = 0
                popularity = 0
                count_line += 1

            lastBusinessID = data['business_id']
            line = f.readline()
            if line:
                data = json.loads(line)
                
    print(count_line)
    outfile.close()
    f.close()

        
parseBusinessData()
# parseUserData()
# parseCheckinData()
# parseReviewDataForUpdate()
# parseReviewData()
# parseCategories()
# updatePopularityAndSuccess()
