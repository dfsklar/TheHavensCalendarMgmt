# $1 = target name such as "bh" or "sh" or "union"
# $2 = the URL to proxy

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
fgrep --silent END:VCALENDAR /tmp/$1_test.ics && \
echo "DOING THE MOVE NOW" && \
mv /tmp/$1_test.ics $DEST_FOLDER/$1.ics && \
exit 0

echo "File /tmp/$1_test.ics was missing expected strings -- ignoring"
exit 2
