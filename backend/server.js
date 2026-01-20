require('dotenv').config();

const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

/* ---------------- MOCK DATABASE ---------------- */

const database = {
  bus: {
    id: 'BUS001',
    name: 'Sleeper Express',
    route: 'Ahmedabad → Mumbai',
    totalSeats: 40,
    layout: 'sleeper',
  },
  stations: [
    { id: 'ST001', name: 'Ahmedabad', arrivalTime: null, departureTime: '22:00', distance: 0 },
    { id: 'ST002', name: 'Vadodara', arrivalTime: '00:30', departureTime: '00:45', distance: 110 },
    { id: 'ST003', name: 'Surat', arrivalTime: '03:00', departureTime: '03:15', distance: 260 },
    { id: 'ST004', name: 'Mumbai', arrivalTime: '07:00', departureTime: null, distance: 530 }
  ],
  seats: [],
  bookings: [],
  meals: [
    { id: 'M001', name: 'Veg Thali', type: 'veg', price: 150 },
    { id: 'M002', name: 'Paneer Combo', type: 'veg', price: 180 },
    { id: 'M003', name: 'Chicken Biryani', type: 'non-veg', price: 220 },
    { id: 'M004', name: 'Jain Thali', type: 'jain', price: 160 }
  ]
};

/* ---------------- HELPERS ---------------- */

function generateSeats(count) {
  const seats = [];
  const types = ['lower', 'upper', 'lower'];

  for (let i = 1; i <= count; i++) {
    seats.push({
      id: `S${String(i).padStart(3, '0')}`,
      number: i,
      type: types[(i - 1) % 3],
      isBooked: false,
      bookedSegments: []
    });
  }
  return seats;
}

database.seats = generateSeats(40);

function isSeatAvailable(seat, fromStation, toStation) {
  if (!seat.isBooked) return true;

  const fromIndex = database.stations.findIndex(s => s.id === fromStation);
  const toIndex = database.stations.findIndex(s => s.id === toStation);

  for (const seg of seat.bookedSegments) {
    const segFrom = database.stations.findIndex(s => s.id === seg.from);
    const segTo = database.stations.findIndex(s => s.id === seg.to);

    if (!(toIndex <= segFrom || fromIndex >= segTo)) {
      return false;
    }
  }
  return true;
}

function calculateFare(fromStation, toStation) {
  const from = database.stations.find(s => s.id === fromStation);
  const to = database.stations.find(s => s.id === toStation);
  if (!from || !to) return 0;

  return Math.round(Math.abs(to.distance - from.distance) * 0.8);
}

/* ---------------- ROUTES ---------------- */

app.get('/api/stations', (req, res) => {
  res.json({ success: true, data: database.stations });
});

app.get('/api/seats', (req, res) => {
  const { from, to } = req.query;

  if (!from || !to) {
    return res.status(400).json({ success: false, message: 'From & To required' });
  }

  const seats = database.seats.map(seat => ({
    ...seat,
    available: isSeatAvailable(seat, from, to),
    fare: calculateFare(from, to)
  }));

  res.json({ success: true, data: seats });
});

app.get('/api/meals', (req, res) => {
  res.json({ success: true, data: database.meals });
});

app.post('/api/bookings', (req, res) => {
  const { seatIds, fromStation, toStation, passenger, meals } = req.body;

  if (!seatIds || !fromStation || !toStation || !passenger) {
    return res.status(400).json({ success: false, message: 'Missing fields' });
  }

  const unavailable = seatIds.filter(id => {
    const seat = database.seats.find(s => s.id === id);
    return !seat || !isSeatAvailable(seat, fromStation, toStation);
  });

  if (unavailable.length) {
    return res.status(400).json({ success: false, message: 'Seats unavailable', unavailable });
  }

  const booking = {
    id: `BK${Date.now()}`,
    seatIds,
    fromStation,
    toStation,
    passenger,
    meals: meals || [],
    status: 'confirmed',
    bookingTime: new Date().toISOString()
  };

  seatIds.forEach(id => {
    const seat = database.seats.find(s => s.id === id);
    seat.isBooked = true;
    seat.bookedSegments.push({ from: fromStation, to: toStation });
  });

  database.bookings.push(booking);
  res.status(201).json({ success: true, data: booking });
});

/* ---------------- STATISTICS ROUTE (NEW) ---------------- */

app.get('/api/statistics', (req, res) => {
  const totalBookings = database.bookings.length;
  const confirmed = database.bookings.filter(b => b.status === 'confirmed').length;
  const cancelled = database.bookings.filter(b => b.status === 'cancelled').length;
  const occupiedSeats = database.seats.filter(s => s.isBooked).length;

  res.json({
    success: true,
    data: {
      totalBookings,
      confirmedBookings: confirmed,
      cancelledBookings: cancelled,
      occupancyRate: ((occupiedSeats / database.seats.length) * 100).toFixed(2)
    }
  });
});

/* ---------------- SERVER ---------------- */

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚌 Sleeper Bus Booking API running on port ${PORT}`);
});
