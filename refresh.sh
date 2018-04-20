# $1 = target name such as "bh" or "sh" or "union"
# $2 = the URL to proxy

# Why do this?

# It turns out that many rental-marketplace services cannot 
# read an ICS file directly from google's servers, but are
# perfectly happy with a URL that points to my own server
# EVEN THOUGH THE ICS CONTENT IS IDENTICAL.

# So this really is nothing more than a copy from google's servers
# to mine... with absolutely ZERO modification of the ICS content.

# Care is taken to ensure the destination file is overwritten only
# if the wget from google's servers produced a valid non-empty file.

TARGET=$1
URL=$2
DEST_FOLDER=$3

wget -O /tmp/$1_test.ics $2

LINECOUNT=`wc -l < /tmp/$1_test.ics`

echo $LINECOUNT

if test $LINECOUNT -lt 200 
then
    echo "File /tmp/$1_test.ics looks suspiciously small -- ignoring"
    exit 3
fi

fgrep --silent VEVENT /tmp/$1_test.ics && \
fgrep --silent HAVEN /tmp/$1_test.ics && \
fgrep --silent 'END:VCALENDAR' /tmp/$1_test.ics && \
echo "DOING THE MOVE NOW" && \
echo cp /tmp/$1_test.ics $DEST_FOLDER/$1.ics && \
cp /tmp/$1_test.ics $DEST_FOLDER/$1.ics && \
echo "Well the mv is done" && \
exit 0

echo "File /tmp/$1_test.ics was missing expected strings -- ignoring"
exit 2
