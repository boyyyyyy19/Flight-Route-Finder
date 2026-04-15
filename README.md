# ✈️ Flight Route Finder

Flight Route Finder is a Python-based desktop application that helps virtual pilots and aviation enthusiasts quickly calculate flight distances, estimate flight times, and generate SimBrief flight plans using ICAO airport and aircraft codes.

The application features a modern Tkinter GUI, smart caching, and a searchable aircraft selection to make route planning fast and reliable.

---

## 🚀 Features

### 🛫 Airport Coordinate Lookup
- Enter **ICAO airport codes** for departure and arrival
- Uses OpenStreetMap (Nominatim) to determine accurate airport coordinates

### 📏 Distance Calculation
- Calculates **great‑circle distance** between airports
- Displays results in:
  - Kilometers (km)
  - Nautical miles (nm)

### ⏱️ Flight Time Estimation
- Estimates flight time based on:
  - Aircraft cruise speed
  - Route distance
- Adds realistic buffer time for taxi, takeoff, and landing

### ✈️ Searchable Aircraft Type Dropdown
- Aircraft selected using a **dropdown menu**
- Supports **search‑as‑you‑type filtering**
- Uses ICAO aircraft type codes
- Prevents typing errors and invalid aircraft entries

### 🧠 Smart Route Caching
- Previously calculated routes are stored in memory
- Repeated searches return instantly without recalculating data

### 🌐 SimBrief Integration
- Automatically generates a **pre-filled SimBrief flight planning URL**
- Opens directly in your web browser with:
  - Departure airport
  - Arrival airport
  - Aircraft type

---

## 🖥️ User Interface Highlights

- Clean and responsive Tkinter GUI
- Clear status messages and error handling
- Results displayed in a readable summary
- One‑click access to SimBrief flight planning

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter / ttk** – GUI framework
- **geopy** – Distance calculations
- **OpenStreetMap Nominatim** – Airport geocoding
- **SimBrief** – Online flight planning integration

---

## ▶️ How It Works (High‑Level)

1. User enters departure and arrival ICAO codes
2. User selects an aircraft type from the searchable dropdown
3. The app:
   - Retrieves airport coordinates
   - Calculates great‑circle distance
   - Estimates flight time based on aircraft speed
4. Results are displayed in the UI
5. A SimBrief route can be opened with one click

---

## 📦 Requirements

- Python 3.9 or newer
- Required Python packages:
  - `geopy`

Install dependencies using:

```bash
pip install geopy
``
