import tkinter as tk
from tkinter import ttk, font
import webbrowser
import urllib.parse
from geopy.distance import great_circle
from geopy.geocoders import Nominatim

# ==========================
# Aircraft speeds (GLOBAL)
# ==========================
AIRCRAFT_SPEEDS = {
    "B738": 840, "A320": 828, "B77W": 907, "A388": 900, "C172": 226,
    "A225": 850, "A306": 870, "A310": 890, "A318": 828, "A319": 828,
    "A321": 828, "A20N": 828, "A21N": 828, "A332": 880, "A333": 880,
    "A359": 903, "A35K": 903, "B744": 920, "B752": 876, "B772": 907,
    "B787": 902, "C130": 593, "C17": 926, "CRJ7": 870, "CRJ9": 870,
    "DC10": 900, "E170": 870, "E190": 870, "L101": 965, "MD11": 940,
    "PC12": 528, "SR22": 333, "TBM9": 611
}

# Cache
route_cache = {}

# ==========================
# Utilities
# ==========================
def get_airport_coordinates(icao):
    geolocator = Nominatim(user_agent="flight-planner")
    location = geolocator.geocode(f"{icao} airport")
    if not location:
        raise Exception(f"Airport not found: {icao}")
    return (location.latitude, location.longitude)

def calculate_distance(dep, arr):
    km = great_circle(dep, arr).kilometers
    nm = km * 0.539957
    return km, nm

def estimate_flight_time(distance, aircraft):
    speed = AIRCRAFT_SPEEDS.get(aircraft, 800)
    return (distance / speed) + 0.5

def format_time(hours):
    mins = int(hours * 60)
    return f"{mins//60}h {mins%60}m"

def create_simbrief_url(dep, arr, aircraft):
    return (
        "https://www.simbrief.com/system/dispatch.php?"
        f"orig={urllib.parse.quote(dep)}&"
        f"dest={urllib.parse.quote(arr)}&"
        f"type={urllib.parse.quote(aircraft)}"
    )

def find_route_gui(dep, arr, aircraft):
    key = f"{dep}_{arr}_{aircraft}"
    if key in route_cache:
        return route_cache[key]

    dep_coords = get_airport_coordinates(dep)
    arr_coords = get_airport_coordinates(arr)

    km, nm = calculate_distance(dep_coords, arr_coords)
    time = format_time(estimate_flight_time(km, aircraft))

    result = {
        "departure": dep,
        "arrival": arr,
        "aircraft": aircraft,
        "distance_km": round(km, 2),
        "distance_nm": round(nm, 2),
        "flight_time": time,
        "simbrief_url": create_simbrief_url(dep, arr, aircraft)
    }

    route_cache[key] = result
    return result

# ==========================
# Main App
# ==========================
class FlightPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Planner Pro")
        self.root.geometry("600x550")

        self.header_font = font.Font(size=16, weight="bold")

        self.create_widgets()

    # --------------------------
    # Aircraft dropdown filter
    # --------------------------
    def filter_aircraft(self, event=None):
        typed = self.aircraft_var.get().upper()
        filtered = [a for a in self.aircraft_list if typed in a]
        self.aircraft_dropdown["values"] = filtered if filtered else self.aircraft_list

    def create_widgets(self):
        ttk.Label(self.root, text="Flight Planner Pro", font=self.header_font).pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Departure ICAO").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frame, text="Arrival ICAO").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(frame, text="Aircraft Type").grid(row=2, column=0, padx=5, pady=5)

        self.entry_dep = ttk.Entry(frame)
        self.entry_arr = ttk.Entry(frame)

        self.entry_dep.grid(row=0, column=1)
        self.entry_arr.grid(row=1, column=1)

        # SEARCHABLE AIRCRAFT DROPDOWN
        self.aircraft_list = sorted(AIRCRAFT_SPEEDS.keys())
        self.aircraft_var = tk.StringVar()

        self.aircraft_dropdown = ttk.Combobox(
            frame,
            textvariable=self.aircraft_var,
            values=self.aircraft_list,
            width=18
        )
        self.aircraft_dropdown.grid(row=2, column=1)
        self.aircraft_dropdown.bind("<KeyRelease>", self.filter_aircraft)
        self.aircraft_dropdown.set("A320")

        ttk.Button(
            frame, text="Calculate",
            command=self.on_calculate
        ).grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(self.root, text="", justify="left")
        self.result_label.pack(pady=10)

        self.simbrief_button = ttk.Button(
            self.root, text="Open SimBrief", state=tk.DISABLED
        )
        self.simbrief_button.pack()

    def on_calculate(self):
        dep = self.entry_dep.get().upper().strip()
        arr = self.entry_arr.get().upper().strip()
        ac = self.aircraft_var.get().upper().strip()

        if not dep or not arr or not ac:
            return

        try:
            r = find_route_gui(dep, arr, ac)
            self.result_label.config(
                text=(
                    f"Departure: {r['departure']}\n"
                    f"Arrival: {r['arrival']}\n"
                    f"Aircraft: {r['aircraft']}\n"
                    f"Distance: {r['distance_km']} km ({r['distance_nm']} nm)\n"
                    f"Flight Time: {r['flight_time']}"
                )
            )

            self.simbrief_button.config(
                state=tk.NORMAL,
                command=lambda: webbrowser.open(r["simbrief_url"])
            )
        except Exception as e:
            self.result_label.config(text=str(e))

# ==========================
# Run
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    FlightPlannerApp(root)
    root.mainloop()
