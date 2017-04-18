import requests
import datetime
import time
from bs4 import BeautifulSoup

page = requests.get("http://mfl.williammck.net/poll/58d3dad399f5024018fde2d8")

soup = BeautifulSoup(page.text, "html.parser")

table = soup.table

rows = table.find_all('tr')

data = []

def SeparateNamesFromVotes(inputString):
    components = inputString.split(':')
    assert len(components) == 2

    return [ components[0], components[1] ]


for row in rows:
    poll = row.find_all('td')
    if poll:
        timestamp = poll[0].text
        vote_counts = poll[1].text.replace(" ","").replace("\n"," ")
        candidates = vote_counts.split(" ")
        candidates = filter(None, candidates)
        data.append( [timestamp, SeparateNamesFromVotes(candidates[0])[1], SeparateNamesFromVotes(candidates[1])[1]] )


for i, value in enumerate(data):
    t1 = datetime.datetime.strptime(value[0], '%Y-%m-%d %H:%M:%S')
    data[i][0] = t1

data.sort()


def get_data(hours, minutes):
    print (type(data[0][0]))
    print (type(datetime.timedelta(hours=hours,minutes=minutes)))
    end_time = data[0][0] + datetime.timedelta(hours=hours,minutes=minutes)
    test_data = []
    for i in data:
        if i[0] < end_time:
            test_data.append(i)
        else:
            pass
    #convert times to unix timestamp
    print (data[-5:])
    for i in test_data:
        dt = i[0]
        i[0] = time.mktime(dt.timetuple())
        str_i1 = i[1].encode('ascii')
        str_i2 = i[2].encode('ascii')
        i[1] = int(str_i1)
        i[2] = int(str_i2)
    print (data[-5:])
    return test_data