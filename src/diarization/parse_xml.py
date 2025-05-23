import argparse
import xml.etree.ElementTree as ET
from pyannote.core import Annotation, Segment
from pathlib import Path


"""
parses a Pangloss XML annotation file and 
returns the annotations in pyannote.core.Annotation type
example of S tag : 
<S id='S1' who="Questions">
<AUDIO start='0.000' end='1.900'/>
<FORM kindOf='phono'>Quelles sont les langues que tu connais ?</FORM>
</S>
"""

def count_speakers(xml_file):
    """
    Counts the number of unique speakers in the given XML file.
    Returns 0 if there is no 'who' attribute or if the 'who' attribute is empty. 
    TODO : check problem who='A' and 'B' in some files
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    speakers = set()  # A set to keep track of unique speakers

    for segment in root.findall('S'):
        speaker = segment.get('who')
        if speaker and speaker.strip():  # Check if 'who' exists and is not empty or just whitespace
            speakers.add(speaker)  # Add speaker to the set
    print(speakers)
    return len(speakers) if speakers else 0

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    annotations = Annotation()
    
    for segment in root.findall('S'):
        speaker = segment.get('who')
        audio = segment.find('AUDIO')
        start_time = float(audio.get('start'))
        end_time = float(audio.get('end'))

        # add Segment to the Annotation object
        annotations[Segment(start_time, end_time)] = speaker

    return annotations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a Pangloss XML annotation file. Converts pangloss xml to rttm format, supported by pyannote-audio.')
    parser.add_argument('xml_file', type=str, help='Path to the Pangloss XML annotation file')
    args = parser.parse_args()

    # Parse the XML and return annotations in pyannote.core.Annotation format
    annotations = parse_xml(args.xml_file)
    rttm_path = Path(args.xml_file).with_suffix('.rttm')
    with rttm_path.open("w") as rttm:
        annotations.write_rttm(rttm)
    #print(annotations)
    print(count_speakers(args.xml_file))
