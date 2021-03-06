import json
import datetime
import time
import os

from ..svm import gen_alert_model, pred_alert
from ...database.database import connectDB, closeDB
from ...reporter import reportError, isError
 
def trim_time(data):
    result = []
    for res in data:
        curr = datetime.datetime.strptime(res['time'], '%Y-%m-%d %H:%M:%S.%f')
        currentYMD = time.mktime(datetime.datetime(curr.year, curr.month, curr.day).timetuple())
        currentUnix = time.mktime(curr.timetuple())

        result.append({
            "amps": res["amps"],
            "time": int(currentUnix - currentYMD)
        })

    return result


def loopSVM():
    if os.path.isfile('svmrun.json'):
        with open('svmrun.json', 'r') as json_file:
            data = json.load(json_file)

        last = datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
        time_between = datetime.datetime.now() - last

        # if time_between.days >= 7:
            # try:
            #     conn, cursor = connectDB()
            #     query = ''' SELECT channelID from channels '''
            #     cursor.execute(query)
            #     channels = cursor.fetchall()
            # except Exception as error:
            #     reportError('SQL Error: Unable to retrieve channel IDs', error)
            #     closeDB(conn, cursor)

            # for chID in channels:
            #     try:
            #         query = ''' SELECT time, amps FROM usages WHERE channelID = %s '''
            #         cursor.execute(query, chID)
            #         results = cursor.fetchall()
            #     except Exception as error:
            #         reportError('SQL Error: Unable to insert channel usage', error)
            #         closeDB(conn, cursor)
                
            #     closeDB(conn, cursor)
    with open('test.json', 'r') as json_file:
        results = json.load(json_file)
    data = trim_time(results)
    gen_alert_model('0', data)

    data = {}
    data['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('svmrun.json', 'w') as json_file:
        json.dump(data, json_file)
    

def main():
    try:
        loopSVM()
        curr = datetime.datetime.strptime("2019-04-14 01:24:06.000000", '%Y-%m-%d %H:%M:%S.%f')
        currentYMD = time.mktime(datetime.datetime(curr.year, curr.month, curr.day).timetuple())
        currentUnix = time.mktime(curr.timetuple())

        pred_alert('0', [[.72, currentUnix - currentYMD]])

    except Exception as error:
        reportError('An error occured starting the test script', error)


if __name__ == "__main__":
    main()

