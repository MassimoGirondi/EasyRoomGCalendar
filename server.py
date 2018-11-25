import os
import parameters as par
import requests
import datetime
from icalendar import Alarm,Event,Calendar
import flask
from flask import Response,Flask


def cal_generator():
    #download next 6 weeks
    today=datetime.date.today()
    dates=[today+datetime.timedelta(days=7*x) for x in range(0,6)]
    cals=[]
    for d in dates:
        formatted=d.strftime(par.date_format)
        url=par.base_url+par.parameters+par.date_par+formatted
        #print(url)
        try:
            text=requests.get(url).text
            cals.append(text)
        except:
            print("Error getting events for "+formatted)

    final_cal=""
    if len(cals)<=2:
        print("ERROR: too few results!")
        exit()

    #Delete the end tag of the first week
    final_cal=cals[0][:-14]+"\n"

    # Concatenate the events for every week, just stripping
    # the preamble and the end of the file

    for c in cals[1:]:
        first=c.find("BEGIN:VEVENT")
        final_cal+=c[first:-14]
        final_cal+="\n"
    #add the end tag 
    final_cal+="END:VCALENDAR"


    #Just to debug and faster development
    #open("/tmp/cal.ics","w").write(final_cal)
    #final_cal=open("/tmp/cal.ics").read()



    ical=Calendar.from_ical(final_cal)
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
