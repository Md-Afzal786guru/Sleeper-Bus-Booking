<h1 align="center">🚍 Sleeper Bus Booking System – AI / ML Prediction Dashboard</h1>

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg" />
  <img alt="Status" src="https://img.shields.io/badge/status-active-success.svg" />
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg" />
</p>

<p align="center">
  <a href="https://github.com/Md-Afzal786guru/Sleeper-Bus-Booking">📘 Documentation</a> •
  <a href="http://localhost:8501/">✨ Demo</a>
</p>

---

## 📌 Project Overview

The **Sleeper Bus Ticket Booking System** is a full-stack web application designed to simplify **online bus ticket reservations** between **Ahmedabad → Mumbai**.

It allows users to:
- View bus routes and schedules
- Select sleeper seats
- Book tickets digitally
- View **AI-based booking confirmation probability**

The system eliminates long queues at bus stations and helps users plan their journey efficiently.

---

## ✨ Key Features

- 🚌 Bus route & station management  
- 🛏️ Sleeper seat layout visualization  
- 🎫 Real-time seat availability  
- 📊 AI/ML-based booking probability prediction (mock logic)  
- 🧠 Smart simulation using Python  
- 🌐 REST API using Node.js & Express  
- 📈 Interactive Streamlit dashboard  

---

## 🧠 AI / ML Prediction Logic (Mock)

> **Purpose:** Predict the probability of booking confirmation  

**Logic Used:**
- Probability decreases as seats get filled
- Random variation added to simulate real-world behavior
- Implemented using pure Python (no ML frameworks)
- Designed for **academic & demo purposes**

✔️ Easily replaceable with real ML models in future.

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit** – Interactive dashboard  
- **HTML / CSS** – UI components  

### Backend
- **Node.js**
- **Express.js**
- **REST APIs**

### AI / Logic
- **Python**
- **NumPy**
- **Random Simulation**

### Tools
- Git & GitHub  
- Postman  
- VS Code / PyCharm  

---

## 🧪 Backend API Test Cases

| Test Case                       | Endpoint                   | Method | Input / Query                                                                                                  | Expected Output                                                                                                  | Description                                                     |
|---------------------------------|----------------------------|--------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| Get all stations                 | `/api/stations`            | GET    | -                                                                                                             | `{ success: true, data: [stations] }`                                                                          | Returns all bus stations with IDs, names, and distances         |
| Get seats availability           | `/api/seats`               | GET    | `from=ST001&to=ST004`                                                                                         | `{ success: true, data: [seats with available & fare] }`                                                       | Each seat shows availability (`true/false`) and calculated fare |
| Get seats without `from/to`      | `/api/seats`               | GET    | -                                                                                                             | `{ success: false, message: "From & To required" }`                                                            | Should return 400 error if `from` or `to` is missing            |
| Get meals                        | `/api/meals`               | GET    | -                                                                                                             | `{ success: true, data: [meals] }`                                                                             | Returns all meals with ID, name, type, and price                |
| Create a booking                 | `/api/bookings`            | POST   | `{ seatIds:["S001","S002"], fromStation:"ST001", toStation:"ST004", passenger:{name:"John"}, meals:["M001"] }` | `{ success: true, data: booking }`                                                                             | Creates a booking, marks seats as booked, calculates total fare |
| Create booking missing fields    | `/api/bookings`            | POST   | `{ seatIds:["S001"] }`                                                                                         | `{ success: false, message: "Missing fields" }`                                                                | Should fail if required fields missing                          |
| Create booking seat unavailable  | `/api/bookings`            | POST   | Booking a seat already booked for the segment                                                                 | `{ success: false, message: "Seat S001 unavailable" }`                                                         | Prevent double booking for same segment                         |
| Cancel booking                   | `/api/bookings/:id/cancel` | PUT    | Booking ID in URL                                                                                             | `{ success: true, message: "Booking cancelled successfully" }`                                                 | Cancels booking, frees seats for that segment                   |
| Cancel non-existent booking      | `/api/bookings/:id/cancel` | PUT    | Random ID                                                                                                     | `{ success: false, message: "Booking not found" }`                                                             | Returns 404 if booking ID not found                             |
| Get all bookings                 | `/api/bookings`            | GET    | -                                                                                                             | `{ success: true, data: [bookings] }`                                                                          | Returns list of all bookings                                    |
| Check seat availability          | `/api/availability`        | GET    | `seatId=S001&from=ST001&to=ST004`                                                                             | `{ success: true, available: true/false }`                                                                     | Returns availability of a seat for a segment                    |
| Check availability invalid seat  | `/api/availability`        | GET    | `seatId=INVALID&from=ST001&to=ST004`                                                                          | `{ success: false, message: "Seat not found" }`                                                                | Should return 404 if seat ID not found                          |
| Get statistics                   | `/api/statistics`          | GET    | -                                                                                                             | `{ success: true, data: { totalBookings, confirmedBookings, cancelledBookings, occupiedSeats, occupancyRate } }` | Returns booking stats and occupancy rate                        |
| Invalid route                    | `/api/invalid`             | GET    | -                                                                                                             | `{ success: false, message: "Route not found" }`                                                               | Catch-all for undefined routes                                  |

---

## 🎨 UI/UX Prototype

You can view the full UI/UX design of the Sleeper Bus Booking project on Figma:

[Figma Prototype Link](https://www.figma.com/make/AG99tZ8CBqdEAcaPQPEiXm/App-Builder?p=f&fullscreen=1)

This prototype shows the complete flow: selecting stations, checking seat availability, choosing meals, booking confirmation, and dashboard statistics.

---

## 🗂️ Project Structure

```text
Sleeper_Bus_Booking/
│
├── backend/
│   ├── node_modules/          # Node.js dependencies
│   ├── .env                   # Environment variables
│   ├── package.json           # Backend dependencies & scripts
│   ├── package-lock.json      # Locked dependency versions
│   └── server.js              # Express server & API routes
│
├── ml-model/
│   ├── app.py                 # Streamlit dashboard (Frontend)
│   ├── prediction_model.py    # AI/ML mock prediction logic
│   ├── mock_booking_dataset.csv  # Booking simulation dataset
│   ├── mock_dataset.csv       # Additional mock data
│   ├── model_insights.json    # Prediction logic insights
│   └── requirements.txt       # Python dependencies
│
├── .gitignore                 # Ignored files/folders
├── PREDICTION_APPROACH.md     # AI/ML logic explanation
└── README.md                  # Project documentation
## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Md-Afzal786guru/Sleeper-Bus-Booking.git
cd Sleeper-Bus-Booking
2️⃣ Backend Setup (Node.js)
cd backend
npm install
npm start or npm run dev
3️⃣ Frontend Setup (Streamlit)
cd ./ml-model
pip install -r requirements.txt
streamlit run app.py

🚀 Demo
http://localhost:8501

