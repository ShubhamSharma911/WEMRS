# WEMRS - Workforce Expense Management & Receipt System (Backend)

## Project Overview
WEMRS is a scalable backend system for workforce expense management. It enables employees to upload expense receipts (images or PDFs), extracts and validates receipt data using OCR, and applies policy-based capping logic based on employee categories and expense types. The system is designed for extensibility, supporting both merchant and payment receipts, and is built with modern Python best practices.

## Features
- **FastAPI-based RESTful API**
- **PostgreSQL** database with **SQLAlchemy Core** (no ORM)
- Upload and storage of expense receipts (images, PDFs)
- **Tesseract OCR** and **pdf2image** for text extraction from receipts
- **Strategy + Factory + Service** architecture for receipt processing and capping logic
- **Role-based JWT authentication** (`EMPLOYEE`, `ADMIN`, `SUPER_ADMIN`)
- Modular logging (file and console) and HTTP request logging middleware
- **Conda environment** for reproducible dependency management
- Seed scripts for roles, categories, statuses, and demo users
- Designed for easy extension to ML-based OCR (e.g., LayoutLM) in future phases
- Testable with **pytest** (test cases to be added)

## Technologies Used
- Python 3.11
- FastAPI
- SQLAlchemy Core
- PostgreSQL
- Tesseract OCR (system dependency)
- pdf2image, Pillow, pytesseract (Python OCR stack)
- passlib, python-jose (security)
- Uvicorn (ASGI server)
- Conda (environment management)
- Pytest (testing, planned)

## Folder Structure
```text
app/
  controllers/         # API endpoints (auth, user, upload, capping)
  database/            # DB connection, schema, seed data
  factories/           # Factory for capping strategies
  models/              # User roles, enums, and models
  ocr/                 # OCR engine abstraction and Tesseract implementation
  repositories/        # Data access for users, receipts, caps, etc.
  schemas/             # Pydantic schemas for validation
  security/            # Hashing and JWT helpers
  services/            # Business logic for auth, upload, capping, users
  strategies/          # Capping strategy interface and DB implementation
  utils/               # Logger, file utils, JWT, request utils, etc.
  views/               # (Reserved for route definitions)
  xyz.py               # (Sample/utility file)
config.py              # App configuration (uses .env)
environment.yml        # Conda environment (all dependencies)
requirements.txt       # pip dependencies (for pip installs)
init_seed.py           # Script to initialize/seed the database
logs/                  # Log files (created at runtime)
uploaded_receipts/     # Uploaded receipt files
```

## Setup Instructions
1. **Clone the repository:**
   ```sh
git clone <repo-url>
cd WEMRS
```
2. **Create and activate the Conda environment:**
   ```sh
conda env create -f environment.yml
conda activate wemrs-env
```
3. **(Optional) Install pip-only dependencies:**
   ```sh
pip install -r requirements.txt
```
4. **Set up your environment variables:**
   - Copy `.env.example` to `.env` and fill in your PostgreSQL and JWT settings.
   - Required variables (see `config.py`):
     - `database_hostname`, `database_port`, `database_name`, `database_username`, `database_password`, `secret_key`, `algorithm`, `access_token_expire_minutes`
5. **Initialize the database and seed data:**
   ```sh
python init_seed.py
```
   (This will create tables and insert default roles, categories, statuses, and demo users.)
6. **Run the FastAPI server:**
   ```sh
uvicorn app.main:app --reload
```
7. **Access the API docs:**
   [http://localhost:8000/docs](http://localhost:8000/docs)

## Logging
- All logs are written to the `logs/app.log` file and also output to the console.
- HTTP requests are logged via FastAPI middleware (see `app/main.py`).
- Logging is handled by `app/utils/logger.py`.

## Testing
- Test cases are (or will be) written using **pytest**.
- To run tests (once available):
   ```sh
pytest
```

## Receipt Upload & OCR
- Receipts (images or PDFs) are uploaded via the `/upload/` endpoint.
- **Tesseract OCR** and **pdf2image** are used to extract text from receipts.
- **System requirements:**
  - Tesseract OCR must be installed and available in your PATH.
  - For PDF support, poppler-utils must be installed (for pdf2image).
- Uploaded files are saved in the `uploaded_receipts/` directory.

## Authentication & Roles
- JWT-based authentication with three roles: `EMPLOYEE`, `ADMIN`, `SUPER_ADMIN`.
- Role-based access control is enforced on all endpoints.
- Default demo users are seeded (see `app/database/seed_data.py`).

## Capping Logic & Extensibility
- Capping logic is implemented using the **Strategy + Factory + Service** pattern.
- Easily extendable to support new capping policies or receipt types.
- Designed to support both merchant and payment receipts with minimal changes.
- OCR engine is abstracted (see `app/ocr/base_ocr_engine.py`) for future ML-based engines (e.g., LayoutLM, Donut, etc.).

## Planned Future Enhancements
- ML-based receipt parsing (LayoutLM, Donut, etc.) for improved accuracy.
- More granular test coverage with pytest.
- Advanced analytics and reporting endpoints.

## Contact & Support
For questions, issues, or contributions, please contact the project maintainer. 