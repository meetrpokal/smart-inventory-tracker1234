# Smart Inventory Tracker

Smart Inventory Tracker is a full-stack web application that helps organizations manage stock, monitor expiry, detect low-stock items, and compute shortest logistics routes between Gujarat cities.

This project is designed to demonstrate strong placement-level skills in:

- Data structures and algorithms (Dijkstra shortest path)
- Backend API development (Flask)
- Frontend integration (HTML, Bootstrap, JavaScript, Chart.js)
- Authentication and session management
- Deployment awareness (Vercel + MongoDB Atlas)

## Problem Statement

Small and medium organizations often struggle to:

- Maintain accurate stock levels
- Track batch expiry dates
- Export inventory data for reporting
- Plan efficient delivery or movement routes

This project provides a single interface to solve these problems with real-time operations and analytics.

## Key Features

1. Authentication
- Organization-based login and registration
- Password hashing using Werkzeug
- Session-protected routes

2. Inventory Operations
- Add stock with optional expiry date
- Remove stock with validation
- Inventory table view with status (Valid / Expired)

3. Monitoring and Reports
- Check expired items
- Check low stock for user-defined threshold
- Export inventory as CSV report

4. Pathfinding Module
- Find shortest path between Gujarat cities
- Dijkstra algorithm implementation in Python
- Path visualization using Chart.js (cumulative distance chart)

5. Storage Strategy
- Primary: MongoDB Atlas (if MONGO_URI is configured)
- Fallback: local JSON files (inventory_data.json, users.json)

## Tech Stack

- Backend: Python, Flask
- Security: Werkzeug password hashing, Flask sessions
- Frontend: HTML, CSS, JavaScript, Bootstrap 5, Bootstrap Icons
- Visualization: Chart.js
- Database: MongoDB Atlas (PyMongo, optional), JSON fallback
- Deployment: Vercel (Python serverless)
- Additional module: C++ console implementation (Inventory.cpp)

## Project Structure

```
inventory_tracker-main/
|- app.py                  # Flask app with APIs, auth, inventory, pathfinding
|- Inventory.cpp           # Console-based C++ implementation with similar concepts
|- inventory_data.json     # Local fallback inventory storage
|- requirements.txt        # Python dependencies
|- vercel.json             # Vercel deployment config
|- templates/
|  |- login.html           # Login/register UI
|  |- index.html           # Main dashboard UI
|- README.md
```

## API Endpoints Summary

- GET / -> Dashboard (login required)
- GET, POST /login -> Login page + login API
- POST /register -> Register organization account
- GET /logout -> End session
- POST /add_stock -> Add inventory quantity (+optional expiry)
- POST /remove_stock -> Remove inventory quantity
- GET /get_inventory -> Get inventory with status
- GET /check_expiry -> List expired items
- GET /check_low_stock/<threshold> -> Low-stock items list
- GET /export_csv -> Download inventory report
- GET /get_cities -> Supported cities for routing
- POST /find_path -> Shortest path between selected cities

## Setup and Run (Local)

1. Clone the repository

```bash
git clone <your-repository-url>
cd inventory_tracker-main
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Optional: configure MongoDB Atlas

- Set environment variable MONGO_URI
- If not set, app automatically uses local JSON storage

4. Run the Flask app

```bash
python app.py
```

5. Open in browser

```text
http://127.0.0.1:5000
```

## Deployment (Vercel)

This project includes vercel.json for Python deployment.

Build config:
- Source: app.py
- Runtime: @vercel/python
- Route: all traffic redirected to app.py

For production, configure environment variables in Vercel:

- MONGO_URI
- FLASK_SECRET_KEY (recommended enhancement)



