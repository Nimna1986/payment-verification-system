# Payment Verification System

A full-stack payment verification system that helps verify customer payments against orders using payment information and OCR-based payment screenshot processing.

The system consists of:

* **React frontend** — user interface
* **FastAPI backend** — REST API and business logic
* **PostgreSQL** — database
* **OCR** — extracts payment information from uploaded payment screenshots

---

## 1. System Architecture

```text
                    ┌─────────────────────┐
                    │      Frontend       │
                    │   React / Vite      │
                    └──────────┬──────────┘
                               │
                               │ HTTP Requests
                               ▼
                    ┌─────────────────────┐
                    │       Backend       │
                    │      FastAPI        │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │   PostgreSQL    │         │      OCR        │
        │    Database     │         │    Processing   │
        └─────────────────┘         └─────────────────┘
```

### Payment Verification Flow

```text
Customer Order
      │
      ▼
Payment Information
      │
      ▼
Payment Screenshot Upload
      │
      ▼
OCR Text Extraction
      │
      ▼
Extract Payment Details
      │
      ▼
Compare With Order
      │
      ▼
Payment Verification
      │
      ▼
Verification Result
```

---

# 2. Technology Stack

### Backend

* Python 3.13
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* Tesseract OCR
* Pytesseract
* Pillow
* Uvicorn

### Frontend

* React
* Vite
* JavaScript
* npm

### Database

* PostgreSQL

---

# 3. Project Structure

```text
payment-verification-project/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .env.example
├── .gitignore
└── README.md
```

The FastAPI application entry point is:

```text
backend/app/main.py
```

---

# 4. Prerequisites

Before running the project locally, install:

* Git
* Python 3.13
* PostgreSQL
* Node.js
* npm
* Tesseract OCR

Check the installations:

```bash
git --version
python --version
psql --version
node --version
npm --version
```

Python 3.13 is recommended for the backend environment.

---

# 5. Clone the Repository

Open a terminal and clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Enter the project directory:

```bash
cd <YOUR_REPOSITORY_NAME>
```

---

# 6. PostgreSQL Setup

Make sure PostgreSQL is installed and running.

Create the application database.

For example:

```sql
CREATE DATABASE payment_verification;
```

The database name can be changed, but the name must match the backend configuration.

---

# 7. Backend Local Setup

Open a terminal in the project root.

Move into the backend:

```bash
cd backend
```

## 7.1 Create Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

After activation, the terminal should show:

```text
(.venv)
```

---

## 7.2 Install Backend Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

# 8. Backend Environment Variables

Create a `.env` file inside the `backend` directory.

Example:

```text
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/payment_verification
```

Replace:

```text
USERNAME
PASSWORD
```

with the PostgreSQL credentials configured on the local machine.

### Important

Do not commit the real `.env` file to GitHub.

Use `.env.example` as a template.

---

# 9. Tesseract OCR Setup

The payment verification system uses Tesseract OCR to extract text from payment screenshots.

Install Tesseract OCR on the local machine.

On Windows, the executable is commonly installed at:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If the project configuration requires the Tesseract executable path, make sure it points to the correct installation path on the local machine.

Verify the installation:

```bash
tesseract --version
```

If the command is not recognized, use the installed Tesseract executable path or add Tesseract to the system PATH.

---

# 10. Start the Backend

Make sure:

* PostgreSQL is running
* The virtual environment is activated
* You are inside the `backend` directory

Run:

```bash
uvicorn app.main:app --reload
```

The backend should start at:

```text
http://127.0.0.1:8000
```

If `uvicorn` is not recognized, use:

```bash
python -m uvicorn app.main:app --reload
```

---

# 11. Backend API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows reviewers to:

* View API endpoints
* Create and retrieve orders
* Submit payment information
* Upload payment screenshots
* Test payment verification
* Inspect API responses

Alternative documentation is available at:

```text
http://127.0.0.1:8000/redoc
```

---

# 12. Frontend Local Setup

Keep the backend running.

Open a **second terminal**.

From the project root:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

---

# 13. Frontend Environment Configuration

The frontend needs to know where the FastAPI backend is running.

If the frontend uses a Vite environment file, configure the API URL according to the variable used by the project.

For example:

```text
VITE_API_URL=http://127.0.0.1:8000
```

The important point is that the frontend must communicate with:

```text
http://127.0.0.1:8000
```

which is the local FastAPI backend.

Do not commit sensitive credentials to the frontend environment file.

---

# 14. Start the Frontend

From the `frontend` directory:

```bash
npm run dev
```

Vite will display a local URL in the terminal.

Typically:

```text
http://localhost:5173
```

Open the URL shown by Vite in a browser.

---

# 15. Running the Complete Application

The backend and frontend need to run simultaneously.

