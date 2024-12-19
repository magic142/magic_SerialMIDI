# Serial to MIDI Bridge v0.4 by magic142

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

   or download the file and open it

2. Install the required dependencies:

   pip install mido pyserial

3. Run the application

## Usage

Open the application, and select the serial ports and MIDI outputs.

Set the baud rate and click "Start" to convert data from serial to MIDI.



## Version History


## v0.1
- Initial release of the Serial to MIDI Bridge.
- Added basic functionality for a fixed and hard-coded serial to MIDI conversion.
- Implemented basic Tkinter GUI to start and stop the conversion.

## v0.2
- Added the Serial Port, MIDI Bus and Baud Rate selection dropdown menu.
- Added the function to scan serial ports and MIDI buses.
- Improved error handling for missing ports and MIDI devices.
- Improved Tkinter GUI.

## v0.3
- Enhanced serial input and MIDI output support allow multiple inputs to be routed to different outputs.
- Improved user interface for better UX.
- Resolved the issue that required both serial inputs to be selected before starting.

## v0.4 (current)
- Added one more input routing, now it can handle three different routings.
- Improved user interface for better UX.
