### Step-by-Step Installation Instructions

**Make sure the instance Folder remove before run the application**

#### 1. **Set Up Your Project Environment**

1. **Create a Project Directory** (if you haven’t already):

    ```bash
    mkdir expense-sharing-application
    cd expense-sharing-application
    ```

2. **Create a Virtual Environment**:

    This isolates your project’s dependencies from other Python projects.

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:

    - On **Windows**:
      ```bash
      venv\Scripts\activate
      ```
    - On **macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```
#### 2. **Install the Required Packages**

1. **Install Packages from `requirements.txt`**:

    Run the following command to install all the required packages listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

#### 3. **Verify the Installation**

1. **Check Installed Packages**:

    Verify that the packages were installed correctly by listing them:

    ```bash
    pip list
    ```

#### 4. **Run Your Flask Application**
1. **Run the Flask Application**:

    ```bash
    python app.py
    ```

    This will start the Flask development server, and you can access your application at `http://127.0.0.1:5000`.

### Optional: Updating Dependencies

If you need to update packages in the future:

1. **Update Packages**:

    ```bash
    pip install --upgrade <package_name>
    ```
### Postman Cmd:

the Postman commands for testing the endpoints of your Flask application:
### 1. **Register a User**

- **Method**: `POST`
- **URL**: `http://127.0.0.1:5000/register`
- **Headers**:
  - `Content-Type: application/json`
- **Body** (raw JSON):

  ```json
  {
      "email": "test@example.com",
      "name": "Test User",
      "mobile_number": "1234567890",
      "password": "yourpassword"
  }
  ```

### 2. **Login to Get Access Token**

- **Method**: `POST`
- **URL**: `http://127.0.0.1:5000/login`
- **Headers**:
  - `Content-Type: application/json`
- **Body** (raw JSON):

  ```json
  {
      "email": "test@example.com",
      "password": "yourpassword"
  }
  ```

  **Response**:

  ```json
  {
      "access_token": "your_jwt_token_here"
  }
  ```

### 3. **Add an Expense**

- **Method**: `POST`
- **URL**: `http://127.0.0.1:5000/expenses`
- **Headers**:
  - `Authorization: Bearer your_jwt_token_here`
  - `Content-Type: application/json`
- **Body** (raw JSON):

  ```json
  {
      "description": "Dinner",
      "amount": 50.00,
      "split_method": "equal",
      "split_details": {
          "test@example.com": 25.00
      }
  }
  ```

### 4. **Get User Expenses**

- **Method**: `GET`
- **URL**: `http://127.0.0.1:5000/users/test@example.com/expenses`
- **Headers**:
  - `Authorization: Bearer your_jwt_token_here`

### 5. **Get Balance Sheet**

- **Method**: `GET`
- **URL**: `http://127.0.0.1:5000/expenses/balance_sheet`
- **Headers**:
  - `Authorization: Bearer your_jwt_token_here`

### 6. **Download Balance Sheet**

- **Method**: `GET`
- **URL**: `http://127.0.0.1:5000/expenses/balance_sheet/download`
- **Headers**:
  - `Authorization: Bearer your_jwt_token_here`

### Notes

- Replace `"your_jwt_token_here"` with the actual JWT token you get from the login response.
- Ensure your Flask application is running before sending requests through Postman.
- Adjust the URLs if your Flask application is running on a different port or domain.

With these Postman commands, you can effectively test your API endpoints.
