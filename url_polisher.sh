# Insert here your URL from browser's console
URL="PASTE YOUR URL HERE"


#Divide Host and parameters
HOST=`echo $URL | sed 's/\?.*//'`
URL=`echo $URL | sed 's/[^\?]*\?//'`

#Remove date field
URL=`echo $URL | sed 's/\&date=[0-9-]*//'`
echo $HOST
echo $URL


echo -e "base_url=\"$HOST\"\nparameters=\"$URL\"\ndate_format=\"%d-%m-%Y\"\ndate_par=\"&date=\"" > parameters.py
