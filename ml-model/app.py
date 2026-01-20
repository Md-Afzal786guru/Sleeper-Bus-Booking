import streamlit as st
import requests
from prediction_model import BookingPredictionModel

API_URL = "http://localhost:5000"

st.set_page_config(
    page_title="Sleeper Bus Booking",
    page_icon="🚍",   # Emoji icon
    layout="wide"
)

st.title("🚍 Sleeper Bus Booking – AI / ML Prediction Dashboard")

@st.cache_resource
def load_model():
    model = BookingPredictionModel()
    data = model.generate_mock_dataset(1000)
    model.train(data)
    return model

model = load_model()

# ---------------- NODE API DATA ----------------
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

# ---------------- PREDICTION FORM ----------------
st.divider()
st.subheader("🤖 Booking Confirmation Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    day_of_week = st.selectbox(
        "Day of Week",
        ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    )
    route_segment = st.selectbox(
        "Route Segment",
        ["Ahmedabad-Vadodara","Ahmedabad-Surat","Ahmedabad-Mumbai",
         "Vadodara-Mumbai","Surat-Mumbai"]
    )
    seat_type = st.selectbox("Seat Type", ["lower", "upper"])

with col2:
    booking_hour = st.slider("Booking Hour", 0, 23, 12)
    num_seats = st.selectbox("Number of Seats", [1,2,3,4])
    has_meal = st.selectbox("Meal Included?", [0,1], format_func=lambda x: "Yes" if x else "No")

with col3:
    advance_days = st.slider("Advance Booking Days", 0, 30, 5)
    month = st.selectbox("Travel Month", list(range(1,13)))

if st.button("🔮 Predict Confirmation Probability"):
    booking_data = {
        "day_of_week": day_of_week,
        "booking_hour": booking_hour,
        "route_segment": route_segment,
        "seat_type": seat_type,
        "num_seats": num_seats,
        "has_meal": has_meal,
        "advance_days": advance_days,
        "month": month
    }

    probability = model.predict_confirmation_probability(booking_data)

    st.success(f"✅ Confirmation Probability: **{probability}%**")

    if probability >= 75:
        st.info("🟢 Very high chance of confirmation")
    elif probability >= 50:
        st.warning("🟡 Moderate chance of confirmation")
    else:
        st.error("🔴 High risk of cancellation")
