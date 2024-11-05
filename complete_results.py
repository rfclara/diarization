import pandas as pd
from pathlib import Path
import librosa
from parse_xml import count_speakers
from diarization import diarize_audio
from evaluation import evaluate
from pyannote.database.util import load_rttm


def get_wav_length(wav_path):
    """Returns the duration of the wav file in seconds."""
    audio, sample_rate = librosa.load(wav_path, sr=None)
    return int(librosa.get_duration(y=audio, sr=sample_rate))


def process_file_data(file_path):
    """Processes each file by calculating its duration and gold speakers."""
    path = Path(file_path)
    wav_path = path.with_suffix('.wav')
    xml_path = path.with_suffix('.xml')

    # Compute duration
    duration = get_wav_length(wav_path)

    # Count speakers in XML (gold number of speakers)
    gold_speakers = count_speakers(xml_path)

    return duration, gold_speakers


def compute_der(row):
    print("compute_der")
    """Computes the original DER and predicted speakers after diarization."""
    rttm_path = Path(row['file']).with_suffix('.rttm')
    wav_path = Path(row['file']).with_suffix('.wav')
    xml_path = Path(row['file']).with_suffix('.xml')

    # Diarize the audio file (first diarization without knowing the number of speakers)
    diarize_audio(wav_path)

    # Load RTTM file to determine the number of predicted speakers after diarization
    annotation = list(load_rttm(rttm_path).values())[0]
    pred_speakers = len(annotation.labels())  # Count predicted speakers after diarization

    # Evaluate diarization against the gold reference
    der = evaluate(xml_path, rttm_path)

    return f"{der * 100:.2f}", pred_speakers


def compute_new_der(row):
    print("comput_new_der")
    """Computes the DER after diarization using the gold number of speakers."""
    rttm_path = Path(row['file']).with_suffix('.rttm')
    wav_path = Path(row['file']).with_suffix('.wav')
    xml_path = Path(row['file']).with_suffix('.xml')

    # Diarize the audio file with the given number of speakers
    diarize_audio(wav_path, row['gold_num_spk'])

    # Evaluate the diarization result
    new_der = evaluate(xml_path, rttm_path)

    return f"{new_der * 100:.2f}"


def update_results(df):
    """Updates the DataFrame with durations, speaker counts, DER, predicted speakers, and new DER."""
    # Process each file and compute duration and gold_num_spk
    processed_data = [process_file_data(file) for file in df['file']]
    df[['duration', 'gold_num_spk']] = pd.DataFrame(processed_data, columns=['duration', 'gold_num_spk'])

    # Compute DER and predicted speakers after diarization
    der_and_pred_spk = df.apply(lambda row: compute_der(row), axis=1)
    df[['DER', 'pred_num_spk']] = pd.DataFrame(der_and_pred_spk.tolist(), index=df.index)

    # Compute the new DER using the gold number of speakers
    df['new_DER'] = df.apply(compute_new_der, axis=1)

    return df


# Load the results CSV
results = pd.read_csv("results.csv")

# Update DataFrame with necessary calculations
results = update_results(results)

# Save the updated DataFrame back to the CSV file
results.to_csv("results.csv", index=False)

print("Durations, speaker counts, DER, predicted speakers, and new_DER have been updated and saved.")
