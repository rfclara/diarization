```markdown
# Une nouvelle évaluation des capacités multilingues
des modèles neuronaux pré-entrainés de la parole

Evaluating [`pyannote.audio`](https://github.com/pyannote/pyannote-audio) on endangered languages. Exporting segmented Praat TextGrid for linguists.

## Introduction

This project aims to evaluate the performance of the pyannote audio diarization toolkit on endangered languages from the Pangloss collection. The goal is to export segmented Praat TextGrids that can be used by linguists for further analysis.

Ces travaux ont été partiellement financés par le projet D IAGNO STIC soutenu par l’Agence
d’Innovation de Défense (contrat no 2022 65 007) et le projet D EEP T YPO soutenu par
l’Agence Nationale de la Recherche (ANR-23-CE38-0003-01).

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

Install [`pyannote.audio`](https://github.com/pyannote/pyannote-audio) with `pip install pyannote.audio`
Accept [`pyannote/segmentation-3.0`](https://hf.co/pyannote/segmentation-3.0) user conditions
Accept [`pyannote/speaker-diarization-3.1`](https://hf.co/pyannote/speaker-diarization-3.1) user conditions
Create access token at [`hf.co/settings/tokens`](https://hf.co/settings/tokens).

## Usage

To run the diarization on your audio files, use the following command:

```bash
python diarization.py <path_to_wav_file>
```
