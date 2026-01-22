import streamlit as st
import requests
from random import randint

API_URL = "http://localhost:5000"

st.set_page_config(
    page_title="Sleeper Bus Booking Dashboard",
    page_icon="🚍",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align:center'>🚍 Sleeper Bus Booking System – Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

def mock_confirmation_probability(from_station, to_station, num_seats, seat_type, day_of_week):
    base = 50

    seat_factor = (4 - num_seats) * 10
    probability = base + seat_factor

    if day_of_week in ["Friday", "Saturday", "Sunday"]:
        probability -= 10
    else:
        probability += 5

    probability += randint(-10, 10)

    return max(0, min(100, probability))
try:
    stations = requests.get(f"{API_URL}/api/stations").json()["data"]
    station_dict = {s["name"]: s["id"] for s in stations}
except:
    st.error("❌ Cannot fetch stations from backend")
    station_dict = {}

try:
    meals_data = requests.get(f"{API_URL}/api/meals").json()["data"]
    meals_dict = {m["name"]: m["id"] for m in meals_data}
except:
    st.error("❌ Cannot fetch meals from backend")
    meals_dict = {}

st.subheader("📊 Live Booking Statistics")
try:
    stats = requests.get(f"{API_URL}/api/statistics").json()["data"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Bookings", stats["totalBookings"])
    col2.metric("Confirmed", stats["confirmedBookings"])
    col3.metric("Cancelled", stats["cancelledBookings"])
    col4.metric("Occupancy %", stats["occupancyRate"])
except:
    st.error("❌ Node.js backend not running on port 5000")

st.markdown("---")

st.subheader("🤖 Predict & Book Seats")

with st.form("booking_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        from_station = st.selectbox("From Station", list(station_dict.keys()))
        to_station = st.selectbox("To Station", list(station_dict.keys()))
        seat_type = st.selectbox("Seat Type", ["lower", "upper"])

    with col2:
        booking_hour = st.slider("Booking Hour", 0, 23, 12)
        num_seats = st.selectbox("Number of Seats", [1, 2, 3, 4])
        selected_meals = st.multiselect("Select Meals", list(meals_dict.keys()))

    with col3:
        advance_days = st.slider("Advance Booking Days", 0, 30, 5)
        travel_month = st.selectbox("Travel Month", list(range(1, 13)))
        day_of_week = st.selectbox(
            "Day of Travel",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
        passenger_name = st.text_input("Passenger Name", "Afzal")
        passenger_age = st.number_input("Passenger Age", 1, 120, 25)

    predict_btn = st.form_submit_button("🔮 Predict Confirmation Probability")
    book_btn = st.form_submit_button("🚍 Confirm Booking")

if from_station == to_station:
    st.warning("⚠ From and To stations cannot be the same")
    predict_btn = False
    book_btn = False

if predict_btn:
    probability = mock_confirmation_probability(
        from_station,
        to_station,
        num_seats,
        seat_type,
        day_of_week
    )

    st.markdown(
        f"""
        <div style='padding:12px;border-radius:10px;background-color:#E0F7FA;'>
            <h4>✅ Confirmation Probability: <strong>{probability}%</strong></h4>
            <p>🗓 Travel Day: <b>{day_of_week}</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if probability >= 75:
        st.success("🟢 Very high chance of confirmation")
    elif probability >= 50:
        st.warning("🟡 Moderate chance of confirmation")
    else:
        st.error("🔴 High risk of cancellation")

if book_btn:
    try:
        from_id = station_dict[from_station]
        to_id = station_dict[to_station]

        seats_response = requests.get(
            f"{API_URL}/api/seats?from={from_id}&to={to_id}"
        ).json()["data"]

        available_seats = [
            s["id"] for s in seats_response
            if s["available"] and s["type"] == seat_type
        ]

        if len(available_seats) < num_seats:
            st.error("❌ Not enough seats available")
        else:
            booking_payload = {
                "seatIds": available_seats[:num_seats],
                "fromStation": from_id,
                "toStation": to_id,
                "passenger": {
                    "name": passenger_name,
                    "age": passenger_age
                },
                "meals": [meals_dict[m] for m in selected_meals] if selected_meals else []
            }

            response = requests.post(
                f"{API_URL}/api/bookings",
                json=booking_payload
            )

            if response.status_code == 201:
                st.success("✅ Booking Confirmed!")
                st.json(response.json()["data"])
            else:
                st.error("❌ Booking failed")

    except Exception as e:
        st.error(f"❌ Backend Error: {e}")
st.markdown("---")
st.subheader("🗂 Booking History & Cancel Bookings")

try:
    bookings = requests.get(f"{API_URL}/api/bookings").json()["data"]

    if bookings:
        for b in bookings:
            with st.expander(f"Booking ID: {b['id']} | Status: {b['status']}"):
                st.write(f"👤 Passenger: {b['passenger']['name']} ({b['passenger']['age']} yrs)")
                st.write(f"💺 Seats: {', '.join(b['seatIds'])}")
                st.write(f"📍 Route: {b['fromStation']} → {b['toStation']}")
                st.write(f"💰 Fare: {b['fare']}")
                st.write(f"🕒 Created: {b['createdAt'][:19]}")

                if b["status"] == "confirmed":
                    if st.button("Cancel Booking", key=b["id"]):
                        res = requests.put(
                            f"{API_URL}/api/bookings/{b['id']}/cancel"
                        )
                        if res.json().get("success"):
                            st.success("Booking cancelled")
    else:
        st.info("No bookings found")

except Exception as e:
    st.error(f"Cannot fetch bookings: {e}")
