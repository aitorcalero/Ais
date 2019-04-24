"""
An example code to run live queries on the SPIRE API.
"""

import requests
import json
import time
import datetime
import os

waittime = 900   # wait 15 min in between queries

# SPIRE AIS ENDPOINT
ENDPOINT = 'https://api.sense.spire.com/vessels'


# FORMAT
FORMAT = 'json'

# YOUR TOKEN Contact us to get this token.
AUTH_TOKEN = ""

HEADERS = {"Authorization": "Bearer {}".format(AUTH_TOKEN), 'Accept': 'application/%s' % FORMAT}


# Message Processing
def process_messages(messages, theValue):
    '''Function that will be used to process data fetched from the API'''
    if theValue is None:
        uniquename = '1'
    else:
        uniquename = str(theValue)

    outputdir = os.path.normpath(os.path.curdir + '/spire/')
    outputfile = outputdir + uniquename + '.json'
    f_out = open(outputfile, 'w')
    f_out.write(messages)
    f_out.close()


def query_data():

    print("Start Querying SPIRE Data...")
    now = datetime.datetime.now()
    newiso = datetime.datetime.isoformat(now)
    request = ENDPOINT + '/?updated_after=%s' % newiso

    since = None

    while True:
        print(request)
        response = requests.get(request, headers=HEADERS)
        data = response.json()
        datajson = json.loads(response.text)
        thetext = json.dumps(datajson, indent=2)   # makes nicely formatted JSON

        try:
            process_messages(thetext, since)
        except KeyError:
            print("No data to write.")
            continue  # dumps out of While True loop

        if 'paging' in data:
            try:
                since = data['paging']['next']
                if request.find("next=") != -1:
                    t = request.find("next=") + len("next=")
                    # strip out
                    request = request[:t] 
                    request = request + since
                else:
                    request = request + "&next=%s" % since

            except KeyError:
                print('The data transfer is over. Waiting %s seconds to requery the vessels. Press CTRL+C to quit.' % waittime)
                time.sleep(waittime)
                now = datetime.datetime.now()
                newiso = datetime.datetime.isoformat(now)
                request = ENDPOINT + '/?updated_after=%s' % newiso


if __name__ == '__main__':
    query_data()
