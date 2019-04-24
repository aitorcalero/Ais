"""
An example code to run live queries on the SPIRE API.
"""

import requests
import json
import time
import datetime
import os

# wait 15 min in between queries
waittime = 100

# SPIRE AIS ENDPOINT
ENDPOINT = 'https://api.sense.spire.com/vessels'


# FORMAT
FORMAT = 'json'

# YOUR TOKEN Contact us to get this token.
# AUTH_TOKEN = "7nGMLSHFS1BxqMg1oVQLS2QSISKi86Bd"

AUTH_TOKEN = "ozE4uCoStkebDoq1mLPoSQz8PoUxnw5n"

HEADERS = {"Authorization": "Bearer {}".format(AUTH_TOKEN), 'Accept': 'application/%s' % FORMAT}

# Message Processing
def process_messages(messages, theValue):
    '''Function that will be used to process data fetched from the API'''
    if theValue is None:
        uniquename = '1'
    else:
        uniquename = str(theValue)

    outputdir = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + '/spire/')
    outputfile = outputdir + uniquename + '.json'
    print(outputdir)
    print(outputfile)
    
    f_out = open(outputfile, 'w')
    f_out.write(messages)
    f_out.close()

    outputfileGEP = outputdir + uniquename + '.json'
    f_outGEP = open(outputfileGEP, 'w')
    f_outGEP.write(messages)
    f_outGEP.close()


def query_data():

    print('Start Querying SPIRE Data...')
    # change now to utcnow
    now = datetime.datetime.utcnow()
    newiso = datetime.datetime.isoformat(now)
    #newiso =  '2019-03-11T09:15:00.0'
    request = ENDPOINT + '/?updated_after=%s' % newiso

    since = None

    while True:
        print(request)
        response = requests.get(request, headers=HEADERS)
        data = response.json()
        datajson = json.loads(response.text)
        # makes nicely formatted JSON
        thetext = json.dumps(datajson, indent=2)

        try:
            process_messages(thetext, since)
        except KeyError:
            print ("No data to write.")
            continue  # dumps out of While True loop

        if 'paging' in data:
            try:
                since = data['paging']['next']
                if request.find("next=") != -1:
                    t = request.find("next=") + len("next=")
                    request = request[:t] #strip out
                    request = request + since
                else:
                    request = request + "&next=%s" % since

            except KeyError:
                print('The data transfer is over. Waiting %s seconds to requery the vessels. Press CTRL+C to quit.' % waittime)
                # exip app
                #exit(0)
                #time.sleep(waittime)
                now = datetime.datetime.utcnow()
                newiso = datetime.datetime.isoformat(now)
                request = ENDPOINT + '/?updated_after=%s' % newiso
                time.sleep(waittime)

if __name__ == '__main__':
    query_data()
