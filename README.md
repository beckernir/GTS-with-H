# GrantTracker

GrantTracker is a comprehensive Django-based platform for managing grants, budgets, training, community engagement, and reporting in educational or organizational settings. It features strict role-based access (system admin, REB officer, school admin, teacher) and modern, user-friendly interfaces for all modules.

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

## Usage

- Log in as an admin to access all modules and management features.
- Teachers and school admins have access to their relevant dashboards and actions.
- Use the sidebar and navigation menus to access grants, budgets, training, community, and reports.
- The training calendar displays all upcoming sessions in an interactive view.

## Development

- **Static files:** Place custom CSS/JS in `static/`.
- **Templates:** All HTML templates are in `templates/` and organized by app.
- **Apps:**
  - `grants/`, `budget/`, `training/`, `community/`, `reporting/`, `core/`, `ai_engine/`, `api/`
- **Database:** Default is MySQL, but SQLite can be used for local development.

## Contribution Guidelines

1. Fork the repository and create a new branch for your feature or bugfix.
2. Write clear, well-documented code and update/add tests as needed.
3. Submit a pull request with a clear description of your changes.
4. Follow the code style and naming conventions used in the project.

## License

This project is licensed under the MIT License.

## Acknowledgements
- [Django](https://www.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [FullCalendar](https://fullcalendar.io/)
- All contributors and open-source libraries used.

---

For questions or support, please open an issue or contact the maintainers.

# GrantTracker Demo User Credentials

Below are the default demo users for each main role in the system. All users have the password: `Grant@123`

| Role                | Username      | Email                    | Password   |
|---------------------|--------------|--------------------------|------------|
| System Admin        | admin        | admin06@gmail.com        | Grant@123  |
| REB Officer         | reb-officer  | reb-officer@reb.gov.rw   | Grant@123  |
| School Admin        | school-admin | school-admin@school.rw   | Grant@123  |
| Teacher             | teacher      | teacher@school.rw        | Grant@123  |

All users are set to `active` and have the correct role assigned. You can log in to `/admin/` or the main app with these credentials. 