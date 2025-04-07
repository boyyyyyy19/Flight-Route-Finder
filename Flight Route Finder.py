import tkinter as tk
from tkinter import messagebox, ttk, font
import webbrowser
import urllib.parse
from geopy.distance import great_circle
from geopy.geocoders import Nominatim

# Cache for storing previous searches
route_cache = {}

# Function to get the coordinates of the airport from ICAO code
def get_airport_coordinates(icao_code):
    geolocator = Nominatim(user_agent="flight-planner")
    location = geolocator.geocode(f"{icao_code} airport")
    if location:
        return (location.latitude, location.longitude)
    else:
        raise Exception(f"Error: Could not find coordinates for airport {icao_code}")

# Function to calculate distance between two airports (in kilometers and nautical miles)
def calculate_distance(departure_coords, arrival_coords):
    distance_km = great_circle(departure_coords, arrival_coords).kilometers
    distance_nm = distance_km * 0.539957  # Convert kilometers to nautical miles
    return distance_km, distance_nm

# Function to estimate flight time based on the distance and aircraft type
def estimate_flight_time(distance, aircraft_type):
    aircraft_speeds = planes = {
    "B738": 840,  # Boeing 737-800
    "A320": 828,  # Airbus A320
    "B77W": 907,  # Boeing 777-200ER
    "A388": 900,  # Airbus A380
    "C172": 226,  # Cessna 172
    "A225": 850,  # Antonov An-225
    "A306": 870,  # Airbus A300-600
    "A3ST": 850,  # Airbus A310 STOL
    "A30B": 870,  # Airbus A300B
    "A30F": 870,  # Airbus A300 Freighter
    "A310": 890,  # Airbus A310
    "A318": 828,  # Airbus A318
    "A319": 828,  # Airbus A319
    "A20N": 828,  # Airbus A320neo
    "A321": 828,  # Airbus A321
    "A21N": 828,  # Airbus A321neo
    "A332": 880,  # Airbus A330-200
    "A333": 880,  # Airbus A330-300
    "A338": 880,  # Airbus A330-800
    "A339": 880,  # Airbus A330-900
    "A342": 890,  # Airbus A340-200
    "A343": 890,  # Airbus A340-300
    "A345": 890,  # Airbus A340-500
    "A346": 890,  # Airbus A340-600
    "A359": 903,  # Airbus A350-900
    "A35K": 903,  # Airbus A350-1000
    "AT43": 519,  # ATR 42-300
    "AT45": 519,  # ATR 42-500
    "AT46": 556,  # ATR 42-600
    "AT72": 510,  # ATR 72-500
    "AT73": 510,  # ATR 72-600
    "AT75": 510,  # ATR 75
    "AT76": 556,  # ATR 76
    "B190": 537,  # Beechcraft 1900
    "B350": 578,  # Beechcraft Super King Air 350
    "B461": 730,  # Boeing 461
    "B462": 730,  # Boeing 462
    "B463": 730,  # Boeing 463
    "B703": 966,  # Boeing 707-320
    "B712": 891,  # Boeing 717-200
    "B721": 965,  # Boeing 727-100
    "B722": 965,  # Boeing 727-200
    "B732": 940,  # Boeing 737-200
    "B733": 885,  # Boeing 737-300
    "B734": 885,  # Boeing 737-400
    "B735": 885,  # Boeing 737-500
    "B736": 833,  # Boeing 737-600
    "B737": 833,  # Boeing 737-700
    "BBJ1": 833,  # Boeing 737 Business Jet 1
    "BBJ2": 833,  # Boeing 737 Business Jet 2
    "B38M": 839,  # Boeing 737 MAX 8
    "B739": 833,  # Boeing 737-900
    "BBJ3": 833,  # Boeing 737 Business Jet 3
    "B742": 939,  # Boeing 747-200
    "B744": 920,  # Boeing 747-400
    "B74F": 920,  # Boeing 747-400 Freighter
    "B748": 918,  # Boeing 747-8
    "B48F": 918,  # Boeing 748 Freighter
    "B752": 876,  # Boeing 757-200
    "B75F": 876,  # Boeing 757-200 Freighter
    "B753": 876,  # Boeing 757-300
    "B762": 870,  # Boeing 767-200
    "B763": 870,  # Boeing 767-300
    "B76F": 870,  # Boeing 767 Freighter
    "B764": 870,  # Boeing 767-400
    "B772": 907,  # Boeing 777-200
    "B77F": 907,  # Boeing 777 Freighter
    "B77L": 907,  # Boeing 777-200LR
    "B788": 902,  # Boeing 787-8
    "B789": 902,  # Boeing 787-9
    "B78X": 902,  # Boeing 787-10
    "BCS1": 829,  # Bombardier CS100
    "BCS3": 829,  # Bombardier CS300
    "BE20": 537,  # Beechcraft Super King Air 200
    "BE24": 296,  # Beechcraft Musketeer
    "BE36": 333,  # Beechcraft Bonanza A36
    "BE58": 370,  # Beechcraft Baron 58
    "BE60": 435,  # Beechcraft King Air 60
    "BE6G": 435,  # Beechcraft King Air 65
    "B60T": 435,  # Beechcraft King Air 60T
    "C130": 593,  # Lockheed C-130 Hercules
    "C160": 513,  # Transall C-160
    "C17": 926,  # Boeing C-17 Globemaster III
    "C182": 278,  # Cessna 182 Skylane
    "R182": 278,  # Cessna 182 RG
    "C208": 344,  # Cessna 208 Caravan
    "C25A": 778,  # Cessna 525 Citation Jet
    "C25B": 778,  # Cessna 525B Citation Jet Bravo
    "C25C": 833,  # Cessna 525C Citation Jet CJ3
    "C310": 370,  # Cessna 310
    "C337": 324,  # Cessna 337 Skymaster
    "C404": 407,  # Cessna 404 Titan
    "C408": 407,  # Cessna 408 SkyCourier
    "C414": 407,  # Cessna 414 Chancellor
    "C46": 346,  # Curtiss C-46 Commando
    "C510": 741,  # Cessna Citation Mustang
    "C550": 780,  # Cessna Citation II
    "C56X": 890,  # Cessna Citation X
    "C680": 890,  # Cessna Citation Sovereign
    "C700": 890,  # Cessna Citation Latitude
    "C750": 978,  # Cessna Citation X+
    "CL30": 850,  # Bombardier Challenger 300
    "CL35": 850,  # Bombardier Challenger 350
    "CL60": 850,  # Bombardier Challenger 600
    "CONI": 483,  # Concorde
    "CONS": 483,  # Concorde supersonic
    "CRJ2": 859,  # Bombardier CRJ200
    "CRJ5": 859,  # Bombardier CRJ500
    "CRJ7": 870,  # Bombardier CRJ700
    "CRJ9": 870,  # Bombardier CRJ900
    "CRJX": 870,  # Bombardier CRJ-X
    "D328": 611,  # Dornier 328
    "DA42": 356,  # Diamond DA42 Twin Star
    "DA62": 378,  # Diamond DA62
    "DC10": 900,  # McDonnell Douglas DC-10
    "DC3": 287,  # Douglas DC-3
    "DC6": 509,  # Douglas DC-6
    "DC85": 900,  # McDonnell Douglas DC-85
    "DC86": 900,  # McDonnell Douglas DC-86
    "DH8A": 500,  # De Havilland Dash 8-100
    "DH8B": 500,  # De Havilland Dash 8-200
    "DH8C": 500,  # De Havilland Dash 8-300
    "DH8D": 667,  # De Havilland Dash 8-400
    "DHC2": 203,  # De Havilland Beaver
    "DHC6": 315,  # De Havilland Twin Otter
    "DHC7": 463,  # De Havilland Dash 7
    "E135": 833,  # Embraer ERJ-135
    "E13L": 833,  # Embraer ERJ-145LR
    "E140": 833,  # Embraer ERJ-140
    "E145": 833,  # Embraer ERJ-145
    "E170": 870,  # Embraer E170
    "E175": 870,  # Embraer E175
    "E190": 870,  # Embraer E190
    "E19L": 870,  # Embraer E190LR
    "E195": 870,  # Embraer E195
    "E50P": 750,  # Embraer Phenom 500
    "E55P": 833,  # Embraer Phenom 550
    "EA50": 630,  # Embraer Phenom 100
    "EVAL": 500,  # Embraer Evolution
    "F28": 843,  # Fokker 28
    "F50": 532,  # Fokker 50
    "F70": 843,  # Fokker 70
    "F100": 843,  # Fokker 100
    "FA50": 852,  # Falcon 50
    "GLF4": 870,  # Gulfstream G4
    "H25B": 843,  # Hawker 800
    "HDJT": 780,  # HondaJet
    "IL76": 780,  # Ilyushin Il-76
    "JS41": 565,  # Jetstream 41
    "KODI": 296,  # Kodiak 100
    "L101": 965,  # Lockheed L-1011 TriStar
    "L410": 388,  # Let L-410 Turbolet
    "LJ25": 852,  # Learjet 25
    "LJ35": 852,  # Learjet 35
    "LJ45": 860,  # Learjet 45
    "MD11": 940,  # McDonnell Douglas MD-11
    "MD1F": 940,  # McDonnell Douglas MD-1F
    "MD82": 890,  # McDonnell Douglas MD-82
    "MD83": 890,  # McDonnell Douglas MD-83
    "MD88": 890,  # McDonnell Douglas MD-88
    "MD90": 890,  # McDonnell Douglas MD-90
    "MU2": 556,  # Mitsubishi MU-2
    "P06T": 287,  # Piper Aerostar 600
    "P180": 741,  # Piaggio P180 Avanti
    "P212": 315,  # Piper Navajo Chieftain
    "P46T": 500,  # Piper Malibu Mirage
    "M600": 500,  # Piper M600
    "PA24": 300,  # Piper Comanche
    "PA34": 300,  # Piper Seneca
    "PA44": 300,  # Piper Seminole
    "PC12": 528,  # Pilatus PC-12
    "RJ70": 843,  # Saab 340
    "RJ85": 843,  # Saab 85
    "RJ1H": 843,  # Saab 340
    "SB20": 556,  # Short 360
    "SF34": 528,  # Saab 340
    "SF50": 611,  # Cirrus SF50 Vision Jet
    "SH33": 407,  # Short 330
    "SH36": 407,  # Short 360
    "SR22": 333,  # Cirrus SR22
    "SR2T": 333,  # Cirrus SR20
    "SU95": 870,  # Sukhoi Superjet 100
    "SW4": 463,  # Swearingen Metro
    "T134": 850,  # Tupolev Tu-134
    "T154": 850,  # Tupolev Tu-154
    "T204": 880,  # Tupolev Tu-204
    "TBM8": 593,  # TBM 850
    "TBM9": 611,  # TBM 900
    "VC10": 935,  # Vickers VC10
    "YK40": 760   # Yakovlev Yak-40
}


    default_speed = 800  # Default speed in km/h
    speed = aircraft_speeds.get(aircraft_type, default_speed)
    flight_time = distance / speed  # Time in hours
    flight_time += 0.5  # Add 30 minutes for takeoff and landing
    return flight_time

