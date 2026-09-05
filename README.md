# RideShare — Full-Stack Ride Booking Platform

A collaborative full-stack ride-booking project built to explore REST API design, authentication, role-based application flows, real-time WebSocket communication, mapping, and backend architecture.
The repository contains two backend generations: an earlier Flask/Firebase implementation and a newer Django REST Framework implementation. The Django backend is the current version and is the primary focus of this repository.

## What this project demonstrates

- REST API design with Django REST Framework
- JWT-based authentication with access and refresh tokens
- Custom Django user model with `customer` and `driver` roles
- Invitation and account-activation workflow
- Role-aware frontend routing
- Ride discovery, booking, acceptance, notification, and payment flows
- Distance-based ride pricing with `geopy`
- Real-time location exchange with Django Channels and WebSockets
- Google Maps integration
- Environment-based configuration for application secrets and allowed origins
- Refactoring from an earlier Flask/Firebase architecture to Django/DRF

## Architecture

```text
                    ┌─────────────────────────┐
                    │      React frontend     │
                    │      Vite + JSX         │
                    └────────────┬────────────┘
                                 │
                    HTTP / JSON  │  WebSocket
                                 │
             ┌───────────────────┴───────────────────┐
             │                                       │
             ▼                                       ▼
┌──────────────────────────┐            ┌──────────────────────────┐
│ Django REST Framework    │            │ Django Channels          │
│ JWT authentication       │            │ authenticated WebSocket  │
│ ride-booking APIs        │            │ location exchange        │
│ notifications/payments   │            │                          │
└────────────┬─────────────┘            └────────────┬─────────────┘
             │                                       │
             └───────────────────┬───────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │      Django models      │
                    │ User / Vehicle          │
                    │ RideOrder / Payments    │
                    │ Invitation / Notification│
                    └─────────────────────────┘
```

For local development, the Django project currently uses SQLite and an in-memory Channels layer.

## Core application flow

### Account lifecycle

An administrator can create an invitation for a new user. The application generates an activation link and allows the invited user to register as either a `customer` or `driver`.

Authentication is handled with Django REST Framework and SimpleJWT. Authenticated users receive access and refresh tokens, and refresh tokens can be blacklisted during logout.

### Customer workflow

A customer can:

- authenticate to the application
- view available vehicles
- choose a driver
- select departure and destination coordinates
- create a ride request
- receive ride-status notifications
- share location information during the ride
- view and complete a payment record

### Driver workflow

A driver can:

- authenticate to the application
- access a driver-specific dashboard
- receive ride-request notifications
- accept or reject ride requests
- participate in the real-time location-sharing flow

## REST API surface

| Endpoint | Purpose |
| --- | --- |
| `/login/` | Authenticate a user and issue JWT tokens |
| `/register/` | Register an invited user |
| `/activate/<uidb64>/<token>/` | Validate an account invitation/activation link |
| `/logout/` | Blacklist the active refresh token and log out |
| `/user-dashboard/` | Retrieve available vehicle information |
| `/order-ride/` | Start the ride-order workflow |
| `/book-ride/` | Create a ride booking and calculate the price |
| `/notification/` | Retrieve user notifications |
| `/accept-order/` | Accept or reject a ride request |
| `/mark-notification/` | Mark a notification as read |
| `/payment/` | Retrieve or complete payment records |

Most operational API views require JWT authentication.

## Data model

- **User** — custom authentication model with `customer` and `driver` roles
- **Vehicle** — vehicle assigned one-to-one to a user/driver
- **RideOrder** — customer/driver relationship, route information, distance, and ride status
- **Payments** — payment state and calculated ride price
- **InvitationEmails** — invitation and registration state
- **Notification** — sender/receiver ride notifications and read state

Ride orders support the states:

```text
pending → accepted / rejected → in_progress → completed
```

## Real-time communication

The project uses Django Channels for WebSocket communication.

Authenticated WebSocket clients are assigned to per-user channel groups. Location messages can then be exchanged between the customer and driver participating in a ride.

The WebSocket layer is currently configured with Django Channels' in-memory channel layer for local development.

## Frontend

The frontend is implemented in React with Vite and includes:

