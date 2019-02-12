# EasyRoom to Google Calendar bridge

This is a simple bridge between the Easyroom platform and Google Calendar

I developed this to have my university lessons directly on my Google Calendar. However, it can work easily also with other calendar software.

To use it you need to run it on a host that is reachable by your calendar provider. In the case of Google Calendar, this need to be a server with a public address. One of the free hosters you can use is Heroku: it works great with the free plan.

This has been developed to be used with the University of Trento EasyRoom service. This is not related in any way to it and it's not officially supported or endorsed by it.
Maybe it's against the Term of Service, you have been warned :).


## Program logic

Basically, this program merges together the calendars for the next 6 weeks, providing a iCalendar file readable by a Calendar manager.

## Installation

- Clone this repository
- Visit the [EasyRoom portal](https://easyroom.unitn.it/Orario), select your courses and click on `View timetable` (in italian: `Mostra orario`). 
- Open the console of your browser (`CTRL+Shift+c` or `F12`) and select the `Network` tab.
- Keeping it open, return to the EasyRoom page and click `Export weekly commitments to your personal calendar`(in italian: `Esporta gli impegni settimanali nel calendario personale`).
- In the previously opened network log, you should see a line like `ec_download_ical_grid.php?.....`, right click on it and select `Copy URL`
- Paste the above text into the file `url_polisher.sh`, replacing the text `PASTE YOUR URL HERE`
- Run the script: `bash url_polisher.sh`
- Then, you should be able to get your calendar: test it running `python3 server.py` and visiting the shown URL.
- If everything is correct you can run it in Heroku or any other system: in this case you may have to commit the modifications before uploading to the server.
- Add the events to your calendar software and set the auto update interval to something reasonable (if you can set it). The URL you have to specify is the one that you used to test the server: `http(s)://NAME-OR-IP:PORT/cal.ics`. 


# UPDATE 12/02/2018
Now, it seems that now the website send directly the whole calendar. However, the url is not accepted into Google Calendar.

The `server_single.py` now is just a proxy to the file given by EasyRoom.  
The start date can be set into the parameters file.


## License

The software contained in this repository is free software, released under the GNU Public License v3 license. See [LICENSE](LICENSE) for more informations.

