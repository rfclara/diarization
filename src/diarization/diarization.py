import argparse
from pyannote.audio import Pipeline
from pathlib import Path
import torch
import textgrid
import torchaudio

"""From the audio file, returns the diarization result in RTTM and TextGrid format
contains the speaker id, start time, end time"""

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                    use_auth_token="YUR_HUGGINGFACE_TOKEN",)

pipeline.to(torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
print("Using device:", pipeline.device)

def diarize_audio(audio_file, num_speakers=None):
    # Pre-load audio in memory
    waveform, sample_rate = torchaudio.load(audio_file)
    audio_input = {"waveform": waveform, "sample_rate": sample_rate}
    diarization = pipeline(audio_input, num_speakers=num_speakers)
    audio_path = Path(audio_file)
    rttm_filename = audio_path.with_suffix('.rttm')
    textgrid_filename = audio_path.with_suffix('.TextGrid')
    with rttm_filename.open("w") as rttm:
        diarization.write_rttm(rttm)
    write_textgrid(diarization, textgrid_filename)

def write_textgrid(diarization, textgrid_filename):
    tg = textgrid.TextGrid()
    tiers = {}

    # Iterate over segments and associated speaker information
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        start = segment.start
        end = segment.end

        # Check if the speaker already has a tier, otherwise create one
        if speaker not in tiers:
            tiers[speaker] = textgrid.IntervalTier(name=speaker)
            tg.append(tiers[speaker])

        # Add the segment to the corresponding speaker tier
        tiers[speaker].add(start, end, "")

    # Write the TextGrid to file
    with open(textgrid_filename, 'w') as f:
        tg.write(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Diarize an audio file, saves the segmented content in rttm and TextGrid formats.')
    parser.add_argument('audio_file', type=str, help='Path to the audio file')
    parser.add_argument('-n', '--num_speakers', type=int, help='Number of speakers to diarize')
    args = parser.parse_args()
    diarize_audio(args.audio_file, args.num_speakers)
