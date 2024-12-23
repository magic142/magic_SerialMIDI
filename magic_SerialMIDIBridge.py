import os
import serial
import mido
from mido import Message
import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class MidiBridgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial to MIDI Bridge")
        
        self.num_ports = 3  # Number of serial-to-MIDI mappings
        self.serial_ports = [None] * self.num_ports
        self.midi_out = [None] * self.num_ports
        self.ser = [None] * self.num_ports
        self.thread = [None] * self.num_ports
        self.running = [False] * self.num_ports
        
        # Frame for controls
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)
        
        # Serial Ports Controls
        self.label = tk.Label(self.frame, text="Select Serial Ports:")
        self.label.grid(row=0, column=0, padx=10)
        self.serial_ports_combobox = [ttk.Combobox(self.frame, width=30) for _ in range(self.num_ports)]
        for i, combobox in enumerate(self.serial_ports_combobox):
            combobox.grid(row=0, column=i+1, padx=10)
        self.refresh_ports()

        # Scan Button
        self.scan_button = tk.Button(self.frame, text="Scan Ports", command=self.refresh_ports, width=20)
        self.scan_button.grid(row=0, column=self.num_ports + 1, padx=10)

        # MIDI Outputs Controls
        self.midi_label = tk.Label(self.frame, text="Select MIDI Outputs:")
        self.midi_label.grid(row=1, column=0, padx=10)
        self.midi_out_combobox = [ttk.Combobox(self.frame, width=30) for _ in range(self.num_ports)]
        for i, combobox in enumerate(self.midi_out_combobox):
            combobox.grid(row=1, column=i+1, padx=10)
        self.refresh_midi_ports()

        # Refresh MIDI Button
        self.refresh_midi_button = tk.Button(self.frame, text="Refresh MIDI Outputs", command=self.refresh_midi_ports, width=20)
        self.refresh_midi_button.grid(row=1, column=self.num_ports + 1, padx=10)

        # Baud Rate Controls
        self.baudrate_label = tk.Label(self.frame, text="Select Baud Rate:")
        self.baudrate_label.grid(row=2, column=0, padx=10)
        self.baudrate_combobox = ttk.Combobox(self.frame, width=30, values=[9600, 19200, 38400, 57600, 115200, 31250])
        self.baudrate_combobox.grid(row=2, column=1, padx=10)
        self.baudrate_combobox.set(31250)

        # Start and Stop Buttons
        self.start_button = tk.Button(self.frame, text="Start", command=self.start, width=20)
        self.start_button.grid(row=3, column=0, pady=10, padx=10)
        self.stop_button = tk.Button(self.frame, text="Stop", command=self.stop, width=20)
        self.stop_button.grid(row=3, column=1, pady=10, padx=10)
        self.stop_button.config(state=tk.DISABLED)

    def refresh_ports(self):
        """Scan and update serial ports list"""
        ports = self.get_serial_ports()
        for combobox in self.serial_ports_combobox:
            combobox['values'] = ports
        if ports:
            self.serial_ports_combobox[0].current(0)

    def refresh_midi_ports(self):
        """Scan and update MIDI outputs list"""
        midi_ports = mido.get_output_names()
        for combobox in self.midi_out_combobox:
            combobox['values'] = midi_ports
        if midi_ports:
            self.midi_out_combobox[0].current(0)

    def get_serial_ports(self):
        """Get a list of available serial ports"""
        ports = []
        if os.name == 'posix':  # macOS or Linux
            ports = [port for port in os.listdir('/dev') if port.startswith('tty.')]
        elif os.name == 'nt':  # Windows
            for i in range(256):
                try:
                    port = f'COM{i}'
                    ser = serial.Serial(port)
                    ser.close()
                    ports.append(port)
                except (serial.SerialException, ValueError):
                    pass
        return ports

    def start(self):
        """Start the serial-to-MIDI bridge"""
        selected_ports = [combobox.get() for combobox in self.serial_ports_combobox]
        selected_midi_outputs = [combobox.get() for combobox in self.midi_out_combobox]

        if not any(selected_ports) or not any(selected_midi_outputs):
            messagebox.showerror("Error", "Please select at least one serial port and MIDI output.")
            return

        try:
            baud_rate = int(self.baudrate_combobox.get())
            for i in range(self.num_ports):
                if selected_ports[i] and selected_midi_outputs[i]:
                    selected_port_path = f"/dev/{selected_ports[i]}"
                    if not os.path.exists(selected_port_path):
                        raise FileNotFoundError(f"Port {selected_port_path} not found.")
                    self.ser[i] = serial.Serial(selected_port_path, baud_rate)
                    self.midi_out[i] = mido.open_output(selected_midi_outputs[i])
                    self.running[i] = True
                    self.thread[i] = threading.Thread(target=self.run, args=(i,), daemon=True)
                    self.thread[i].start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Error opening serial ports or MIDI outputs: {e}")

    def stop(self):
        """Stop the serial-to-MIDI bridge"""
        self.running = [False] * self.num_ports
        for i in range(self.num_ports):
            if self.ser[i]:
                self.ser[i].close()
            if self.midi_out[i]:
                self.midi_out[i].close()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def parse_serial_to_midi(self, line, index):
        """Convert serial input to MIDI message"""
        if line.startswith("MIDI message"):
            parts = line.split(", ")
            try:
                msg_type = int(parts[0].split(": ")[1])
                channel = int(parts[1].split(": ")[1])
                data1 = int(parts[2].split(": ")[1])
                data2 = int(parts[3].split(": ")[1])
                midi_msg = Message('note_on' if msg_type == 144 else 'note_off', 
                                   note=data1, velocity=data2, channel=channel)
                self.midi_out[index].send(midi_msg)
            except (IndexError, ValueError) as e:
                print(f"Error parsing MIDI message: {e}")
        else:
            print("Unrecognized line (ignored):", line)

    def run(self, index):
        """Read serial data and convert to MIDI messages"""
        while self.running[index]:
            if self.ser[index].in_waiting > 0:
                line = self.ser[index].readline().decode('utf-8', errors='ignore').strip()
                self.parse_serial_to_midi(line, index)
            time.sleep(0.01)

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = MidiBridgeApp(root)
    root.mainloop()
    
