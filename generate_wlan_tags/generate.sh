#!/bin/bash

SSID=
ENC=
PSK=
OUTPUT=

# use parameters
for i in $*
do
  case $i in
    (--ssid=*)
      SSID=${i#--ssid=}
    ;;
    (--enc=*)
      ENC=${i#--enc=}
    ;;
    (--psk=*)
      PSK=${i#--psk=}
    ;;
    (--out=*)
      OUTPUT=${i#--out=}
    ;;
    (*)
      echo "usage: $0 [--ssid=...] [--enc=...] [--psk=...] [--out=...]" 1>&2
      exit
    ;;
  esac
done

TEMPDIR=$(mktemp -d)
[ -d "$TEMPDIR" ] || exit
trap "rm -rf $TEMPDIR; exit" INT TERM EXIT
BASEDIR=$(dirname $0)

# fill in with default / random values
: ${SSID:=$(pwgen 8 1)}
: ${ENC:=WPA}
: ${PSK:=$(pwgen -c -n 63 1)}
: ${OUTPUT:=$SSID}
PSK1=${PSK:0:32}
PSK2=${PSK:32}
#DMTX="WLAN:$SSID:$ENC:$PSK"
DMTX="WIFI:S:$SSID;T:$ENC;P:$PSK;;"

echo "generating card with" 1>&2
echo " SSID: $SSID" 1>&2
echo " ENC: $ENC" 1>&2
echo " PSK: $PSK" 1>&2
echo "writing to: $OUTPUT.pdf" 1>&2

sed -e "s/SSID-TEMPLATE/$SSID/g" -e "s/ENC-TEMPLATE/$ENC/g" -e "s/PSK1-TEMPLATE/$PSK1/g" \
 -e "s/PSK2-TEMPLATE/$PSK2/g" -e "s/DMTX-TEMPLATE/$DMTX/g" \
 < $BASEDIR/wlancard_template.tex > $TEMPDIR/$OUTPUT.tex

(
cd $TEMPDIR 
latex --interaction batchmode $OUTPUT
dvipdf $OUTPUT
)

cp $TEMPDIR/$OUTPUT.pdf .

