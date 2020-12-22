# edlserver
 
A lightweight External Dynamic List (EDL) server for publishing MS Office 365 URLs and IPs for use by Palo Alto Networks NGFWs.
 
Step 1: Build the lightweight docker web service (built from scratch on top of Alpine with lighttpd)
 
`docker build . -t edlserver`
 
Step 2: Start the docker web service (replace `/home/user/edlserver` with your specific path where these files reside; beware the wrap below - it is one contiguous entry!)
 
`docker run -d --restart unless-stopped --name edlserver -p 80:80 -v /home/user/edlserver/dodedl.txt:/var/www/localhost/htdocs/dodedl.txt:ro -v /home/user/edlserver/gcchedl.txt:/var/www/localhost/htdocs/gcchedl.txt:ro -v /home/user/edlserver/commedl.txt:/var/www/localhost/htdocs/commedl.txt:ro edlserver`
 
Step 3: Create a cronjob as follows by going into `crontab -e` (this will check for updates from o365 every 15 minutes; don't forget to change the path from /home/user/edlserver to your real path)
 
`*/15 * * * * python3 /home/user/edlserver/dod-update.py > /home/user/edlserver/cronout-dod.log`
 
`*/15 * * * * python3 /home/user/edlserver/gcch-update.py > /home/user/edlserver/cronout-gcch.log`
 
`*/15 * * * * python3 /home/user/edlserver/comm-update.py > /home/user/edlserver/cronout-comm.log`
 
Step 4: Access your EDLs at:
 
`http://<YOUR_IP>/dodedl.txt`
 
`http://<YOUR_IP>/gcchedl.txt`
 
`http://<YOUR_IP>/commedl.txt`
 
For the everyone's convenience, I have published the three URL EDLs at http://edl.ohanalytics.com:
 
-[O365 Commercial EDL](http://edl.ohanalytics.com/commedl.txt)
-[O365 GCC high EDL](http://edl.ohanalytics.com/gcchedl.txt)
-[O365 DoD EDL](http://edl.ohanalytics.com/dodedl.txt)
 
The EDLs listed above are updated every 15 minutes as updates are found
