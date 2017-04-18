import datetime
import random as random
from yuh import *

#generate sample data to pick from
initial_data = list(data)
#print data[:5]
test_data1 = get_data(0,30)
#rint data[:5]

test_data2 = get_data(1,0)

#test_data3 = get_data(3,0) #add 'url' paramater to get_data function

#select which data set to use below


def is_action_needed(data, person):
    last_time = data[-1][0]

    rates1 = []
    rates2 = []

    deltavotes1 = []
    deltavotes2 = []

    deltatime = []
    for i in range(len(data) - 1):
        deltavotes1.append(data[i + 1][1] - data[i][1])
        deltavotes2.append(data[i + 1][2] - data[i][2])
        deltatime.append(data[i + 1][0] - data[i][0])

    for k in range(len(deltavotes1)):
        rates1.append(60 * (deltavotes1[k] / float(deltatime[k])))

    for k in range(len(deltavotes2)):
        secrate2 = deltavotes2[k] / float(deltatime[k])
        rates2.append(float(60) * secrate2)

    average_rate1 = sum(rates1) / float(len(rates1))
    average_rate2 = sum(rates2) / float(len(rates2))

    now = datetime.datetime.fromtimestamp(last_time)
    eleven = datetime.datetime(now.year, now.month, now.day, 23)
    min_left = int(abs(eleven - now).seconds / 60)

    vote1_estimate = data[-1][1] + min_left * float(average_rate1)
    vote2_estimate = data[-1][2] + min_left * float(average_rate2)

    final_diff = vote1_estimate - vote2_estimate
    final_dict = {'person': person}

    if min_left > random.randint(660,840):
        print ("It is too early to determine if action is needed. There are still %s minutes left in Lent Madness today" % (min_left))
        return False
    elif vote1_estimate > vote2_estimate and person == 2:
        add = int(final_diff * 2.25) + 2
        print ("We need %s votes in %s minutes" % (add, min_left))

        final_dict.update(votes=add, minutes=min_left)
        return final_dict
    elif vote1_estimate > vote2_estimate and person == 1:
        if final_diff > 2500:
            print ("No action is needed, person one is projected to win")
            return False
        elif final_diff < 2500:
            add = int(final_diff * 1.5) + 2
            print ("We need %s votes in %s minutes" % (add, min_left))

            final_dict.update(votes=add, minutes=min_left)
            return final_dict
    elif vote2_estimate > vote1_estimate and person == 1:
        add = int(abs(final_diff) * 2.25) + 2
        print ("We need %s votes in %s minutes" % (add, min_left))

        final_dict.update(votes=add, minutes=min_left)
        return final_dict
    elif vote2_estimate > vote1_estimate and person == 2:
        if abs(final_diff) > 2500:
            return False
        elif abs(final_diff) < 2500:
            add = int(abs(final_diff) * 1.5) + 2
            print ("We need %s votes in %s minutes" % (add, min_left))

            final_dict.update(votes=add, minutes=min_left)
            return final_dict



expected_response = {'person':1,'votes':70,'minutes':9}

def test_answer():
    assert is_action_needed(data,1) == expected_response

is_action_needed(test_data1,1)