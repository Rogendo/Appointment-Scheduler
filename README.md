
# 🏥 Healthcare Appointment Scheduling System

This project implements a secure, scalable backend system for managing patients, doctors, appointments, and medical records. This system supports role-based access control, conflict-free scheduling, and availability management.

## Features
- **Patient profile registration and management**:  Patients can sign up and manage their personal profiles, which include:

    - Contact information (email, phone number)

    - Date of birth

    - Insurance details (name & number)
    
    These details are securely stored and used when scheduling appointments and managing medical history.

- **Doctor profile management with specializations**: Doctors can have detailed profiles that include:

    - Full name and contact info

    - Specialization (e.g., Cardiology, Pediatrics)

    - Department (e.g., Oncology, Maternity)

    - Current availability status (available/occupied)
    
    This helps patients find the right doctor for their needs and ensures accurate matching in the scheduling process.

- **Doctor availability scheduling**: Doctors (or admins) can define their working hours via availability slots. The system:

    - Splits longer periods into 1-hour blocks

    - Ensures no overlaps

    - Stores availability status (booked or free)
    
    This forms the backbone for conflict-free appointment scheduling.
- **Appointment booking with conflict detection**: Patients can book appointments with doctors using available time slots. The system:

    - Checks availability of the selected slot

    - Prevents double-booking and overlaps

    - Automatically marks a slot as “unavailable” once booked

    - Supports appointment status (Scheduled, Completed, Cancelled)

- **Role-based access control (OAuth2)**: Secure access is enforced via:

    - Authentication using email/password and token-based login (OAuth2 + JWT)

    - Authorization levels for different roles (e.g., doctor, admin)

    - Secure route access—only the right users can modify or view certain data (e.g., only doctors can write medical records)

- **API documentation with Swagger/OpenAPI**: Interactive documentation is auto-generated:

    - Lists all available endpoints with descriptions

    - Allows testing directly from the browser

    - Ensures developers and testers can integrate with the API easily

    - Available at /docs and /redoc endpoints in the development environment.

---

## 📖 Documentation
📜 **[Design Desisions Documentation](DesignDecisions.md)** – Defines and explains the design decisions.

---

## 🚀 Getting Started

### **Prerequisites**
Ensure you have the following installed:
- **Python 3.11+**

### **Installation**


The following instructions were tested on the Windows and Linux with Python 3.11+

1. Clone this repository

```

git clone https://github.com/Rogendo/Appointment-Scheduler/.git

```

```

cd Appointment-Scheduler/

```

2. Create and activate virtual environment 

```

python -m venv venv

```

on Linux system

```

source venv/bin/activate

```

on Windows system

```

.\venv\Scripts\activate.bat

```

3. Install requirements

```

pip install  -r requirements.txt

```
4. Change directory to the directory with the manage.py file,
   then run the server.

5. Run the server

```

python manage.py runserver

```