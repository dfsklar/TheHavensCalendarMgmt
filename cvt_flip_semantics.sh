# $1 = input ICS filepath
# $2 = output ICS filepath
# $3 = condo unit abbrev

source /home/sklawlxv/virtualenv/var/www/BIRCHHAVEN/pythonapp/2.7/bin/activate 

cd /home/sklawlxv/TheHavensCalendarMgmt/

python cvt_flip_semantics.py $3 < $1 > /tmp/cvtflip_$3.out || exit 1

mv /tmp/cvtflip_$3.out $2
