CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    position VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE team_leaders (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    assigned_to INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    assigned_by INTEGER REFERENCES team_leaders(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    priority VARCHAR(20) DEFAULT 'Medium',
    deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE task_updates (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    update_text TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    updated_by INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE performance_scores (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    task_completion_score INTEGER DEFAULT 0,
    timeliness_score INTEGER DEFAULT 0,
    quality_score INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



INSERT INTO employees (name, phone, email, position)
VALUES ('Rakibul', '9083480153', 'ri299850@gmail.com', 'Mis');


INSERT INTO team_leaders (employee_id, department)
VALUES (
    (SELECT id FROM employees WHERE phone = '9876543210'), -- or use email if phone is not unique
    'Sales'
);


INSERT INTO employees (name, phone, email, position) 
VALUES ('John Doe', '+1234567890', 'john@example.com', 'Developer');

INSERT INTO team_leaders (employee_id, department)
VALUES (1, 'IT');


INSERT INTO employees (name, phone, email, position)
VALUES ('John Doe', '9876543210', 'tagohn@example.com', 'Team Leader');

select * from team_leaders;
select * from employees;
delete from employees;


INSERT INTO employees (name, phone, email, position) VALUES
('Rakib', '+919083480153', 'alex.j@company.com', 'Senior Developer'),
('Maria Garcia', '+1222333444', 'maria.g@company.com', 'Productsa analyst');

INSERT INTO employees (name, phone, email, position) VALUES
('Raju', '+919163041321', 'raju@company.com', 'Accountant');

INSERT INTO team_leaders (employee_id, department) VALUES
(7, 'Product Development'); 

/* New Upadte date 02/08/2025 */
select * from employees;

delete from employees;
select * from team_leaders;
select * from performance_scores;
delete from performance_scores;
select * from tasks;
delete from tasks;
select * from task_updates;
select * from help_slips;
INSERT INTO employees (name, phone, email, position) VALUES
('Rakib', '+919083480153', 'ri299850@gmail.com', 'Data Analyst or Mis'),
('Raju', '+9147859612365', 'raju@gmail.com', 'Accountant'),
('Nikita', '+1222333444', 'nikita@gmail.com', 'Team Leader');
INSERT INTO team_leaders (employee_id, department) VALUES
(11, 'MD and Team Leader'); 



CREATE TABLE help_slips (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'Medium',
    status VARCHAR(20) DEFAULT 'Request Submitted',
    requester_id INTEGER REFERENCES employees(id),
    assigned_to_id INTEGER REFERENCES employees(id),
    resolved_by_id INTEGER REFERENCES employees(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    remarks TEXT,
    tat_hours FLOAT
);

-- Add comments to columns for documentation
COMMENT ON TABLE help_slips IS 'Table for tracking help requests and their resolution';
COMMENT ON COLUMN help_slips.priority IS 'Priority level: Low, Medium, High, Critical';
COMMENT ON COLUMN help_slips.status IS 'Current status: Request Submitted, In Progress, Resolved';
COMMENT ON COLUMN help_slips.tat_hours IS 'Turn-around time in hours from creation to resolution';


delete from help_slips;

select * from help_slips;



CREATE TABLE help_slips (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'Medium',
    contact_info VARCHAR(100),
    status VARCHAR(50) DEFAULT 'Request Submitted',
    assigned_to INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    remarks TEXT,
    resolved_by INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    resolve_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tat_hours DECIMAL(10,2)
);

CREATE INDEX idx_help_slip_status ON help_slips(status);
CREATE INDEX idx_help_slip_employee ON help_slips(employee_id);
CREATE INDEX idx_help_slip_assigned ON help_slips(assigned_to);



SELECT * FROM help_slips;



// 04-08-2025

select * from tasks;
DELETE FROM tasks
WHERE id=8;
DELETE FROM tasks
WHERE id=9;
DELETE FROM tasks
WHERE id=10;



DELETE FROM tasks
WHERE id=11;

DELETE FROM tasks
WHERE id=12;


select * from employees;


INSERT INTO employees (name, phone, email, position) VALUES
('Uma Yadav', '+918017255804', 'uma@gmail.com', 'Fornt Desk');

UPDATE employees
SET phone = '+919163041321'
WHERE id = 10;

