# Traffic-Congestion-Predictor


## 🚦 Traffic Congestion Predictor

**Traffic Congestion Predictor** is a Streamlit-based web application that helps users find the **fastest route** between two locations by considering **real-time or simulated traffic conditions**.
It visualizes the road network as a graph and uses **Dijkstra’s algorithm** to compute the **shortest travel time path**.


### 🧠 Key Features

* 📍 **Interactive Route Selection** – Choose source and destination locations dynamically.
* ⚡ **Fastest Route Prediction** – Uses Dijkstra’s algorithm to find the optimal route.
* 🗺️ **Graph Visualization** – Displays the road network with nodes, edges, and weights (travel time).
* 🚧 **Traffic Simulation Editor** – Allows users to edit edge weights to simulate traffic congestion.
* 🔁 **Real-time Updates** – Automatically updates routes and visuals after traffic modifications.
* 🧮 **Metrics Display** – Shows total travel time and number of stops.

---

### 🧩 Tech Stack

| Component         | Technology               |
| ----------------- | ------------------------ |
| Frontend          | Streamlit                |
| Backend Logic     | Python                   |
| Graph Computation | NetworkX                 |
| Visualization     | Matplotlib               |
| Algorithm         | Dijkstra’s Shortest Path |

---

### 📁 Project Structure

```
Traffic-Congestion-Predictor/
│
├── app.py                # Main Streamlit application
├── data_loader.py        # Functions to load and manage road network data
├── utils.py              # Utility functions for path calculation & formatting
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

---

### ⚙️ Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/<your-username>/Traffic-Congestion-Predictor.git
   cd Traffic-Congestion-Predictor
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   * **Windows:**

     ```bash
     venv\Scripts\activate
     ```
   * **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**

   ```bash
   streamlit run app.py
   ```

---

### 🧭 How It Works

1. The app loads a **road network graph** from the `data_loader` module.
2. Users select a **source** and **destination** location.
3. The app runs **Dijkstra’s algorithm** to find the shortest path based on travel time (edge weights).
4. The result is **visualized** using NetworkX and Matplotlib.
5. Users can simulate **traffic congestion** by editing edge weights in the **Traffic Editor**.

---



### 🧠 Future Enhancements

* 📡 Integrate real-time traffic APIs (like Google Maps or OpenStreetMap).
* 📱 Build a responsive web version using React + Flask backend.
* 🧭 Add A* search for faster route computation.
* 📊 Add congestion heatmaps and route comparison.

---



This project is licensed under the **MIT License** — feel free to use, modify, and distribute with credit.

---



