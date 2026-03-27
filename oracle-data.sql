-- DEPARTMENTS
INSERT INTO departments (department_id, department_name, location, budget) VALUES (1, 'Executive', 'New York', 500000);
INSERT INTO departments (department_id, department_name, location, budget) VALUES (2, 'Engineering', 'San Francisco', 800000);
INSERT INTO departments (department_id, department_name, location, budget) VALUES (3, 'Sales', 'Chicago', 400000);
INSERT INTO departments (department_id, department_name, location, budget) VALUES (4, 'Marketing', 'Los Angeles', 300000);
INSERT INTO departments (department_id, department_name, location, budget) VALUES (5, 'Human Resources', 'Seattle', 200000);
INSERT INTO departments (department_id, department_name, location, budget) VALUES (6, 'Finance', 'Boston', 250000);
INSERT INTO departments (department_id, department_name, location, budget) VALUES (7, 'IT Support', 'Austin', 180000);

-- EMPLOYEES
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (1, 'John', 'Smith', 'john.smith@company.com', '555-0101', TO_DATE('2019-01-15', 'YYYY-MM-DD'), 150000, 1, NULL, 'CEO');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (2, 'Sarah', 'Johnson', 'sarah.johnson@company.com', '555-0102', TO_DATE('2019-03-20', 'YYYY-MM-DD'), 120000, 2, 1, 'VP Engineering');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (3, 'Michael', 'Williams', 'michael.williams@company.com', '555-0103', TO_DATE('2019-05-10', 'YYYY-MM-DD'), 95000, 3, 1, 'VP Sales');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (4, 'Emily', 'Brown', 'emily.brown@company.com', '555-0104', TO_DATE('2020-02-01', 'YYYY-MM-DD'), 85000, 2, 2, 'Senior Developer');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (5, 'David', 'Jones', 'david.jones@company.com', '555-0105', TO_DATE('2020-04-15', 'YYYY-MM-DD'), 78000, 2, 2, 'Software Engineer');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (6, 'Jessica', 'Davis', 'jessica.davis@company.com', '555-0106', TO_DATE('2020-06-20', 'YYYY-MM-DD'), 72000, 2, 2, 'Software Engineer');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (7, 'Robert', 'Miller', 'robert.miller@company.com', '555-0107', TO_DATE('2020-08-10', 'YYYY-MM-DD'), 68000, 3, 3, 'Sales Manager');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (8, 'Jennifer', 'Wilson', 'jennifer.wilson@company.com', '555-0108', TO_DATE('2020-10-05', 'YYYY-MM-DD'), 65000, 3, 3, 'Sales Representative');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (9, 'James', 'Moore', 'james.moore@company.com', '555-0109', TO_DATE('2021-01-15', 'YYYY-MM-DD'), 70000, 4, 1, 'Marketing Director');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (10, 'Lisa', 'Taylor', 'lisa.taylor@company.com', '555-0110', TO_DATE('2021-03-20', 'YYYY-MM-DD'), 62000, 5, 1, 'HR Manager');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (11, 'William', 'Anderson', 'william.anderson@company.com', '555-0111', TO_DATE('2021-05-10', 'YYYY-MM-DD'), 68000, 6, 1, 'Finance Manager');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, salary, department_id, manager_id, job_title)
VALUES (12, 'Amanda', 'Thomas', 'amanda.thomas@company.com', '555-0112', TO_DATE('2021-07-15', 'YYYY-MM-DD'), 60000, 7, 2, 'IT Support Lead');

