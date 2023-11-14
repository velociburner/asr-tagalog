# asr-tagalog
Project for COSI 136a ASR

# Requirements
Command line: ffmpeg, sox/soxi

Python:
Using Python 3.9+,
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

# Split corpus
Split directory of parallel .TextGrid and .wav files into short segments to use in a model:
```sh
usage: split_corpus.py [-h] [--max-seconds MAX_SECONDS] indir outdir

positional arguments:
  indir                 Directory of parallel .TextGrid and .wav files to load
  outdir                Directory to write segmented parallel .txt and .wav files

options:
  -h, --help            show this help message and exit
  --max-seconds MAX_SECONDS
                        Maximum duration in seconds of segmented audio files
```
