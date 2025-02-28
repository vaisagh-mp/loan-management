# Loan Management System (Django REST API)

## Overview
The Loan Management System is a Django-based REST API designed to manage loans with user-defined monthly compound interest. It supports role-based authentication, automatic interest calculations, and loan repayment schedules. Users can also foreclose loans before tenure completion with adjusted interest calculations.

---

## Tech Stack
- Backend: Django, Django REST Framework (DRF)
- Authentication: JWT (Simple JWT) with OTP Email Verification
- Database: PostgreSQL or SQLite
- Deployment: Render

---

## Features
### 1 Authentication & Role-Based Access Control
 * Implement JWT authentication using Simple JWT  
 * Register users with OTP email verification  
 * Support Admin and User roles  
 * Ensure each API call includes a valid JWT token

### 2️ Loan Management
 * Users can apply for a loan by specifying amount, tenure, and interest rate  
 * Users can view their active and past loans  
 * Users can view loan details with a payment schedule  
 * Users can foreclose a loan early (adjusted interest applies)  
 * Admins can view, manage, and delete loans  

### 3️ Loan Calculation
 * Monthly compound interest calculation  
 * Auto-generated monthly installment schedules  
 * Foreclosure allows early payment with adjusted interest  
 * Stores total payable amount, interest amount, and payment schedules

---

## API Endpoints

### User Authentication
| Method | Endpoint                 | Description                        |
|--------|--------------------------|------------------------------------|
| `POST` | `/api/users/register/`   | Register user and send OTP         |
| `POST` | `/api/users/verify-otp/` | Verify OTP to activate the account |
| `POST` | `/api/users/login/`      | User login with JWT authentication |


### User Loan Management
| Method | Endpoint                          | Description                               |
|--------|-----------------------------------|-------------------------------------------|
| `POST` | `/api/loans/`                     | Apply for a loan                          |
| `GET`  | `/api/loans/`                     | List all loans for the authenticated user |
| `GET`  | `/api/loans/{loan_id}/`           | Get details of a specific loan            |
| `POST` | `/api/loans/{loan_id}/foreclose/` | Foreclose a loan (early repayment)        |

### Admin Loan Management
| Method    | Endpoint                             | Description                     |
|-----------|--------------------------------------|---------------------------------|
| `GET`     | `/api/admin/loans/`                  | View all loans in the system    |
| `GET`     | `/api/admin/loans/{loan_id}/`        | View details of a specific loan |
| `DELETE`  | `/api/admin/loans/{loan_id}/delete/` | Delete a loan                   |

---

## Installation & Setup
### 1️ Clone the Repository
```bash
git clone https://github.com/vaisagh-mp/loan-management.git
cd loan-management
```

### 2️ Create a Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️ Configure `.env` File
Create a `.env` file in the root directory and add:
```env
DB_NAME=loan_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
SECRET_KEY=your-secret-key
```

### 4️ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️ Create a Superuser (Admin Panel Access)
```bash
python manage.py createsuperuser
```

### 6 Run the Development Server
```bash
python manage.py runserver
```

Now, visit `http://127.0.0.1:8000/admin/` to log into the Django Admin Panel.

---

## Testing the API with Postman
1. Register a User → Receive OTP via email
2. Verify OTP → Activate account
3. Login → Obtain JWT access token
4. Create a Loan → Apply for a new loan
5. Foreclose a Loan → Pay early with adjusted interest
6. Admin Actions → View or delete loans

---

## 📝 Testing Instructions

### 1️ Testing with Postman**
1.Import the Postman Collection** (Download or generate from the API).
2.Set `{{base_url}}` to `http://127.0.0.1:8000/` for local testing**.
3.Register a user** to receive OTP.
4.Verify OTP** to activate the account.
5.Login to obtain JWT token** and set it as `Authorization: Bearer <token>`.
6.Test Loan Creation and Management APIs**.
7.Foreclose a loan and validate the response**.
8.Admin can test listing and deleting loans**.

### 2️ Running Automated Tests**
To run Django unit tests:
```bash
python manage.py test
```