-- PROJECTS
INSERT INTO projects (project_id, project_name, description, start_date, end_date, budget, status, department_id)
VALUES (1, 'Cloud Migration', 'Migrate legacy systems to AWS cloud infrastructure', TO_DATE('2023-01-01', 'YYYY-MM-DD'), TO_DATE('2024-06-30', 'YYYY-MM-DD'), 500000, 'IN_PROGRESS', 2);
INSERT INTO projects (project_id, project_name, description, start_date, end_date, budget, status, department_id)
VALUES (2, 'Mobile App v2', 'Complete redesign of mobile application with new UX', TO_DATE('2023-03-01', 'YYYY-MM-DD'), TO_DATE('2024-03-31', 'YYYY-MM-DD'), 350000, 'IN_PROGRESS', 2);
INSERT INTO projects (project_id, project_name, description, start_date, end_date, budget, status, department_id)
VALUES (3, 'Q4 Marketing Campaign', 'Year-end marketing push with social media focus', TO_DATE('2023-10-01', 'YYYY-MM-DD'), TO_DATE('2023-12-31', 'YYYY-MM-DD'), 150000, 'COMPLETED', 4);
INSERT INTO projects (project_id, project_name, description, start_date, end_date, budget, status, department_id)
VALUES (4, 'Sales CRM Upgrade', 'Upgrade CRM system for improved sales tracking', TO_DATE('2023-06-01', 'YYYY-MM-DD'), TO_DATE('2024-01-31', 'YYYY-MM-DD'), 200000, 'IN_PROGRESS', 3);
INSERT INTO projects (project_id, project_name, description, start_date, end_date, budget, status, department_id)
VALUES (5, 'Security Audit', 'Annual security audit and compliance review', TO_DATE('2024-01-15', 'YYYY-MM-DD'), TO_DATE('2024-04-15', 'YYYY-MM-DD'), 100000, 'PLANNING', 7);

-- PROJECT_ASSIGNMENTS
INSERT INTO project_assignments (assignment_id, project_id, employee_id, role, assigned_date)
VALUES (1, 1, 4, 'Tech Lead', TO_DATE('2023-01-01', 'YYYY-MM-DD'));
INSERT INTO project_assignments (assignment_id, project_id, employee_id, role, assigned_date)
VALUES (2, 1, 5, 'Senior Developer', TO_DATE('2023-01-01', 'YYYY-MM-DD'));
INSERT INTO project_assignments (assignment_id, project_id, employee_id, role, assigned_date)
VALUES (3, 1, 6, 'Developer', TO_DATE('2023-02-01', 'YYYY-MM-DD'));
INSERT INTO project_assignments (assignment_id, project_id, employee_id, role, assigned_date)
VALUES (4, 2, 5, 'Tech Lead', TO_DATE('2023-03-01', 'YYYY-MM-DD'));
INSERT INTO project_assignments (assignment_id, project_id, employee_id, role, assigned_date)
VALUES (5, 2, 6, 'Developer', TO_DATE('2023-03-01', 'YYYY-MM-DD'));
INSERT INTO project_assignments (assignment_id, project_id, employee_id, role, assigned_date)
VALUES (6, 2, 12, 'QA Lead', TO_DATE('2023-04-01', 'YYYY-MM-DD'));
INSERT INTO project_assignments (assignment_id, project_id, employee_id, role, assigned_date)
VALUES (7, 4, 7, 'Project Manager', TO_DATE('2023-06-01', 'YYYY-MM-DD'));
INSERT INTO project_assignments (assignment_id, project_id, employee_id, role, assigned_date)
VALUES (8, 4, 8, 'Sales Analyst', TO_DATE('2023-06-15', 'YYYY-MM-DD'));

