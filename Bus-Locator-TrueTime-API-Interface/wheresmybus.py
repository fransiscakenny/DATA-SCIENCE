############################################
# FRANSISCA K LARASATI - CS 1656 PROJECT 1 #
# API KEY: wXyFzh7Hg6Wqgi4JusKJ9nvpv	   #
############################################

import os
import csv
import json
import sys
from requests import get

#Check if user did not provide any argument at all
if len(sys.argv) < 2:
    print("Missing Argument, Try Again!")
else:
#Getting routes by connecting to TrueTime API, printing them, and putting them into a json file: allroutes.json
    if sys.argv[1] == 'getroutes':
        response1 = get('http://realtime.portauthority.org/bustime/api/v3/getroutes?key=wXyFzh7Hg6Wqgi4JusKJ9nvpv&format=json')
        json_object1 = response1.json()
        ROUTES = json_object1["bustime-response"]["routes"]
        ROUTES1 = []
        x = 0;
        for key in ROUTES:
            print(ROUTES[x]["rt"]+", "+ROUTES[x]["rtnm"])
            d = {'rt': ROUTES[x]["rt"], 'rtnm': ROUTES[x]["rtnm"]}
            ROUTES1.append(d)
            x+=1
        f = open('allroutes.json','w')
        json.dump(ROUTES1,f)
        f.close()
#Getting directions for buses with routeID that begins with 6, printing them, and putting them into a json file: 6routes.json
    elif sys.argv[1] == 'getdirections':
        print("ALLROUTES.JSON")
        f = open('allroutes.json','r')
        allroutes = json.load(f)
        f.close()
        RTs = []
        a = 0
        for key in allroutes:
            if str(allroutes[a]["rt"])[0] == '6':
                RTs.append(allroutes[a])
            a+=1
        ARJSON = []
        a = 0
        for x in RTs:
            RTINI = str(RTs[a]["rt"])
            response2 = get('http://realtime.portauthority.org/bustime/api/v3/getdirections?key=wXyFzh7Hg6Wqgi4JusKJ9nvpv&rt={0}&format=json&rtpidatafeed=Port%20Authority%20Bus'.format(RTINI))
            json_object2 = response2.json()
            ROUTESD = json_object2["bustime-response"]["directions"]
            print(RTs[a]["rt"]+", "+RTs[a]["rtnm"]+", "+ROUTESD[0]["id"])
            print(RTs[a]["rt"]+", "+RTs[a]["rtnm"]+", "+ROUTESD[1]["id"])
            DICTION = {'rt':RTs[a]["rt"],'rtnm':RTs[a]["rtnm"],'dir':ROUTESD[0]["id"]}
            ARJSON.append(DICTION)
            a += 1
        f = open('6routes.json', 'w')
        json.dump(ARJSON,f)
        f.close()
#Getting stops ID and their names for specified routeID and direction, printing them, and putting them into a json file: mystops.json
    elif sys.argv[1] == 'getstops':
        if len(sys.argv) < 4:
            print("Missing Argument, Try Again!")
        else:
            if os.path.isfile("./6routes.json"):
                print("6routes exists!")
                f = open('6routes.json', 'r')
                SIXROUTES = json.load(f)
                f.close()
                routeID = sys.argv[2]
                direction = sys.argv[3]
                print("USER CHOSE = routeID: "+routeID+" dir: "+direction)
                index = 0
                found = 0
                while(found == 0):
                    if routeID == SIXROUTES[index]["rt"] and direction == SIXROUTES[index]["dir"]:# and direction == SIXROUTES[index]["dir"]:
                        found = 1
                        print("RouteID & Direction are VALID!")
                        RTtemp = SIXROUTES[0]
                        response3 = get('http://realtime.portauthority.org/bustime/api/v3/getstops?key=wXyFzh7Hg6Wqgi4JusKJ9nvpv&rt={a}&dir={b}&format=json&rtpidatafeed=Port%20Authority%20Bus'.format(a=routeID,b=direction))
                        json_object3 = response3.json()
                        ROUTESS = json_object3["bustime-response"]["stops"]
                        ROUTESS1 = [{"rt":routeID, "dir": direction}]
                        stops = []
                        t = 0;
                        for key in ROUTESS:
                            print(ROUTESS[t]["stpid"]+", "+ROUTESS[t]["stpnm"])
                            stops.append({"stpid": ROUTESS[t]["stpid"], "stpnm": ROUTESS[t]["stpnm"]})
                            t+=1
                        ROUTESS1.append(stops)
                        f = open('mystops.json','w')
                        json.dump(ROUTESS1,f)
                        f.close()
                    if((index == len(SIXROUTES)-1) and found == 0):
                        found = 1
                        print("ERROR: invalid route/direction combination: routeID/directon")
                    index+=1
                else:
                    print("ERROR: file 6routes.json does not exist")
#Getting arrival predictions for specified stopID and the routes in the 6routs.json file, printing them, and putting them into a json file: myarrivals.json
    elif sys.argv[1] == 'getarrivals':
        if len(sys.argv) < 3:
            print("Missing Argument, Try Again!")
        else:
            if os.path.isfile("./6routes.json"):
                print("6routes exists!")
                stpid = sys.argv[2]
                f = open('6routes.json', 'r')
                SIXROUTES2 = json.load(f)
                f.close()
                SAVE = []
                c = 0
                for key in SIXROUTES2:
                    RTT = SIXROUTES2[c]["rt"]
                    response4 = get('http://realtime.portauthority.org/bustime/api/v3/getpredictions?key=wXyFzh7Hg6Wqgi4JusKJ9nvpv&rt={a}&stpid={b}&format=json&rtpidatafeed=Port%20Authority%20Bus'.format(a=RTT,b=stpid))
                    json_object4 = response4.json()
                    key = "error"
                    if key in json_object4["bustime-response"]:
                        print("RouteID does not exists for the specified StopID")
                    else:
                        ROUTESA = json_object4["bustime-response"]["prd"]
                        y = 0
                        for key in ROUTESA:
                            print(SIXROUTES2[c]["rt"]+", "+SIXROUTES2[c]["rtnm"]+", "+ROUTESA[y]["rtdir"]+", "+ROUTESA[y]["stpid"]+", "+ROUTESA[y]["stpnm"]+", "+ROUTESA[y]["tmstmp"])
                            SAVE.append({"rt":SIXROUTES2[c]["rt"],"rtnm":SIXROUTES2[c]["rtnm"],"rtdir":ROUTESA[y]["rtdir"],"stpid":ROUTESA[y]["stpid"],"stopnm":ROUTESA[y]["stpnm"],"timstmp":ROUTESA[y]["tmstmp"]})
                            y+=1
                    c+=1
                f = open('myarrivals.json','w')
                json.dump(SAVE,f)
                f.close()
            else:
                print("ERROR: file 6routes.json does not exist")
