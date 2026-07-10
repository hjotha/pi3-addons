# pi3-addons Quickstart

## Purpose
`pi3-addons` provides a system tray applet (`temp-applet`) to monitor CPU temperature and usage, and automatically control a cooling fan.

## Entry Points
- `temp-applet.py`: The main executable script.

## Run Commands
```bash
python temp-applet.py
# or
./temp-applet.py
```

## Real Operations
- **Temperature Monitoring**: Uses `vcgencmd measure_temp` to read the CPU temperature.
- **CPU Usage Monitoring**: Uses `psutil.cpu_percent()` to read CPU usage.
- **Fan Control**: Toggles a fan connected to GPIO BCM pin 15 using `RPi.GPIO`. Turns on if temperature >= 60°C or CPU usage >= 60%.
- **System Tray Icon**: Creates a GTK app indicator displaying the current temperature using `gi.repository.AppIndicator3` and `PIL` (Python Imaging Library).
  - The temperature is displayed in red if it reaches 60°C, and green otherwise.
  - A red circle outline is drawn (`draw.ellipse`) if the fan is currently active.

## Known Limitations
- **Hardware Dependent**: Requires a Raspberry Pi (relies on `vcgencmd` and `RPi.GPIO`).
- **Font Dependency**: Hardcodes the use of `/usr/share/fonts/truetype/freefont/FreeMono.ttf`, which must be present on the system.
- **Platform**: Requires GTK 3.0 and a desktop environment supporting AppIndicator3.