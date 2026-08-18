# Automated Bank Payment Verification System

A full-stack payment verification system developed for the **BuildStart Software Engineering Intern 2-Day Engineering Challenge**.

The system allows a business to manage customer orders, record payment submissions, process payment screenshots using OCR, and verify whether a submitted payment matches the expected order information.

The system produces a verification status and provides reasons that can be used by a business employee to decide whether the payment can be accepted.

---

# 1. Problem

The system is designed around the following payment workflow:

```text
Customer places an order
        ↓
Order is recorded in the system
        ↓
Customer makes a bank transfer
        ↓
Customer sends payment slip
        ↓
Payment information is submitted
        ↓
Payment image is processed using OCR
        ↓
Extracted payment information is compared
with the payment/order information
        ↓
Payment verification result
```

There is no direct bank API available for this challenge.

Therefore, the prototype works with the evidence available from the payment submission and the application's existing order/payment records.

---

# 2. Current System

The implemented system contains:

* Order management
* Payment management
* Payment-to-order relationship
* Payment screenshot/image upload
* OCR text extraction from payment images
* Payment verification endpoint
* Payment status tracking
* PostgreSQL persistence
* FastAPI REST API
* Swagger API documentation
* React frontend
* Backend/frontend integration

---

# 3. Technology Stack

## Backend

* Python 3.13
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* Uvicorn
* Pytesseract
* Pillow
* Tesseract OCR

## Frontend

* React
* Vite
* JavaScript
* npm

## Database

* PostgreSQL

## Deployment

* Backend deployed using Render
* Frontend communicates with the backend API

---

# 4. Architecture

```text
                    ┌──────────────────────┐
                    │       Frontend       │
                    │      React/Vite      │
                    └──────────┬───────────┘
                               │
                               │ HTTP API
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │   PostgreSQL    │        │      OCR        │
        │                 │        │    Tesseract    │
        │ Orders          │        │                 │
        │ Payments        │        │ Payment Image   │
        └─────────────────┘        └─────────────────┘
```

---

# 5. Project Structure

```text
project-root/
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
├── .gitignore
└── README.md
```

The backend entry point is:

```text
backend/app/main.py
```

---

# 6. Database Design

The application uses PostgreSQL to persist the order and payment information.

The main entities currently used by the system are:

```text
Orders
   │
   │
   └──────── Payments
```

An order contains information such as:

* Order ID
* Order number
* Customer name
* Expected payment amount
* Order status

A payment contains information such as:

* Payment ID
* Amount
* Transaction ID
* Payment status
* Payment method
* Related order

The database allows the system to compare submitted payment information against the expected order information.

---

# 7. Payment Verification Process

The current implementation follows this process:

```text
Payment submission
        ↓
Payment information stored
        ↓
Payment image uploaded
        ↓
OCR extracts text
        ↓
Extracted information is processed
        ↓
Payment information is compared
        ↓
Verification result
```

The OCR system uses **Tesseract** to extract text from the uploaded payment image.

The extracted text can contain information such as:

* Transaction/reference number
* Payment amount
* Bank/payment information
* Other readable information contained in the payment slip

---

# 8. Payment Image Verification

The backend provides a payment-image verification endpoint.

The implemented endpoint is:

```text
POST /payments/{payment_id}/verify-image
```

The endpoint receives a payment image and processes it using the OCR pipeline.

The extracted information is then used as part of the payment verification process.

---

# 9. Verification Philosophy

The system does not treat the uploaded screenshot itself as proof that a payment is genuine.

The payment image is treated as **submitted evidence**.

The system compares the extracted payment information with the information already stored for the payment/order.

For example:

```text
Order
Expected Amount: Rs. 25,000

Payment
Submitted Amount: Rs. 25,000

OCR
Extracted Amount: Rs. 25,000
```

This provides stronger evidence than simply checking whether an image was uploaded.

---

# 10. Payment Scenarios

The current implementation is designed around the main scenarios in the BuildStart challenge.

## Correct Payment

When the submitted payment information matches the expected payment information, the system can verify the payment successfully.

---

## Wrong Amount

Example:

```text
Expected Amount: 25,000
Payment Amount: 20,000
```

The payment does not satisfy the expected order amount and should not be treated as a valid payment.

---

## Duplicate Payment

The system stores payment transaction identifiers and payment records.

This provides a basis for detecting when an already-recorded transaction is submitted again.

---

## Reused Payment

