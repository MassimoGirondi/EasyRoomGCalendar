import os
import parameters as par
import requests
import datetime
from icalendar import Alarm,Event,Calendar
import flask
from flask import Response,Flask


def cal_generator():
    url=par.base_url+par.parameters+par.date_par+par.start_date
    text=""
    try:
        text=requests.get(url).text
    except:
        print("Error getting events for "+formatted)


    print(text)

    ical=Calendar.from_ical(text)
    #Transform the description and obtain location (hopefully the format is always the same)
    #Ex: Lesson name Teacher name  Aula A108 [Dipartimenti - POVO] Lezione


    #Just ignore the first subcomponent (auxiliary data)
    to_remove=[]
    for event in ical.subcomponents[1:]:

        # Workaround to solve a bug(?) of EasyRoom
        if 'chiusura_typ' in event['description']:
            to_remove.append(event)
        else:
            desc=event['description']
            ai=desc.find("Aula")
            desc1=desc[:ai]
            room=desc[ai:]
            event['description']=desc1
            event['location']=room
        
            #Add a reminder 30 minutes before (in Google Calendar this means a notification)
            #event.subcomponents.append(Alarm(action="DISPLAY", DESCRIPTION="This is a reminder", TRIGGER="-P0DT0H30M0S"))    
            #print(event)
    
    for t in to_remove:
        ical.subcomponents.remove(t)     
    '''
    out=open("/tmp/cal1.ics","wb")
    out.write(ical.to_ical())
    out.close()
    '''
    #Print the calendar
    return ical.to_ical()



#Flask webserver initalization
app = Flask(__name__)

#Default route
@app.route('/')
def home():
    return "I'm working! Visit /cal.ics to obtain your calendar"


@app.route('/cal.ics')
def cal_ics():
    #return cal_generator()
    #return a inline file to save
    return Response(
        cal_generator(),
        mimetype="text/ics",
        headers={"Content-disposition":
                 "attachment; filename=cal.ics"})


#Start the server
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
