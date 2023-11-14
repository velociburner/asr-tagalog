from collections import namedtuple
from pathlib import Path

from praatio import tgio
from pydub import AudioSegment


Interval = namedtuple('Interval', ['start', 'end', 'label'])


def get_entries(textgrid):
    tier = textgrid.tierNameList[0]
    entries = textgrid.tierDict[tier].entryList
    return [Interval(*entry) for entry in entries]


def get_intervals(entries: list[Interval], max_seconds: int):
    intervals: list[Interval] = []

    labels: list[str] = []
    start = entries[0].start
    for i, interval in enumerate(entries):
        seconds = interval.end - start

        # end of file
        if i == len(entries) - 1:
            labels.append(interval.label)
            end = interval.end
            intervals.append((Interval(start, end, " ".join(labels))))

        # end of interval
        if seconds > max_seconds:
            end = entries[i - 1].end
            intervals.append((Interval(start, end, " ".join(labels))))

            # reset interval
            start = entries[i].start
            labels = []

        labels.append(interval.label)

    return intervals


def get_audio_segments(intervals: list[Interval], audio: AudioSegment):
    segments = []
    for interval in intervals:
        # use milliseconds
        start_time = interval.start * 1000
        end_time = interval.end * 1000
        segments.append(audio[start_time: end_time])
    return segments


def write_segments(dir: Path, source: str, intervals: list[Interval],
                   audio_segments: list[AudioSegment]):
    # double check we have the same number of text and audio segments
    assert len(intervals) == len(audio_segments)

    for i, (interval, segment) in enumerate(zip(intervals, audio_segments)):
        filename = dir / f"{source}_{i}"
        text_path = filename.with_suffix(".txt")
        wav_path = filename.with_suffix(".wav")

        with text_path.open('w', encoding='utf8') as f:
            f.write(interval.label)
        with wav_path.open('w', encoding='utf8') as f:
            segment.export(wav_path, format="wav")


def main(indir: Path, outdir: Path, max_seconds: int):
    outdir.mkdir(parents=True, exist_ok=True)
    for file in indir.glob("*.wav"):
        source = file.with_suffix("").name
        print(source)
        audio = AudioSegment.from_wav(file)
        textgrid = tgio.openTextgrid(file.with_suffix(".TextGrid"))
        entries = get_entries(textgrid)
        intervals = get_intervals(entries, max_seconds)
        audio_segments = get_audio_segments(intervals, audio)
        write_segments(outdir, source, intervals, audio_segments)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "indir",
        type=Path,
        help="Directory of parallel .TextGrid and .wav files to load"
    )
    parser.add_argument(
        "outdir",
        type=Path,
        help="Directory to write segmented parallel .txt and .wav files"
    )
    parser.add_argument(
        "--max-seconds",
        type=int,
        default=20,
        help="Maximum duration in seconds of segmented audio files"
    )
    args = parser.parse_args()

    main(args.indir, args.outdir, args.max_seconds)