Because payments are stored in the database and associated with orders, the system can identify payment records that have already been associated with another order.

A payment should not simply be treated as a new payment because a different image was submitted.

---

## Same Payment, Different Image

The system relies on payment information such as the transaction identifier rather than relying only on the image itself.

Therefore, submitting:

```text
Original screenshot
```

and later:

```text
Cropped photograph of the same payment
```

does not automatically make them two different payments.

---



# 11. Three Verification Outcomes

The system's verification workflow is designed around:

### APPROVED

The available information is sufficiently consistent with the expected payment.

### REJECTED

The available information indicates that the payment does not satisfy the required payment conditions.

Examples include:

* Incorrect amount
* Invalid/reused payment
* Conflicting payment information

---

# 12. Frontend

The frontend provides a business-facing interface for interacting with the payment verification system.

The interface allows the user to work with:

* Orders
* Payments
* Payment information
* Payment verification
* Payment image submission
* Verification results

The frontend communicates with the FastAPI backend through HTTP API requests.

---

# 13. Local Setup
Please use the given instructions in setup_instructions.txt to setup the project locally.
## Requirements

Install:

* Python 3.13
* PostgreSQL
* Node.js
* npm
* Git
* Tesseract OCR

Verify:

```bash
python --version
psql --version
node --version
npm --version
tesseract --version
git --version
```

---

# 14. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

---

# 15. PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE payment_verification;
```

Make sure PostgreSQL is running.

---

# 16. Backend Setup

Move into the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

On Windows activate it:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 17. Backend Environment

Create:

```text
backend/.env
```

Configure the PostgreSQL connection used by the application.

Example:

```text
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/payment_verification
```

Replace the username and password with the PostgreSQL credentials on the local machine.

Do not commit the real `.env` file to GitHub.

---

# 18. Tesseract Configuration

The OCR implementation uses Tesseract.

On Windows, the project may use:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is installed in another location, update the configuration accordingly.

Verify:

```bash
tesseract --version
```

---

# 19. Start the Backend

From:

```text
backend/
```

run:

```bash
uvicorn app.main:app --reload
```

If necessary:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 20. Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger allows the interviewer to directly test the implemented API.

The API can be used to inspect the order and payment workflow and test payment verification.

---

# 21. Frontend Setup

Open a **second terminal**.

From the project root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Configure the frontend API URL according to the environment configuration used by the frontend.

For a Vite configuration this may be:

```text
VITE_API_URL=http://127.0.0.1:8000
```

The important requirement is that the frontend points to the locally running FastAPI backend.

---

# 22. Start the Frontend

Run:

```bash
npm run dev
```

Vite will display the frontend URL.

Typically:

```text
http://localhost:5173
```

Open the URL shown in the terminal.

---

# 23. Running Backend and Frontend Together

### Terminal 1

```powershell
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

### Terminal 2

```bash
cd frontend
npm run dev
```

Then open the frontend URL.

---

# 24. Testing the Application

A basic demonstration flow is:

### Scenario 1 — Valid Payment

1. Select an order.
2. Submit the corresponding payment.
3. Upload the payment slip.
4. Run payment verification.
5. Review the verification result.

---

### Scenario 2 — Wrong Amount

Use a payment whose amount does not match the expected order amount.

Expected behavior:

```text
Payment amount does not match the expected order amount.
```

The payment should not be accepted as a valid payment.

---

### Scenario 3 — Duplicate / Reused Payment

Submit an already-used payment transaction again.

The system can use the stored transaction/payment information to identify the previously recorded payment.

---

### Scenario 4 — Unclear Payment Slip

Upload a poor-quality payment image.

The OCR process may fail to extract the required information.

The system should avoid automatically approving the payment when the evidence is insufficient.

---

# 25. Cost Considerations

The current prototype prioritizes inexpensive processing.

The OCR stage uses **Tesseract**, which can run locally rather than requiring an external AI API for every image.

This provides several advantages:

* No per-image AI API cost
* Lower processing cost
* Simple deployment
* Suitable for a prototype
* Deterministic OCR pipeline

The system can therefore use traditional processing for straightforward payment slips instead of automatically sending every image to an expensive multimodal AI model.

For difficult cases, a future version could introduce an AI-based fallback only when necessary.

---

# 26. Fraud Handling

The current design considers fraud scenarios including:

* Wrong payment amount
* Wrong receiving account
* Duplicate transaction
* Reused payment
* Same payment submitted through different images
* Old payment
* Unclear payment image
* Conflicting extracted information

