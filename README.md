# User Preferences Backend API

A backend service designed to manage user accounts and preferences securely and efficiently. It supports user registration, login, and preference updates for features like account settings, notification preferences, theme settings, and privacy configurations.

---

## Features

- **User Authentication**: Secure user login and registration using JWT.
- **Preferences Management**: Update and retrieve user-specific settings:
  - Account Settings
  - Notification Preferences
  - Theme Settings
  - Privacy Settings
- **API Documentation**: Swagger UI available for interactive API exploration.
- **Scalable Design**: Modular architecture for easy extension.

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- `pip` (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/UsithaDJay/user_preferences_backend.git
   cd user_preferences_backend
2. Create and activate a virtual environment:
    ```bash
   python -m venv env
   env\Scripts\activate
3. Install Dependancies:
    ```bash
   pip install -r requirements.txt
4. Set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
5. Run the server:
    ```bash
    python manage.py runserver

The app should now be running at http://localhost:8000.

6. Access the API documentation:
    > http://localhost:8000/docs/

## API Overview

### Authentication

- **Register**: `POST /api/register/`
- **Login**: `POST /api/login/`

### Preferences

- **Get Preferences**: `GET /api/preferences/`
- **Retrieve Specific Preferences**:
  - `GET /api/preferences/account_settings/`
  - `GET /api/preferences/notification_settings/`
  - `GET /api/preferences/theme_settings/`
  - `GET /api/preferences/privacy_settings/`
- **Update Preferences**:
  - `PATCH /api/preferences/account_settings/`
  - `PATCH /api/preferences/notification_settings/`
  - `PATCH /api/preferences/theme_settings/`
  - `PATCH /api/preferences/privacy_settings/`

## Architecture

### Key Components

1. **Models**:
   - **`UserData`**: Stores user details like username, email, and password.
   - **`NotificationSettings`**: Preferences for notifications (frequency, email, and push notifications).
   - **`ThemeSettings`**: Preferences for themes and font sizes.
   - **`PrivacySettings`**: Preferences for profile visibility and data sharing.

2. **Views**:
   - **`RegisterView`**: Handles user registration.
   - **`LoginView`**: Manages user login.
   - Individual views (`AccountSettingsView`, `NotificationSettingsView`, etc.) handle preference-specific operations.

3. **Authentication**:
   - **JWT-based Authentication**: Provides secure access to the API by requiring valid tokens for authenticated operations.

---

## Testing

1. **Run the test suite**:
   ```bash
   python manage.py test preferences.tests
1. **Types of Tests**:
   - **Unit Tests**: Validate individual components such as models and serializers.
   - **Functional Tests**: Ensure user flows like registration, login, and updating preferences work as intended.

## Error Handling

- **400 Bad Request**: Invalid input data.
- **401 Unauthorized**: Missing or invalid authentication token.
- **403 Forbidden**: Access to resource denied.
- **404 Not Found**: Resource does not exist.

---

## Deployment

1. Configure your environment variables for production (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`).
2. Use `gunicorn` or any other WSGI server to serve the app.

---

## Security

- **JWT Authentication**: Secure access for APIs.
- **Data Validation**: Input data is rigorously validated to prevent injection attacks.
- **Atomic Transactions**: Preference updates are processed as atomic operations to ensure data consistency.

---

## Future Enhancements

- **Using Hashed Passwords**: Store user passwords securely using industry-standard hashing algorithms.
- **Validate with Old Password When Updating**: Require users to confirm their old password before allowing password updates for added security.
- **Use Django's Default User Model**: Leverage Django's built-in `User` model to simplify user management and utilize existing best practices.
