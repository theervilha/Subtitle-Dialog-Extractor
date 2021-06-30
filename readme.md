# Extract Dialogues From a Subtitle
The collected data can be used to, for example, modeling a QnA or analyze how characters dialogue. 

## Installation
[Install Python](https://www.python.org/downloads/)

In your terminal, install libraries:<br>
`pip install -r requirements.txt`

You can download your subtitle from any website, but it must be in the same format as matrix_example.srt. 

## Usage
You have to define:
- The filename in settings.py
- What the limit interval from one message to another will be in the settings.py file. If this time has passed and there has been no message, it is considered a new dialogue.

In your terminal, run:<br>
`python extract_dialogues.py`
