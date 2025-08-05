--app/database/connection.py


-- DROP in reverse dependency order
DROP TABLE IF EXISTS expense_issues CASCADE;
DROP TABLE IF EXISTS travel_tickets CASCADE;
DROP TABLE IF EXISTS expense_receipts CASCADE;
DROP TABLE IF EXISTS sub_expense_types CASCADE;
DROP TABLE IF EXISTS expense_caps CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS emp_categories CASCADE;
DROP TABLE IF EXISTS expense_types CASCADE;
DROP TABLE IF EXISTS expense_statuses CASCADE;


-- Create lookup/reference tables first
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE emp_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE expense_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE expense_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Now create sub_expense_types table

CREATE TABLE sub_expense_types(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  expense_type_id INT NOT NULL,
  created_from_receipt_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT fk_Expense_type_sub FOREIGN KEY (expense_type_id) REFERENCES expense_types(id) ON DELETE CASCADE,
  CONSTRAINT fk_receipt_origin FOREIGN KEY (created_from_receipt_id) REFERENCES expense_receipts(id) ON DELETE CASCADE
);

-- Now create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role_id INT NOT NULL,
    emp_category_id INT NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL,
    CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT,
    CONSTRAINT fk_emp_cat FOREIGN KEY (emp_category_id) REFERENCES emp_categories(id) ON DELETE RESTRICT
);

-- Create expense_receipts table

CREATE TABLE expense_receipts (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    expense_type_id INT NOT NULL,
    sub_expense_type_id INT,  -- NEW: optional FK
    amount NUMERIC(10, 2) NOT NULL,
    receipt_file_path TEXT NOT NULL,
    description TEXT,
    status_id INT DEFAULT 1,  -- Pending by default
    uploaded_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    approved_by INT,
    approved_at TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_expense_type FOREIGN KEY (expense_type_id) REFERENCES expense_types(id) ON DELETE RESTRICT,
    CONSTRAINT fk_status FOREIGN KEY (status_id) REFERENCES expense_statuses(id) ON DELETE RESTRICT,
    CONSTRAINT fk_approver FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_sub_expense_type FOREIGN KEY (sub_expense_type_id) REFERENCES sub_expense_types(id) ON DELETE SET NULL
);

-- Create expense_issues table
CREATE TABLE expense_issues (
    id SERIAL PRIMARY KEY,
    receipt_id INT NOT NULL,
    raised_by INT NOT NULL,
    issue_text TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_receipt_issue FOREIGN KEY (receipt_id) REFERENCES expense_receipts(id) ON DELETE CASCADE,
    CONSTRAINT fk_raised_by FOREIGN KEY (raised_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Create travel_tickets table
CREATE TABLE travel_tickets (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    from_location VARCHAR(100),
    to_location VARCHAR(100),
    travel_date DATE,
    purpose TEXT,
    status VARCHAR(50) DEFAULT 'raised',
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_travel_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE expense_caps (
    id SERIAL PRIMARY KEY,
    emp_category_id INT NOT NULL,
    expense_type_id INT NOT NULL,
    cap_amount NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_emp_cat_cap FOREIGN KEY (emp_category_id) REFERENCES emp_categories(id) ON DELETE CASCADE,
    CONSTRAINT fk_expense_type_cap FOREIGN KEY (expense_type_id) REFERENCES expense_types(id) ON DELETE CASCADE,
    UNIQUE (emp_category_id, expense_type_id)
);