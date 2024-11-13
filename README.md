# Serial to MIDI Bridge v0.3 by magic142

This project is a Serial to MIDI Bridge application that converts serial port data into MIDI messages and can route two serial inputs to different MIDI buses simultaneously.
It uses Python and the `mido` library to send MIDI messages to a selected MIDI output device. The application is controlled via a simple GUI built with Tkinter.

## Features

- Select two serial ports
- Select MIDI outputs for both ports
- Set baud rate for serial communication
- Start and stop the bridge
- Supports multiple serial ports and MIDI outputs

## Requirements

- Python 3.x
- `mido` library
- `pyserial` library
- Tkinter (usually comes with Python by default)

## Installation

1. Clone the repository:

   git clone https://github.com/magic142/magic_SerialMIDI.git

2. Install the required dependencies:

pip install mido pyserial

3. Run the application:

python your_script_name.py

## Usage

Open the application, select the serial ports and MIDI outputs.

Set the baud rate and click "Start" to begin converting data from serial to MIDI.



## Version History


## v0.1
- Initial release of the Serial to MIDI Bridge.
- Added basic functionality for a fixed and hard-coded serial to MIDI conversion.
- Implemented Tkinter GUI with port and MIDI selection.

## v0.2
- Fixed bug where selecting one serial port would not work.
- Added feature to set the baud rate, as well as the MIDI bus to route.
- Improved error handling for missing ports and MIDI devices.


## v0.3
- Enhanced MIDI output support (added multiple outputs).
- Improved user interface for better UX.

