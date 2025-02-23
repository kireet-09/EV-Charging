EVie - SMART EV CHARGING RESERVATION SYSTEM

BY: Kireeti Samanthapudi and Keerthi Nori
For ‘Hack The Future: Solve today’s problems with tomorrow’s Technology’ Hackathon

## Features (Current & Future)

### Implemented Features (MVP):
1️⃣ **User Authentication**
   - Secure Sign Up/Login for EV owners & charging station admins.
   - Authentication handled using Django’s built-in system.

2️⃣ **Slot Booking & Management**
   - Users can reserve charging slots for a specific time.
   - Admins can set station availability & manage reservations.

3️⃣ **Email Notification System**
   - Automatic email notifications for booking confirmations and cancellations.
   - Uses Gmail SMTP for secure email delivery.

### Planned Features (Future Enhancements):
3️⃣ **Charging Station Finder (Coming Soon 🚧)**
   - Interactive Google Maps API / Leaflet.js for locating nearby charging stations.
   - Filters for charging speed, price, and availability.

4️⃣ **Payment & Billing System (Coming Soon 💳)**
   - Stripe/Razorpay integration for online payments.
   - Invoice generation & transaction tracking for users.

5️⃣ **Smart Charging Optimization (Future Development 🤖⚡)**
   - AI-based demand prediction for efficient energy distribution.
   - Load balancing to optimize charging sessions.

## Relevance to Hackathon Theme
Our Project is aligned with the Theme of the Hackathon: **'Autonomous Transport: Rethinking Mobility for a Sustainable Future'**

01 **Sustainability** - Supports electric vehicle adoption
02 **Traffic Optimization** - Reduces congestion at charging stations
03 **Safety & Accessibility** - Increases accessibility for EV users
04 **Scalability** - Can integrate with smart city infrastructure

## Tech Stack Used:
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Django & Django REST Framework
- **Database:** MySQL or SQLite
- **APIs:** Google Maps API (for location search), Payment Gateway (Stripe/Razorpay)

## Project Setup:
### Tools Required:
- VS Code / PyCharm for coding
- Postman for API testing
- Git & GitHub for version control
- Virtual Environment for dependency management

### Initialize the Django Project:
```sh
pip install django djangorestframework
```
```sh
django-admin startproject ev_charging_system
cd ev_charging_system
python manage.py startapp reservations
```
- Configure settings (database, installed apps, middleware, etc.)

## Project Development:
### Backend Development:
1️⃣ **Implement User Authentication**
   - Use Django’s built-in authentication system.
   - Create user models for EV owners and charging station admins.
   - Use Django REST Framework for API-based login/signup.

2️⃣ **Develop the Slot Booking System**
   - Create models for Charging Stations, Slots, and Bookings.
   - Define API endpoints for:
     - Viewing available stations.
     - Booking a slot.
     - Canceling a reservation.
     - Fetching booking history.

3️⃣ **Implement Real-Time Availability Updates**
   - Use WebSockets or periodic API polling.
   - Each station updates available slots dynamically.

4️⃣ **Email Notification System**
   - Automatic email confirmation for bookings & cancellations.
   - Uses Gmail SMTP settings.
   - Django’s `send_mail` function for seamless notifications.

5️⃣ **Payment Gateway Integration**
   - Integrate Stripe/Razorpay API for online payments.
   - Store transaction details in the database.

### Frontend Development:
1️⃣ **Create a Responsive UI**
   - Design user-friendly pages: Home, Station Finder, Booking, Payments, Dashboard.
   - Use Bootstrap or TailwindCSS for styling.

2️⃣ **Integrate Google Maps API / Leaflet.js**
   - Display charging stations on an interactive map.
   - Allow users to search by location.

3️⃣ **Connect Frontend with Backend APIs**
   - Use JavaScript (AJAX/Fetch API) to send & receive data.
   - Implement error handling for failed bookings/payments.

## API Endpoints
- `GET /reservation/` – View available slots
- `POST /reservation/` – Book a slot
- `POST /cancel-reservation/<id>/` – Cancel a reservation

## Folder Structure
```
/ev_charging
│── ev_charging/       # Main project folder
│── reservations/      # Reservation app (models, views, etc.)
│── templates/         # Frontend templates
│── static/            # CSS, JS, images
│── db.sqlite3         # Database file
│── manage.py          # Django management script
```

## Conclusion
### Key Takeaways:
- The **Smart EV Charging Reservation System** solves major pain points for EV owners.
- It provides real-time availability, location-based search, and seamless booking & payment.
- Aligns with sustainability and smart city goals for a greener future.

### Impact on Sustainable Mobility:
- **Supports widespread EV adoption** by making charging more accessible.
- **Reduces traffic congestion** at charging stations.
- **Ensures efficient energy use** with demand-based charging.

---
🚗⚡ **Thank you!**

