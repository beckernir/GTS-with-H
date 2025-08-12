
# GrantTracker

GrantTracker is a comprehensive Django-based platform for managing grants, budgets, training, community engagement, and reporting in educational or organizational settings. It features strict role-based access (system admin, REB officer, school admin, teacher) and modern, user-friendly interfaces for all modules.

---

## Table of Contents
- [Features](#features)
- [Module Overview](#module-overview)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [User Management](#user-management)
- [Grant Management](#grant-management)
- [Budget Management](#budget-management)
- [Training Module](#training-module)
- [Community Module](#community-module)
- [Reporting](#reporting)
- [AI Engine](#ai-engine)
- [API](#api)
- [Admin Panel](#admin-panel)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contribution Guidelines](#contribution-guidelines)
- [Demo User Credentials](#granttracker-demo-user-credentials)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Grant Management:** Track and manage grants, categories, and related documents.
- **Budget Module:** Manage budget categories, line items, and transfers with real-time summaries and charts.
- **Training Module:**
  - Manage courses, sessions, enrollments, and progress.
  - Role-based enrollment (admins can enroll others).
  - Certificate management and assignment.
  - Interactive training calendar (FullCalendar integration).
- **Community:** Announcements, discussions, and school engagement.
- **Reporting:** Overview dashboards and exportable reports.
- **Role-Based Access:** System admin, REB officer, school admin, teacher, with permissions enforced throughout.
- **Modern UI:** Bootstrap 5, responsive design, and clear navigation.
- **AI Engine:** Proposal prediction, anomaly detection, and model retraining.
- **REST API:** (if enabled) for integration and automation.

---

## Module Overview

- **core/**: User management, authentication, dashboard, and system configuration.
- **grants/**: Grant proposals, categories, allocation, and document management.
- **budget/**: Budget categories, line items, transfers, and school budget management.
- **training/**: Courses, sessions, enrollments, certificates, and calendar.
- **community/**: Announcements, forums, events, and messaging.
- **reporting/**: Custom, financial, monthly, performance, and school reports.
- **ai_engine/**: Machine learning pipeline, model training, and predictions.
- **api/**: (Optional) REST API endpoints for external integration.
- **procurement/**: (If enabled) Tender and procurement management.

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- pip
- MySQL (or SQLite for development)
- [Node.js](https://nodejs.org/) (optional, for advanced frontend tooling)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/beckernir/GTS-with-H.git
   cd GTS-with-H
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and set your database and secret key values.
5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
8. **Access the app:**
   - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Quick Start Commands

Here are the essential commands to get your GrantTracker project up and running:

1. **Create a virtual environment:**
   ```sh
   python -m venv venv
   ```
   Activate it:
   - **Windows:**
     ```sh
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```sh
     source venv/bin/activate
     ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Apply database migrations:**
   ```sh
   python manage.py migrate
   ```

4. **Create a superuser (admin account):**
   ```sh
   python manage.py createsuperuser
   ```

5. **(Optional) Load demo or dummy data:**
   - Budget dummy transfers:
     ```sh
     python manage.py add_dummy_transfers
     ```
   - Reporting dummy data:
     ```sh
     python manage.py add_dummy_reporting_data
     ```
   - Load criteria demo:
     ```sh
     python manage.py load_criteria_demo
     ```
   - AI Engine (export and train):
     ```sh
     python manage.py export_training_data
     python manage.py train_ml_model
     ```

6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
   Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

7. **(Optional) Collect static files (for production):**
   ```sh
   python manage.py collectstatic
   ```

8. **(Optional) Run tests:**
   ```sh
   python manage.py test
   ```

---

## Usage Guide

- Log in as an admin to access all modules and management features.
- Teachers and school admins have access to their relevant dashboards and actions.
- Use the sidebar and navigation menus to access grants, budgets, training, community, and reports.
- The training calendar displays all upcoming sessions in an interactive view.
- Use the top-right user menu for profile and logout options.

---

## User Management

- **View Users:** Go to Users in the sidebar to see all users. Filter by role or status, or search by name/email.
- **Create User:** Click "Create User" on the user list page. Fill in all required fields, set role and status, and upload a profile picture if desired.
- **Edit User:** Click the edit icon next to a user to update their details.
- **Activate/Deactivate:** Use the action buttons to activate, deactivate, or delete users.
- **Roles:**
  - System Admin: Full access to all modules and user management.
  - REB Officer: Can manage schools, users, and grants.
  - School Admin: Manages teachers and community members at their school.
  - Teacher: Access to training, community, and relevant grants.
  - Community Member: Limited access to community features.
- **Status:** Active, Inactive, Suspended, Pending Approval.
- **Assign to School:** Use the school assignment feature in the user detail view.

---

## Grant Management

- **Proposals:** Create, review, allocate, and manage grant proposals.
- **Categories:** Organize grants by category.
- **Documents:** Upload and manage documents related to proposals.
- **Review/Allocate:** System admins and REB officers can review and allocate grants.

---

## Budget Management

- **School Budgets:** Create and manage budgets for each school.
- **Categories & Line Items:** Add/edit budget categories and line items.
- **Transfers:** Approve or create fund transfers between categories.
- **Reports:** Generate and download budget reports.

---

## Training Module

- **Courses:** Create and manage training courses.
- **Sessions:** Schedule and manage training sessions.
- **Enrollments:** Enroll users in courses (role-based permissions).
- **Certificates:** Assign and manage training certificates.
- **Calendar:** View all sessions in a calendar view.

---

## Community Module

- **Announcements:** Post and manage school/community announcements.
- **Forums:** Create and participate in discussion forums.
- **Events:** Schedule and view community events.
- **Messaging:** Send and receive messages within the platform.

---

## Reporting

- **Dashboards:** Overview dashboards for admins and users.
- **Custom Reports:** Generate custom, financial, monthly, performance, and school reports.
- **Export:** Download reports as PDF.

---

## AI Engine

- **Proposal Prediction:** Get AI-based recommendations for grant proposals.
- **Anomaly Detection:** Detect unusual patterns in proposals or budgets.
- **Model Retraining:** Use management commands to retrain the AI model:
  ```bash
  python manage.py export_training_data
  python manage.py train_ml_model
  ```
- **Status:** View AI model status in the admin or AI dashboard.

---

## API

- **REST API:** (If enabled) Access data programmatically. See `api/` app for available endpoints and authentication.

---

## Admin Panel

- **Access:** `/admin/` (use superuser or demo credentials)
- **Manage:** All models, users, and system settings.

---

## Testing

- **Run all tests:**
  ```bash
  python manage.py test
  ```
- **App-specific tests:**
  ```bash
  python manage.py test grants
  python manage.py test budget
  # etc.
  ```

---

## Troubleshooting

- **Migrations:** If you have migration issues, try:
  ```bash
  python manage.py makemigrations
  python manage.py migrate --fake-initial
  ```
- **Static Files:**
  ```bash
  python manage.py collectstatic
  ```
- **Common Issues:**
  - Check `.env` for correct DB and secret key.
  - Ensure all dependencies are installed.
  - Use the Django admin for emergency user management.

---

## Contribution Guidelines

1. Fork the repository and create a new branch for your feature or bugfix.
2. Write clear, well-documented code and update/add tests as needed.
3. Submit a pull request with a clear description of your changes.
4. Follow the code style and naming conventions used in the project.

---

# GrantTracker Demo User Credentials

Below are the default demo users for each main role in the system. All users have the password: `Grant@123`

| Role                | Username      | Email                    | Password   |
|---------------------|--------------|--------------------------|------------|
| System Admin        | admin        | admin06@gmail.com        | Grant@123  |
| REB Officer         | reb-officer  | reb-officer@reb.gov.rw   | Grant@123  |
| School Admin        | school-admin | school-admin@school.rw   | Grant@123  |
| Teacher             | teacher      | teacher@school.rw        | Grant@123  |

All users are set to `active` and have the correct role assigned. You can log in to `/admin/` or the main app with these credentials.

---

## License

This project is licensed under the MIT License.

## Acknowledgements
- [Django](https://www.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [FullCalendar](https://fullcalendar.io/)
- All contributors and open-source libraries used.

---

For questions or support, please open an issue or contact the maintainers. 