-- CUSTOMERS
INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, city, state, country, postal_code, credit_limit, registration_date)
VALUES (1, 'Alice', 'Anderson', 'alice@email.com', '555-1001', '123 Main Street', 'New York', 'NY', 'USA', '10001', 10000, TO_DATE('2022-01-15', 'YYYY-MM-DD'));
INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, city, state, country, postal_code, credit_limit, registration_date)
VALUES (2, 'Bob', 'Baker', 'bob@email.com', '555-1002', '456 Oak Avenue', 'Los Angeles', 'CA', 'USA', '90001', 15000, TO_DATE('2022-02-20', 'YYYY-MM-DD'));
INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, city, state, country, postal_code, credit_limit, registration_date)
VALUES (3, 'Carol', 'Clark', 'carol@email.com', '555-1003', '789 Pine Road', 'Chicago', 'IL', 'USA', '60601', 8000, TO_DATE('2022-03-25', 'YYYY-MM-DD'));
INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, city, state, country, postal_code, credit_limit, registration_date)
VALUES (4, 'Dan', 'Davis', 'dan@email.com', '555-1004', '321 Elm Drive', 'Houston', 'TX', 'USA', '77001', 12000, TO_DATE('2022-04-30', 'YYYY-MM-DD'));
INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, city, state, country, postal_code, credit_limit, registration_date)
VALUES (5, 'Eve', 'Evans', 'eve@email.com', '555-1005', '654 Maple Lane', 'Phoenix', 'AZ', 'USA', '85001', 7000, TO_DATE('2022-05-15', 'YYYY-MM-DD'));
INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, city, state, country, postal_code, credit_limit, registration_date)
VALUES (6, 'Frank', 'Foster', 'frank@email.com', '555-1006', '987 Cedar Court', 'Philadelphia', 'PA', 'USA', '19101', 9000, TO_DATE('2022-06-20', 'YYYY-MM-DD'));
INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, city, state, country, postal_code, credit_limit, registration_date)
VALUES (7, 'Grace', 'Garcia', 'grace@email.com', '555-1007', '135 Birch Way', 'San Antonio', 'TX', 'USA', '78201', 11000, TO_DATE('2022-07-10', 'YYYY-MM-DD'));
INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, city, state, country, postal_code, credit_limit, registration_date)
VALUES (8, 'Henry', 'Harris', 'henry@email.com', '555-1008', '246 Walnut Street', 'San Diego', 'CA', 'USA', '92101', 13000, TO_DATE('2022-08-15', 'YYYY-MM-DD'));

-- PRODUCTS
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (1, 'Laptop Pro 15', 'High-performance laptop with 15-inch display', 'Electronics', 1299.99, 50, 10, 1, 0);
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (2, 'Wireless Mouse Pro', 'Ergonomic wireless mouse with precision tracking', 'Accessories', 49.99, 200, 50, 1, 0);
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (3, 'USB-C Hub 7-in-1', 'Multi-port USB-C hub with HDMI and card reader', 'Accessories', 79.99, 150, 30, 1, 0);
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (4, 'Monitor Ultra 27"', '4K UHD monitor with HDR support', 'Electronics', 499.99, 75, 15, 2, 0);
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (5, 'Mechanical Keyboard RGB', 'RGB mechanical keyboard with Cherry MX switches', 'Accessories', 149.99, 100, 25, 2, 0);
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (6, 'Webcam HD Pro', '1080p webcam with autofocus and noise cancellation', 'Electronics', 89.99, 120, 20, 1, 0);
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (7, 'Laptop Stand Aluminum', 'Adjustable aluminum laptop stand', 'Accessories', 39.99, 180, 40, 3, 0);
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (8, 'Noise Cancelling Headphones', 'Premium wireless headphones with ANC', 'Electronics', 299.99, 60, 15, 2, 0);
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (9, 'External SSD 1TB', 'Portable SSD with USB 3.2', 'Storage', 119.99, 90, 20, 1, 0);
INSERT INTO products (product_id, product_name, description, category, unit_price, units_in_stock, units_on_order, supplier_id, discontinued)
VALUES (10, 'USB Flash Drive 128GB', 'High-speed USB 3.1 flash drive', 'Storage', 24.99, 300, 100, 3, 0);