The most important design principle is:

> A payment screenshot is evidence, not proof by itself.

The system therefore compares payment evidence with information already stored in the database.

---

# 28. Known Limitations

This is a two-day engineering challenge prototype rather than a production banking system.

Current limitations include:

### No Bank API

The challenge does not provide direct access to a bank transaction API.

Therefore, the system cannot independently query the bank and guarantee that every payment actually occurred.

### OCR Limitations

Tesseract OCR can produce incorrect or incomplete results when the payment image quality is poor.

### SMS Automation

The prototype does not have a direct connection to a bank's SMS infrastructure.

### Image Manipulation Detection

OCR and database validation alone cannot guarantee detection of every digitally manipulated payment screenshot.

### Production Scale

The current implementation is designed as a working prototype and would require additional infrastructure for very high payment volumes.

---

# 29. Production Improvements

If this system were taken to production, I would improve it in the following areas:

### Bank Integration

Integrate trusted bank transaction data where available.

### SMS Processing

Build bank-specific SMS parsers and an automated SMS ingestion service.

### Better Image Analysis

Use image-forensics or multimodal AI only for suspicious or difficult images.

### Background Processing

Move OCR and expensive verification operations into background workers.

### Scalability

Introduce:

* Multiple backend instances
* Job queues
* Object storage
* Database indexing
* Caching

### Monitoring

Add:

* Structured logging
* Error monitoring
* Verification metrics
* Fraud metrics
* Audit logs

### Human Review

Create a dedicated manual-review queue for:

```text
NEEDS VERIFICATION
```

cases.

---

# 30. Engineering Approach

The main engineering decision was to avoid treating payment verification as a simple:

```text
Image → OCR → Valid/Invalid
```

problem.

Instead, the system separates:

```text
Customer-submitted evidence
```

from:

```text
Information already known by the business
```

and uses the available information to determine whether the payment can safely be associated with an order.

The system also recognizes uncertainty.

If the available evidence is insufficient, the correct engineering decision is not to guess.

It is:

```text
NEEDS VERIFICATION
```

---

# 31. Challenge Requirement Coverage

| BuildStart Requirement        | Current Implementation                           |
| ----------------------------- | ------------------------------------------------ |
| Normal payment                | Order/payment verification workflow              |
| Wrong amount                  | Payment amount comparison                        |
| Wrong account                 | Payment/account validation where available       |
| Duplicate payment             | Transaction/payment record checking              |
| Reused payment                | Existing payment/order relationship              |
| Same payment, different image | Transaction-based payment identification         |
| Old payment                   | Existing payment records and payment information |
| Suspicious slip               | OCR/evidence consistency checks                  |
| Unclear image                 | OCR processing with uncertain result handling    |
| Conflicting evidence          | Payment information comparison                   |
| Missing evidence              | Verification cannot safely approve               |
| Similar payment amounts       | Payment information beyond amount is considered  |
| Payment slip images           | Implemented                                      |
| OCR                           | Implemented with Tesseract                       |
| Orders                        | Implemented                                      |
| Payments                      | Implemented                                      |
| PostgreSQL                    | Implemented                                      |
| Backend API                   | Implemented with FastAPI                         |
| Business UI                   | Implemented with frontend                        |
| Local setup                   | Documented above                                 |

---

# 32. Demo

The recommended demonstration should show:

1. A normal payment
2. A wrong amount
3. A duplicate/reused payment
4. An unclear payment image
5. A payment requiring further verification

The interviewer can also inspect the backend directly through:

```text
http://127.0.0.1:8000/docs
```

---

# 33. Deployed Application

The backend has also been configured for deployment using Render.

For local development, use:

```text
http://127.0.0.1:8000
```

For the deployed application, use the deployment URL provided with the submission.

The deployed backend uses the FastAPI entry point:

```text
app.main:app
```

with the production start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

# 34. Conclusion

This project focuses on building a practical payment-verification prototype within the two-day challenge constraints.

The core approach is:

```text
Order
  +
Payment
  +
Payment Image
  ↓
OCR
  ↓
Extract Payment Information
  ↓
Compare Against Stored Information
  ↓
Verification
```

The system prioritizes reliable evidence over blindly approving payments and provides a foundation that can be extended with bank SMS integration, stronger fraud detection, AI-assisted image analysis, and production-scale infrastructure.
