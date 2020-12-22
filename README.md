# edlserver
 
A lightweight External Dynamic List (EDL) server for publishing MS Office 365 URLs and IPs for use by Palo Alto Networks NGFWs.
 
Step 1: Build the lightweight docker web service (built from scratch on top of Alpine with lighttpd)
 
`docker build . -t edlserver`
 
Step 2: Start the docker web service (replace `/home/user/edlserver` with your specific path where these files reside)
 
`docker run -d --name edlserver -p 80:80 -v /home/user/edlserver/dodedl.html:/var/www/localhost/htdocs/dodedl.html:ro -v /home/user/edlserver/gcchedl.html:/var/www/localhost/htdocs/gcchedl.html:ro -v /home/user/edlserver/commedl.html:/var/www/localhost/htdocs/commedl.html:ro edlserver`
 
Step 3: Create a cronjob as follows by going into `crontab -e` (this will check for updates from o365 every 15 minutes)
 
`*/15 * * * * python3 /home/fedadmin/edlserver/dod-update.py >> /home/fedadmin/edlserver/cronout-dod.log`
 
`*/15 * * * * python3 /home/fedadmin/edlserver/gcch-update.py >> /home/fedadmin/edlserver/cronout-gcch.log`
 
`*/15 * * * * python3 /home/fedadmin/edlserver/comm-update.py >> /home/fedadmin/edlserver/cronout-comm.log`
