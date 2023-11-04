# asr-tagalog
Project for COSI 136a ASR

# Requirements
Command line: ffmpeg, sox/soxi

Python:
```sh
pip install -r requirements.txt
```

# Resampling
Resample all mp3 files in a directory to wav files:
```sh
./resample.sh <DIR>
```

Check the total length of the resampled files:
```sh
soxi resampled/ | tail -n1
```
