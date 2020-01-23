@ECHO off
cd "<Full path to web-scraper main>"
set p1=-url "<indeed url to scrape>"
set p2=-kwor "<Keyword 1>" "<Keyword 2>" "<etc..>"
set p3=-sms
set p4=-ph="<Phone number to send info to>"
set p5=-e="<Host email address>"
set p6=-p="<Host email password>"
python -u Main.py %p1% %p2% %p3% %p4% %p5% %p6%