-- ORDERS
INSERT INTO orders (order_id, customer_id, order_date, required_date, shipped_date, total_amount, status, shipping_method, shipping_address)
VALUES (1, 1, TO_DATE('2023-06-15', 'YYYY-MM-DD'), TO_DATE('2023-06-22', 'YYYY-MM-DD'), TO_DATE('2023-06-20', 'YYYY-MM-DD'), 1399.98, 'DELIVERED', 'Standard', '123 Main Street, New York, NY 10001');
INSERT INTO orders (order_id, customer_id, order_date, required_date, shipped_date, total_amount, status, shipping_method, shipping_address)
VALUES (2, 2, TO_DATE('2023-06-20', 'YYYY-MM-DD'), TO_DATE('2023-06-27', 'YYYY-MM-DD'), TO_DATE('2023-06-25', 'YYYY-MM-DD'), 549.98, 'DELIVERED', 'Express', '456 Oak Avenue, Los Angeles, CA 90001');
INSERT INTO orders (order_id, customer_id, order_date, required_date, shipped_date, total_amount, status, shipping_method, shipping_address)
VALUES (3, 3, TO_DATE('2023-07-01', 'YYYY-MM-DD'), TO_DATE('2023-07-08', 'YYYY-MM-DD'), NULL, 229.98, 'PROCESSING', 'Standard', '789 Pine Road, Chicago, IL 60601');
INSERT INTO orders (order_id, customer_id, order_date, required_date, shipped_date, total_amount, status, shipping_method, shipping_address)
VALUES (4, 1, TO_DATE('2023-07-10', 'YYYY-MM-DD'), TO_DATE('2023-07-17', 'YYYY-MM-DD'), NULL, 79.99, 'PENDING', 'Standard', '123 Main Street, New York, NY 10001');
INSERT INTO orders (order_id, customer_id, order_date, required_date, shipped_date, total_amount, status, shipping_method, shipping_address)
VALUES (5, 4, TO_DATE('2023-07-15', 'YYYY-MM-DD'), TO_DATE('2023-07-22', 'YYYY-MM-DD'), TO_DATE('2023-07-20', 'YYYY-MM-DD'), 899.98, 'DELIVERED', 'Express', '321 Elm Drive, Houston, TX 77001');
INSERT INTO orders (order_id, customer_id, order_date, required_date, shipped_date, total_amount, status, shipping_method, shipping_address)
VALUES (6, 5, TO_DATE('2023-07-20', 'YYYY-MM-DD'), TO_DATE('2023-07-27', 'YYYY-MM-DD'), NULL, 149.99, 'SHIPPED', 'Standard', '654 Maple Lane, Phoenix, AZ 85001');
INSERT INTO orders (order_id, customer_id, order_date, required_date, shipped_date, total_amount, status, shipping_method, shipping_address)
VALUES (7, 6, TO_DATE('2023-07-25', 'YYYY-MM-DD'), TO_DATE('2023-08-01', 'YYYY-MM-DD'), NULL, 339.98, 'PROCESSING', 'Express', '987 Cedar Court, Philadelphia, PA 19101');
INSERT INTO orders (order_id, customer_id, order_date, required_date, shipped_date, total_amount, status, shipping_method, shipping_address)
VALUES (8, 7, TO_DATE('2023-08-01', 'YYYY-MM-DD'), TO_DATE('2023-08-08', 'YYYY-MM-DD'), NULL, 499.99, 'PENDING', 'Standard', '135 Birch Way, San Antonio, TX 78201');

-- ORDER_ITEMS
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (1, 1, 1, 'Laptop Pro 15', 1, 1299.99, 0);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (2, 1, 2, 'Wireless Mouse Pro', 2, 49.99, 0);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (3, 2, 4, 'Monitor Ultra 27"', 1, 499.99, 0);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (4, 2, 3, 'USB-C Hub 7-in-1', 1, 79.99, 10);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (5, 3, 5, 'Mechanical Keyboard RGB', 1, 149.99, 15);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (6, 3, 6, 'Webcam HD Pro', 1, 89.99, 5);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (7, 4, 3, 'USB-C Hub 7-in-1', 1, 79.99, 0);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (8, 5, 1, 'Laptop Pro 15', 1, 1299.99, 30);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (9, 5, 2, 'Wireless Mouse Pro', 2, 49.99, 0);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (10, 6, 5, 'Mechanical Keyboard RGB', 1, 149.99, 0);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (11, 7, 8, 'Noise Cancelling Headphones', 1, 299.99, 0);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (12, 7, 9, 'External SSD 1TB', 1, 119.99, 20);
INSERT INTO order_items (item_id, order_id, product_id, product_name, quantity, unit_price, discount)
VALUES (13, 8, 4, 'Monitor Ultra 27"', 1, 499.99, 0);

COMMIT;
