#!/usr/bin/bash

set -o pipefail

DIR=$1

# resample each mp3 to wav, 16k Hz, and 1 channel
for mp3 in $DIR/*.mp3; do
    path=$(echo $mp3 | tr -s '/')
    name=$(basename $path | sed 's/\.mp3/\.wav/')
    ffmpeg -i $path -acodec pcm_s16le -ar 16000 -ac 1 resampled/$name
done