# Function to format flight time in hours and minutes
def format_time(hours):
    total_minutes = int(hours * 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h {minutes}m"

# Function to create a SimBrief URL for flight planning
def create_simbrief_url(departure, arrival, aircraft):
    base_url = "https://www.simbrief.com/system/dispatch.php"
    departure = urllib.parse.quote(departure)
    arrival = urllib.parse.quote(arrival)
    aircraft = urllib.parse.quote(aircraft)
    params = f"?orig={departure}&dest={arrival}&type={aircraft}"
    return base_url + params

# Function that brings everything together and returns the results
def find_route_gui(departure, arrival, aircraft):
    try:
        # Check if this route is already in the cache
        cache_key = f"{departure}_{arrival}_{aircraft}"
        if cache_key in route_cache:
            return route_cache[cache_key]
            
        # Validate ICAO codes
        if len(departure) != 4 or len(arrival) != 4 or len(aircraft) < 2 or len(aircraft) > 4:
            raise ValueError("Invalid ICAO code(s)")

        # Get coordinates of the airports
        departure_coords = get_airport_coordinates(departure)
        arrival_coords = get_airport_coordinates(arrival)

        # Calculate distance between the airports
        distance_km, distance_nm = calculate_distance(departure_coords, arrival_coords)

        # Estimate flight time
        flight_time = estimate_flight_time(distance_km, aircraft)

        # Format results
        flight_time_str = format_time(flight_time)

        # Create SimBrief URL
        url = create_simbrief_url(departure, arrival, aircraft)

        results = {
            "departure": departure,
            "arrival": arrival,
            "aircraft": aircraft,
            "distance_km": round(distance_km, 2),
            "distance_nm": round(distance_nm, 2),
            "flight_time": flight_time_str,
            "simbrief_url": url
        }

        # Store the results in cache
        route_cache[cache_key] = results

        return results
    except Exception as e:
        return {"error": str(e)}

# Tooltip class for showing help text
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Create tooltip window
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(
            self.tooltip, 
            text=self.text, 
            background="#ffffe0", 
            relief="solid", 
            borderwidth=1,
            wraplength=250,
            justify="left",
            padding=(5, 3)
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class FlightPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Planner Pro")
        self.root.geometry("600x550")
        self.root.resizable(True, True)
        self.root.minsize(500, 450)

        # Set app colors
        self.bg_color = "#f0f0f0"
        self.header_bg = "#2c3e50"
        self.header_fg = "white"
        self.accent_color = "#3498db"
        self.secondary_color = "#ecf0f1"
        self.button_color = "#2980b9"
        self.button_fg = "white"

        # Configure root window
        self.root.configure(bg=self.bg_color)
        self.root.option_add("*Font", "Helvetica 10")

        # Initialize custom fonts
        self.header_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=10)
        self.result_font = font.Font(family="Helvetica", size=11)
        self.button_font = font.Font(family="Helvetica", size=10, weight="bold")

        # Setup styles for ttk widgets
        self.setup_styles()

        # Create UI components
        self.create_widgets()

        # Center the window
        self.center_window()

    def setup_styles(self):
        # Create ttk styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Header.TFrame", background=self.header_bg)
        self.style.configure("Content.TFrame", background=self.bg_color)
        self.style.configure("Results.TFrame", background=self.secondary_color, relief="ridge")
        
        self.style.configure("TLabel", background=self.bg_color, font=self.label_font)
        self.style.configure("Header.TLabel", 
                             background=self.header_bg, 
                             foreground=self.header_fg, 
                             font=self.header_font)

        self.style.configure("TEntry", padding=5)
        self.style.map("TButton",
                      foreground=[('pressed', self.button_fg), ('active', self.button_fg)],
                      background=[('pressed', '!disabled', self.button_color), 
                                 ('active', self.accent_color)])

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def update_status(self, message, is_error=False):
        # Update status bar
        self.status_bar.configure(text=message)
        self.root.update_idletasks()

    def display_results(self, results):
        # Update result labels with fetched data
        self.departure_value.config(text=results['departure'])
        self.arrival_value.config(text=results['arrival'])
        self.aircraft_value.config(text=results['aircraft'])
        self.distance_value.config(text=f"{results['distance_km']} km ({results['distance_nm']} nm)")
        self.time_value.config(text=results['flight_time'])
        
        # Enable and configure the SimBrief button
        self.simbrief_button.config(
            state=tk.NORMAL, 
            command=lambda: webbrowser.open(results["simbrief_url"])
        )
        
        # Show the results frame
        if not self.results_frame.winfo_ismapped():
            self.results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

    def on_calculate_button_click(self):
        # Get user input from entry fields
        departure = self.entry_departure.get().strip().upper()
        arrival = self.entry_arrival.get().strip().upper()
        aircraft = self.entry_aircraft.get().strip().upper()

        # Check for empty fields
        if not departure or not arrival or not aircraft:
            self.update_status("Please fill in all fields.", is_error=True)
            return

        # Call find_route_gui function
        results = find_route_gui(departure, arrival, aircraft)

        if "error" in results:
            self.update_status(results["error"], is_error=True)
        else:
            self.update_status("Route found successfully!", is_error=False)
            self.display_results(results)
            
    def create_widgets(self):
        # Create header frame
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=10)

        header_label = ttk.Label(header_frame, text="Flight Planner Pro", style="Header.TLabel")
        header_label.pack(padx=10, pady=10)

        # Create input frame
        input_frame = ttk.Frame(self.root, style="Content.TFrame")
        input_frame.pack(fill=tk.X, padx=20)

        departure_label = ttk.Label(input_frame, text="Departure ICAO:")
        departure_label.grid(row=0, column=0, padx=5, pady=5)
        self.entry_departure = ttk.Entry(input_frame)
        self.entry_departure.grid(row=0, column=1, padx=5, pady=5)

        arrival_label = ttk.Label(input_frame, text="Arrival ICAO:")
        arrival_label.grid(row=1, column=0, padx=5, pady=5)
        self.entry_arrival = ttk.Entry(input_frame)
        self.entry_arrival.grid(row=1, column=1, padx=5, pady=5)

        aircraft_label = ttk.Label(input_frame, text="Aircraft Type (ICAO):")
        aircraft_label.grid(row=2, column=0, padx=5, pady=5)
        self.entry_aircraft = ttk.Entry(input_frame)
        self.entry_aircraft.grid(row=2, column=1, padx=5, pady=5)

        calculate_button = ttk.Button(input_frame, text="Calculate", style="TButton", command=self.on_calculate_button_click)
        calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Create results frame
        self.results_frame = ttk.Frame(self.root, style="Results.TFrame")
        
        self.departure_label = ttk.Label(self.results_frame, text="Departure ICAO:")
        self.departure_label.grid(row=0, column=0, padx=10, pady=5)
        self.departure_value = ttk.Label(self.results_frame, text="N/A")
        self.departure_value.grid(row=0, column=1, padx=10, pady=5)

        self.arrival_label = ttk.Label(self.results_frame, text="Arrival ICAO:")
        self.arrival_label.grid(row=1, column=0, padx=10, pady=5)
        self.arrival_value = ttk.Label(self.results_frame, text="N/A")
        self.arrival_value.grid(row=1, column=1, padx=10, pady=5)

        self.aircraft_label = ttk.Label(self.results_frame, text="Aircraft Type:")
        self.aircraft_label.grid(row=2, column=0, padx=10, pady=5)
        self.aircraft_value = ttk.Label(self.results_frame, text="N/A")
        self.aircraft_value.grid(row=2, column=1, padx=10, pady=5)

        self.distance_label = ttk.Label(self.results_frame, text="Distance (km):")
        self.distance_label.grid(row=3, column=0, padx=10, pady=5)
        self.distance_value = ttk.Label(self.results_frame, text="N/A")
        self.distance_value.grid(row=3, column=1, padx=10, pady=5)

        self.time_label = ttk.Label(self.results_frame, text="Flight Time:")
        self.time_label.grid(row=4, column=0, padx=10, pady=5)
        self.time_value = ttk.Label(self.results_frame, text="N/A")
        self.time_value.grid(row=4, column=1, padx=10, pady=5)

        self.simbrief_button = ttk.Button(self.results_frame, text="Open SimBrief Route", state=tk.DISABLED)
        self.simbrief_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Status bar
        self.status_bar = ttk.Label(self.root, text="Welcome to Flight Planner Pro", anchor="w", relief="sunken", padding=5)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

# Main code to start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FlightPlannerApp(root)
    root.mainloop()
