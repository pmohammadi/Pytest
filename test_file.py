import requests
import datetime
import time
from bs4 import BeautifulSoup

page = requests.get("http://mfl.williammck.net/poll/58dba3c799f502489e494900")

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
        candidates = list(filter(None, candidates))
        can1 = SeparateNamesFromVotes(candidates[0])
        can2 = SeparateNamesFromVotes(candidates[1])
        data.append([timestamp, can1[1], can2[1]])

vote_counts_lst = []
list_of_times = []
for ject in data:
    current_time = data[0]
    list_of_times.append(current_time)
    vote_counts_lst.append([data[1], data[2]])

data.sort()
vote_counts_lst.sort()
list_of_times.sort()

for i, value in enumerate(data):
    t1 = datetime.datetime.strptime(value[0], '%Y-%m-%d %H:%M:%S')
    data[i][0] = t1

def get_data(hours, minutes):
    first_time = data[0][0]
    end_time = first_time + datetime.timedelta(hours=hours, minutes=minutes)
    test_data = []
    for i in data:
        if i[0] < end_time:
            test_data.append(i)
        else:
            pass
    for i in test_data:
        dt = i[0]
        i[0] = time.mktime(dt.timetuple())
        str_i1 = i[1].encode('ascii')
        str_i2 = i[2].encode('ascii')
        i[1] = int(str_i1)
        i[2] = int(str_i2)
    print(test_data)

get_data(7, 34)

def IsActionNeeded(data1, person):
    last_time = data1[-1][0]
    modulo = (last_time % 86400) / float(86400)
    if modulo < .5:
        print ("No action is needed yet")
        return False
    p1_votes = data1[-1][1]
    p2_votes = data1[-1][2]
    FinalVoteCount = p1_votes + p2_votes
    percent_1 = p1_votes/FinalVoteCount
    percent_2 = p2_votes/FinalVoteCount
    if p1_votes > p2_votes and person == 1:
        winning_margin = p1_votes - p2_votes
        percent_margin = 100 * winning_margin / FinalVoteCount
        print ("good guy is winning by %s votes or %s percent" % (winning_margin, percent_margin))
    elif p1_votes > p2_votes and person == 2:
        winning_margin = p1_votes - p2_votes
        percent_margin = 100 * winning_margin / FinalVoteCount
        print ("good guy is losing by %s votes or %s percent" % (winning_margin, percent_margin))
    elif p1_votes < p2_votes and person == 1:
        winning_margin = p2_votes - p1_votes
        percent_margin = 100 * winning_margin / FinalVoteCount
        print ("good guy is losing by %s votes or %s percent" % (winning_margin, percent_margin))
    elif p1_votes < p2_votes and person == 2:
        winning_margin = p2_votes - p1_votes
        percent_margin = 100 * winning_margin / FinalVoteCount
        print ("good guy is winning by %s votes or %s percent" % (winning_margin, percent_margin))
    else:
        print ("the two saints are currently tied")

    rates1 = []
    rates2 = []
    deltavotes1 = []
    deltavotes2 = []
    deltatime = []
    for i in range(len(data1)-1):
        deltavotes1.append(data1[i+1][1] - data1[i][1])
        deltavotes2.append(data1[i+1][2] - data1[i][2])
        deltatime.append(data1[i+1][0] - data1[i][0])
    for k in range(len(deltavotes1)):
        rates1.append(60*(deltavotes1[k]/float(deltatime[k])))
    for k in range(len(deltavotes2)):
        secrate2 = deltavotes2[k]/float(deltatime[k])
        rates2.append(float(60)*secrate2)
    average_rate1 = sum(rates1)/float(len(rates1))
    average_rate2 = sum(rates2)/float(len(rates2))
    print (rates1)
    print (rates2)
    print ("average rate for person 1:", average_rate1)
    print ("average rate for person 2:", average_rate2)
    list_of_elevens = []
    first_eleven = 1489118400 #march 9, 11pm
    timediff = last_time - first_eleven #the difference between the current time and march 9, 11pm
    print ("timediff", timediff)
    timer = 1 + (timediff / 86400) #provides day of competition as an integer with the first date being 0; provides days since march 9,11?
    #round "timer" to the next highest number, then use as index in list of "elevens"
    print ("number of days since march 9, 11pm", timer)
    day_eleven = timer*86400 + first_eleven #lets test this but I think it will give us a unix timestamp back of the time at eleven at each day;
    print ("unix time stamp for above date:", day_eleven)
    min_left = int((day_eleven - last_time)/float(60))
    print (min_left)
    vote1_estimate = min_left * float(average_rate1)
    vote2_estimate = min_left * float(average_rate2)
    print (vote1_estimate)
    print (vote2_estimate)
    final_diff = vote1_estimate - vote2_estimate
    final_dict = {'person': person}
    if min_left > 720:
        print ("It is too early to determine if action is needed. There are still %s minutes left in Lent Madness today" % (min_left))
        return final_dict
    elif vote1_estimate > vote2_estimate and person == 2:
        print ("take action")
        add = int(final_diff * 2.25) + 2
        print ("We need %s votes in %s minutes" % (add, min_left))
        final_dict.update(votes = add, minutes = min_left)
        return final_dict
    elif vote1_estimate > vote2_estimate and person == 1:
        if final_diff > 2500:
            print ("No action is needed, person one is projected to win")
            return False
        elif final_diff < 2500:
            print ("Some action is needed")
            add = int(final_diff * 1.5) + 2
            print ("We need %s votes in %s minutes" % (add, min_left))
            final_dict.update(votes = add, minutes = min_left)
            print (final_dict)
            return final_dict
    elif vote2_estimate > vote1_estimate and person == 1:
        print ("take action")
        add = int(abs(final_diff) * 2.25) + 2
        print ("We need %s votes in %s minutes" % (add, min_left))
        final_dict.update(votes = add, minutes = min_left)
        return final_dict
    elif vote2_estimate > vote1_estimate and person == 2:
        if abs(final_diff) > 2500:
            print ("No action needed, person 2 is projected to win")
            return False
        elif abs(final_diff) < 2500:
            print ("Some action is needed")
            add = int(abs(final_diff) * 1.5) + 2
            print ("We need %s votes in %s minutes" % (add, min_left))
            final_dict.update(votes = add, minutes = min_left)
            print (final_dict)
            return final_dict
IsActionNeeded(data, 2)