#!/usr/bin/env bash

set -eou pipefail
MUSICFOLDER="/media/Ext/Music"
while true
do
    LINE=$(cat albums.csv   | head -1 | tr "," "\n" ) || $(echo "albums.csv seems empty. Exiting" && exit) 
    echo $LINE
    ARTIST=$(echo "$LINE" | head -1) 
    echo $ARTIST
    ALBUM=$(echo "$LINE" | head -2 | tail -1)
    echo $ALBUM
    DLURL=$(echo "$LINE" | head -3 | tail -1)
    echo $DLURL
    COVER=$(echo "$LINE" | head -4 | tail -1)
    echo $COVER

    if [ "$ARTIST" != "" ]
    then
        echo "Downloading ${ARTIST} - ${ALBUM}..."
        youtube-multi-dl -f best -q 0 -a "$ARTIST" --album "$ALBUM" "$DLURL" || $(echo "Youtube-Multi-DL failed. Exiting." && exit)
        # download cover
        if [ "$COVER" != "" ]
        then
            echo "Getting album cover..."
            # get file extension
            EXTENSION=$(echo "$COVER" | awk -F . '{print $NF}')
            # download file
            wget "$COVER" -O "${ALBUM}/cover.jpg"
            echo "Done."
        fi
        echo "Culling album from albums.csv..."
        tail -n +2 "albums.csv" > "albums.tmp" && mv "albums.tmp" albums.csv
        echo "Done."
        echo ""
        
        if [ ! -d "${MUSICFOLDER}/${ARTIST}" ]
        then
            mkdir "${MUSICFOLDER}/${ARTIST}"
        fi
        echo "Moving ${ALBUM} to ${MUSICFOLDER}/${ARTIST}..."
        mv "${ALBUM}" "${MUSICFOLDER}/${ARTIST}"

    else
        echo "Done"
        break
    fi
done