- public and protected routes
- customer-only and driver-only application views
- authentication state stored client-side
- customer dashboard
- driver dashboard
- ride-order interface
- notification interface
- payment interface
- Google Maps integration
- real-time location display through WebSockets

Client-side route guards improve the user experience, while API authentication remains a backend responsibility.

## Security-related implementation

- JWT authentication using Django REST Framework SimpleJWT
- refresh-token rotation and blacklisting configuration
- Django password validators
- authenticated API views using `IsAuthenticated`
- authenticated WebSocket connections
- CORS restricted to configured origins
- Django secret key, allowed hosts, CORS origins, CSRF origins, and SMTP credentials loaded from environment variables
- Google Maps API key removed from source code and loaded from environment configuration
- `.env` files excluded from version control

This is an educational portfolio project and should not be considered production-ready without additional hardening, infrastructure configuration, and security testing.

## Project structure

```text
project_app_rest/
├── Frontend/               # React/Vite client
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   ├── .env.example
│   └── vite.config.js
├── New_Backend/            # Current Django/DRF implementation
│   ├── app/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializer.py
│   │   ├── permissions.py
│   │   ├── consumers.py
│   │   ├── routing.py
│   │   └── user_auth.py
│   ├── rideshare/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── asgi.py
│   ├── templates/
│   ├── requirements.in
│   ├── requirements.txt
│   └── manage.py
├── Backend/                # Earlier Flask/Firebase implementation
├── Project_app.ipynb       # Earlier development notes / prototype work
└── README.md
```

## Backend setup

### 1. Clone the repository

```bash
git clone https://github.com/Thomas170491/project_app_rest.git
cd project_app_rest/New_Backend
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Direct dependencies are maintained in `requirements.in`; the pinned dependency set is generated in `requirements.txt`.

### 4. Configure environment variables

```bash
cp .env.example .env
```

Generate a local Django secret key:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Then update `.env` with local values.

```dotenv
DJANGO_SECRET_KEY=replace-with-a-random-development-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:5173

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=example@example.com
EMAIL_HOST_PASSWORD=example_password
EMAIL_PORT=587
```

Do not commit the real `.env` file.

### 5. Initialize the database

```bash
python manage.py migrate
```

Optionally create an administrator account:

```bash
python manage.py createsuperuser
```

### 6. Validate the Django configuration

```bash
python manage.py check
```

### 7. Run the backend

```bash
python manage.py runserver
```

The development server will normally be available at:

```text
http://127.0.0.1:8000/
```

## Frontend environment configuration

The React application reads its Google Maps key from Vite environment configuration:

```dotenv
VITE_GOOGLE_MAPS_API_KEY=replace-with-google-maps-browser-key
```

The frontend source also expects backend HTTP and WebSocket base URLs through Vite environment variables when running the complete application locally.

Google Maps browser keys should be restricted in Google Cloud by allowed HTTP referrers and by the minimum required Maps APIs.

## Project evolution

This repository intentionally retains the earlier `Backend/` implementation alongside `New_Backend/`.

The earlier version was built with Flask and Firebase. The newer implementation moves the application toward a more structured API architecture using Django REST Framework, Django ORM models, SimpleJWT authentication, and Django Channels.

Keeping both versions provides a record of the project's architectural evolution and the transition from an initial application prototype to a more structured REST-oriented backend.

## Current status

Implemented areas include authentication, invitations, customer/driver roles, ride ordering, notifications, payment state, mapping, and WebSocket-based location exchange.

Areas for future improvement include:

- automated backend and frontend tests
- stricter server-side role/permission policies
- Redis-backed Channels configuration
- production database configuration
- HTTPS and secure deployment settings
- structured logging and removal of remaining debug output
- API schema/OpenAPI documentation
- improved error handling and validation
- CI/CD for the full-stack application

## Collaboration

This project was developed collaboratively.

The repository reflects contributions from multiple developers across the application's backend, frontend, and integration work. My contributions focused on areas of the application that I worked on directly, while other parts of the project were developed jointly or by collaborators.

Git history is preserved to provide a transparent record of individual contributions.

## Portfolio context

I include this project in my portfolio because it demonstrates my practical experience with backend development, REST APIs, authentication, application architecture, and secure configuration in a collaborative software-development environment.