## Terminal 1 — Backend

From the project root:

```powershell
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Terminal 2 — Frontend

From the project root:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

Use the exact URL displayed by Vite if it chooses a different port.

---

# 16. Complete Local Setup — Quick Version

For an experienced developer:

### Terminal 1

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
cd backend

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Terminal 2

```bash
cd <YOUR_REPOSITORY_NAME>
cd frontend

npm install
npm run dev
```

Then open the frontend URL displayed by Vite.

---

# 17. Testing the Application

Once both servers are running:

### Step 1 — Open the Frontend

Open:

```text
http://localhost:5173
```

### Step 2 — View Orders

Use the frontend to view the available orders.

### Step 3 — Select an Order

Select the order for which a payment needs to be verified.

### Step 4 — Submit Payment

Provide the payment information required by the application.

### Step 5 — Upload Payment Screenshot

Upload the relevant bank/payment screenshot.

### Step 6 — OCR Processing

The backend processes the uploaded image using OCR.

The system attempts to extract relevant information such as:

* Transaction/reference number
* Payment amount
* Payment-related information

### Step 7 — Verification

The extracted payment information is compared against the relevant order/payment information.

### Step 8 — View Result

The frontend displays the payment verification result.

---

# 18. Testing the Backend Independently

The frontend is not required to test the API.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to independently test the backend endpoints.

This is useful for verifying that:

```text
Frontend
   ↓
FastAPI API
   ↓
Business Logic
   ↓
PostgreSQL
```

is working correctly.

---

# 19. Troubleshooting

## Backend does not start

Make sure you are inside:

```text
backend/
```

and the virtual environment is activated.

Then run:

```powershell
.venv\Scripts\activate
```

and:

```bash
python -m uvicorn app.main:app --reload
```

---

## `ModuleNotFoundError`

Install the backend dependencies again:

```bash
pip install -r requirements.txt
```

---

## PostgreSQL connection error

Check:

1. PostgreSQL is running.
2. The database exists.
3. The username is correct.
4. The password is correct.
5. The database name is correct.
6. The `DATABASE_URL` is correct.

Example:

```text
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/payment_verification
```

---

## Frontend cannot connect to backend

Check that the backend is running:

```text
http://127.0.0.1:8000/docs
```

Then check the frontend API configuration.

It should point to the local backend:

```text
http://127.0.0.1:8000
```

Also make sure both frontend and backend are running simultaneously.

---

## `npm` is not recognized

Install Node.js and restart the terminal.

Verify:

```bash
node --version
npm --version
```

---

## Frontend dependencies are missing

Inside the frontend directory:

```bash
npm install
```

Then:

```bash
npm run dev
```

---

## Tesseract OCR error

Verify that Tesseract is installed:

```bash
tesseract --version
```

If Windows cannot find Tesseract, check that the configured executable path points to the actual installation location.

---

# 20. Security Notes

For local development:

* Never commit `.env` files containing passwords or secrets.
* Never commit PostgreSQL credentials.
* Do not expose production credentials in frontend code.
* Use environment variables for configuration.
* Use separate credentials for development and production.

---

# 21. Reviewer / Interviewer Checklist

Before evaluating the project, verify:

* [ ] PostgreSQL is installed and running
* [ ] The database has been created
* [ ] Python 3.13 is installed
* [ ] Backend virtual environment is created
* [ ] Backend dependencies are installed
* [ ] Backend `.env` is configured
* [ ] Tesseract OCR is installed
* [ ] FastAPI starts successfully
* [ ] Swagger opens successfully
* [ ] Node.js and npm are installed
* [ ] Frontend dependencies are installed
* [ ] Frontend API URL points to the local backend
* [ ] Frontend starts successfully
* [ ] Frontend can communicate with the backend
* [ ] Orders can be accessed
* [ ] Payment information can be submitted
* [ ] Payment screenshots can be uploaded
* [ ] OCR processing works
* [ ] Payment verification produces a result

---

# 22. Local URLs

| Component | URL                           |
| --------- | ----------------------------- |
| Frontend  | `http://localhost:5173`       |
| Backend   | `http://127.0.0.1:8000`       |
| Swagger   | `http://127.0.0.1:8000/docs`  |
| ReDoc     | `http://127.0.0.1:8000/redoc` |

> The frontend port may differ if Vite automatically selects another available port. Always use the URL displayed in the terminal.

---

# 23. Notes

This project is designed to demonstrate a complete full-stack payment verification workflow, including:

* Order management
* Payment management
* Payment screenshot upload
* OCR-based information extraction
* Payment verification
* REST API development
* PostgreSQL database integration
* Frontend/backend integration

The backend and frontend can also be tested independently using Swagger and the frontend application respectively.
