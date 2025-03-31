🚀 EVie - SMART EV CHARGING RESERVATION SYSTEM

By: Kireeti Samanthapudi and Keerthi NoriFor the Hackathon: "Hack The Future: Solve today’s problems with tomorrow’s technology"

✅ Features (Current & Future)

🔥 Implemented Features (MVP)

1️⃣ User Authentication

Secure Sign Up/Login for EV owners and charging station admins.

Authentication handled using Django’s built-in system.

Users are redirected to a personalized dashboard after login.

2️⃣ Slot Booking & Management

Users can reserve charging slots for a specific time.

Admins can manage stations, set availability, and oversee reservations.

Dynamic slot loading based on the selected station.

3️⃣ AI-Powered Demand Prediction

Integrated AI model for demand prediction.

Displays estimated wait time and traffic status for each station.

Real-time updates for smarter slot booking decisions.

4️⃣ Email Notification System

Automatic email notifications for booking confirmations and cancellations.

Uses Gmail SMTP for secure email delivery.

5️⃣ Dynamic Carpooling Feature

Users can create or join carpools with other EV users.

Displays carpool details with departure time, destination, and members.

6️⃣ Interactive Dashboard

Upon login, users are directed to a dashboard with:

Navigation buttons for reservations, carpooling, and station search.

AI predictions and reservation management.

Dark mode toggle for personalized viewing.

7️⃣ Real-Time Slot Updates

Slot availability automatically updates when a reservation is made or canceled.

Prevents duplicate or incorrect bookings.

🚀 Planned Features (Future Enhancements)

✅ 1. Charging Station Finder (Coming Soon 🚧)

Interactive Google Maps API / Leaflet.js for locating nearby charging stations.

Filters for charging speed, price, and availability.

✅ 2. Payment & Billing System (Coming Soon 💳)

Stripe/Razorpay integration for online payments.

Invoice generation & transaction tracking for users.

✅ 3. Smart Charging Optimization (Future Development 🤖⚡)

AI-based demand prediction for efficient energy distribution.

Load balancing to optimize charging sessions and reduce energy waste.

🌍 Relevance to Hackathon Theme

Our project aligns with the "Autonomous Transport: Rethinking Mobility for a Sustainable Future" theme by offering:

♻️ Sustainability: Supports electric vehicle adoption and eco-friendly transport.

🚦 Traffic Optimization: Reduces congestion at charging stations.

✅ Safety & Accessibility: Increases accessibility and convenience for EV users.

🔥 Scalability: Can integrate with smart city infrastructure.

⚙️ Tech Stack Used

✅ Frontend:

HTML, CSS, JavaScript

Bootstrap for styling

✅ Backend:

Django & Django REST Framework

Python for AI model integration

✅ Database:

MySQL or SQLite for reservation data management

✅ APIs & Services:

AI model for demand prediction

Gmail SMTP for email notifications

Google Maps API / Leaflet.js (future enhancement)

🛠️ Project Setup

💻 Tools Required:

VS Code / PyCharm for coding

Postman for API testing

Git & GitHub for version control

Virtual Environment for dependency management

⚙️ Initialize the Django Project:

# Install Django & REST framework
pip install django djangorestframework

# Start the project
django-admin startproject ev_charging_system  
cd ev_charging_system  
python manage.py startapp reservations  

# Configure settings (database, installed apps, middleware, etc.)

🔨 Project Development

✅ Backend Development:

1️⃣ User Authentication:

Django’s built-in authentication system.

Separate user models for EV owners and admins.

Django REST Framework for API-based login/signup.

2️⃣ Slot Booking System:

Models for Charging Stations, Slots, and Bookings.

API endpoints for:

Viewing available stations.

Booking a slot.

Canceling reservations.

Fetching booking history.

3️⃣ AI-Powered Demand Prediction:

Real-time wait time and traffic estimation using AI models.

Displayed dynamically based on selected stations.

4️⃣ Real-Time Availability Updates:

Uses AJAX calls for seamless data fetching.

Dynamic station and slot rendering without reloading the page.

5️⃣ Email Notification System:

Automatic email confirmation for bookings & cancellations.

Uses Gmail SMTP settings.

Django’s send_mail() function for seamless notifications.

🎨 Frontend Development

1️⃣ Responsive UI:

User-friendly pages:

Home, Station Finder, Reservations, Carpooling, Payments, Dashboard.

Bootstrap used for styling.

Dark mode toggle button for improved accessibility.

2️⃣ Dynamic Slot Loading:

JavaScript & AJAX for dynamic station-slot pairing.

Ensures only relevant slots appear when a station is selected.

3️⃣ Interactive Dashboard:

Grid-based layout with navigation cards.

Displays reservation insights, AI predictions, and links.

⚡ API Endpoints

📌 Reservation Endpoints:

GET /reservation/ → View available slots

POST /reservation/ → Book a slot

POST /cancel-reservation/<id>/ → Cancel a reservation

📌 Carpooling Endpoints:

GET /carpooling/ → View available carpools

POST /carpooling/join/<id>/ → Join a carpool

POST /carpooling/create/ → Create a carpool

📌 AI Model Endpoints:

GET /ai-predict/<station_id>/ → Fetch AI demand prediction

Returns JSON response with wait time and availability status.

📁 Folder Structure

/ev_charging  
│── ev_charging/         # Main project folder  
│── reservations/        # Reservation app (models, views, templates)  
│── templates/           # Frontend HTML templates  
│── static/              # CSS, JS, images  
│── db.sqlite3           # Database file  
│── manage.py            # Django management script  

🛡️ Conclusion

✅ Key Takeaways:

EVie solves major pain points for EV owners by offering:

Real-time availability.

Location-based station search.

Seamless booking, management, and carpooling.

Enhances sustainable mobility and reduces congestion.

Ensures efficient energy usage with AI-powered demand prediction.

✅ Impact on Sustainable Mobility:

Supports widespread EV adoption by making charging more accessible.

Reduces traffic congestion at charging stations.

Promotes environmentally friendly transport through carpooling.

🚗⚡ Thank you for using EVie – Smart EV Charging Reservation System! 🚦

