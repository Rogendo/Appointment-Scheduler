## Design Decisions: Healthcare Appointment Scheduling System
##### Overview

This system was designed to provide a secure, scalable, and maintainable backend for managing healthcare appointments, patients, and doctors. The core design choices focus on modularity, clarity of roles, and data consistency — aligned with healthcare data sensitivity and real-world scheduling logic.

1. Database Design

    User Separation: I separated CustomUser, Doctor, and Patients to clearly distinguish between shared and role-specific fields, enabling flexible role-based access and extension in the future.

    Normalized Schema: The database is normalized to avoid duplication and ensure referential integrity. For instance:

    - Doctor reference CustomUser.

    - Appointment references both Doctor and Patient via foreign keys.

    - Availability as a Separate Table: Doctor availability is modeled separately to support dynamic slot generation, update operations, and to check for booking conflicts efficiently.

2. Appointment Logic & Integrity

    Conflict Prevention: Before creating an appointment, the system verifies if the selected doctor is available and has no overlapping appointment. This ensures clean scheduling without double bookings.

    Availability Linking: Each appointment is tied to a specific availability slot, which can be marked as “booked” to prevent reuse.

    A doctor creates availabilty slots by keying in the start_time or work and end_time of work, then this entire timeframe, is broken and split into smaller 1 hr bookable sessions!

3. Security Design

    Role-Based Access Control (RBAC): Authentication is done via OAuth2.0 or JWTs, with roles such as 'Patient', and 'Admin' assigned to users. Each API endpoint enforces access restrictions, except the patients creation and appointment booking.

    Data Protection: Sensitive patient data (e.g., insurance, medical records) is handled using field-level encryption. Medical records are only accessible to authorized doctors and the admin.

    Auditability: Timestamps (created_at, updated_at) on all records support audit trails.

4. API Design

    RESTful Endpoints: All endpoints follow RESTful conventions with clear, consistent naming (/patients, /appointments, /doctors/availability).

    Swagger/redoc API Documentation: The API is fully documented using Swagger and redoc to enable testing and ease of integration with frontend/mobile clients.


5. Testing Approach

    Unit Tests cover the core business logic: appointment booking, availability conflict detection, and user role enforcement.

    Although, the script unit tests for some core functionalities were problematic as it was impossible to create or simulate the creation of the multiple availability slots! Using the api for this testing works best and more efficiently.

