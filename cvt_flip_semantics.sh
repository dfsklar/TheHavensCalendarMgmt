# $1 = input ICS filepath
# $2 = output ICS filepath
# $3 = condo unit abbrev

cd /root/TheHavensCalendarMgmt/

python cvt_flip_semantics.py $3 < $1 > /tmp/cvtflip_$3.out

diff /tmp/cvtflip_$3.out $2  && exit

# The file has changed
echo "File changed so we are going to deploy a new ics file at $2"
mv /tmp/cvtflip_$3.out $2
