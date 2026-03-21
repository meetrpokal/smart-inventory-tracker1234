# Smart Inventory Tracker

A full-stack inventory management system with a web interface, MongoDB cloud storage, and pathfinding capabilities for Gujarat cities. Built with Python Flask and a C++ reference backend.

## Features

- **Inventory Management**
  - Add/Remove stock with optional expiry date tracking
  - Low stock alerts (configurable threshold)
  - Expired items detection
  - **CSV export**: download your full inventory as a `.csv` file containing Product, Quantity, Expiry date, and Status columns

- **User Accounts**
  - Register / Login with hashed passwords
  - Per-user inventory stored in MongoDB (with local JSON fallback)

- **Advanced Analytics**
  - Real-time inventory tracking
  - Demand spike detection
  - FIFO expiry management

- **Pathfinding System**
  - Shortest path calculation between Gujarat cities using Dijkstra's algorithm
  - Interactive web visualization

## CSV Export

The `/export_csv` route generates a downloadable `inventory_report.csv` file for the logged-in user's current inventory. The CSV contains four columns:

| Column   | Description                                      |
|----------|--------------------------------------------------|
| Product  | Name of the inventory item                       |
| Quantity | Current quantity in stock                        |
| Expiry   | Expiry date (`YYYY-MM-DD`) or `N/A` if not set   |
| Status   | `Valid` or `Expired(<qty>)` for expired batches  |

The file is generated entirely in memory — no temporary files are written to disk — making it compatible with read-only deployment environments such as Vercel.

## Tech Stack

- **Backend**: Python Flask (Web API), C++ (reference core logic)
- **Database**: MongoDB Atlas via `pymongo` (falls back to local `inventory_data.json`)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Visualization**: Chart.js
- **Deployment**: Vercel

## Project Structure

```
smart-inventory-tracker/
├── Inventory.cpp         # C++ reference inventory system
├── app.py                # Flask web application
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment config
├── templates/
│   ├── index.html        # Main web interface
│   └── login.html        # Login / Register page
├── inventory_data.json   # Local JSON fallback storage
└── README.md
```

## Prerequisites

- Python 3.8+
- A [MongoDB Atlas](https://www.mongodb.com/atlas) cluster (free tier works fine) **or** use the local JSON fallback
- (Optional) C++ compiler (`g++`) to rebuild `inventory.exe`

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/meetrpokal/smart-inventory-tracker1234.git
   cd smart-inventory-tracker1234
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   This installs Flask, Werkzeug, Jinja2, `pymongo`, and `dnspython`.

3. **Configure MongoDB (optional)**

   By default the app connects to a demo Atlas cluster. To use your own cluster, set the `MONGO_URI` environment variable before starting the server:
   ```bash
   export MONGO_URI="mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?appName=<app>"
   ```
   If `MONGO_URI` is not set or the connection fails, the app automatically falls back to local `inventory_data.json` storage.

   > **Vercel deployment**: add `MONGO_URI` as an Environment Variable in your Vercel project settings.

## Usage

### Running the Web Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open browser and navigate to**
   ```
   http://localhost:5000
   ```

3. **Register** a new account (or log in), then use the dashboard to:
   - Add / remove stock items
   - Set expiry dates on batches
   - Check low-stock and expiry alerts
   - **Export inventory to CSV** using the *Export CSV* button

