import pandas as pd
from pyannote.metrics.diarization import DiarizationErrorRate
from pyannote.database.util import load_rttm
from parse_xml import parse_xml

def evaluate(xml_file, rttm_file):
    """
    Evaluate diarization error rate (DER) between reference XML and predicted RTTM file.
    
    Args:
    xml_file (str): Path to the reference XML file.
    rttm_file (str): Path to the predicted RTTM file.

    Returns:
    der (float): Diarization Error Rate as a float value.
    """
    # Initialize the Diarization Error Rate (DER) metric
    metric = DiarizationErrorRate(skip_overlap=True)
    
    # Parse the reference XML and predicted RTTM
    reference = parse_xml(xml_file)
    predicted = list(load_rttm(rttm_file).values())[0]

    # Compute the Diarization Error Rate (DER)
    der = metric(reference, predicted)    
    return der

def save_results(csv_file, rttm_file, der):
    """
    Save the diarization error rate (DER) result to a CSV file, appending new results.

    Args:
    csv_file (str): Path to the CSV file.
    rttm_file (str): Path to the RTTM file being evaluated.
    der (float): Diarization Error Rate value to save.
    """
    pred_num_spk = len((list(load_rttm(rttm_file).values())[0].labels()))
    
    new_result = pd.DataFrame({'file': [rttm_file], 'DER': [f"{der * 100:.2f}"], 'pred_num_spk':[pred_num_spk]})
    try:
        # Attempt to read existing CSV file
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        # Create a new DataFrame if file not found
        df = pd.DataFrame(columns=['file', 'DER'])
    
    # Append new results and save to CSV
    df = pd.concat([df, new_result], ignore_index=True)
    df.to_csv(csv_file, index=False)
    print(f"Results for {rttm_file} saved to {csv_file}.")

if __name__ == "__main__":
    import argparse
    
    # Argument parser
    parser = argparse.ArgumentParser(description='Evaluate a diarization result.')
    parser.add_argument('xml_file', type=str, help='Path to the REFERENCE Pangloss XML annotation file')
    parser.add_argument('rttm_file', type=str, help='Path to the PREDICTED RTTM file')
    parser.add_argument('-w', '--write_results', type=str, nargs='?', const=True, 
                        help='Optional: Provide a CSV path to write results or leave empty to use a default path "results.csv"')
    args = parser.parse_args()

    # Call the evaluation function
    der = evaluate(args.xml_file, args.rttm_file)
    
    # Save the results if the --write_results option is provided
    if args.write_results:
        csv_file = args.write_results if isinstance(args.write_results, str) else 'results.csv'
        save_results(csv_file, args.rttm_file, der)
