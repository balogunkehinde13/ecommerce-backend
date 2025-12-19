# E-commerce Product API

A comprehensive RESTful API built with Django and Django REST Framework for managing products in an e-commerce platform. This API provides complete product management, user authentication, advanced search, and filtering capabilities.

## 🚀 Features

### Core Functionality
- ✅ **Product Management** - Full CRUD operations for products
- ✅ **User Authentication** - JWT token-based authentication system
- ✅ **Category Management** - Organize products by categories
- ✅ **Advanced Search** - Search products by name, description, or category
- ✅ **Filtering** - Filter by category, price range, and stock availability
- ✅ **Pagination** - Efficient handling of large datasets
- ✅ **Image Upload** - Support for product images

### Product Features
- Name, description, price, category
- Stock quantity management
- Image URL or file upload support
- Availability status tracking
- Automatic timestamp tracking

### Security
- JWT authentication with token refresh
- Password validation and hashing
- Permission-based access control
- CORS configuration for frontend integration

# Authentication & Authorization

This project uses **JSON Web Token (JWT)–based authentication** to secure the API and control access to protected resources.

---

## Authentication Method

JWT authentication is implemented using **Django REST Framework SimpleJWT**.  
When a user logs in with valid credentials, the server generates a signed access token. This token is included in subsequent API requests to verify the user’s identity.

Tokens are sent using the standard HTTP header format:

Authorization: Bearer <access_token>

yaml
Copy code

The term **Bearer** indicates that any client presenting a valid token is authorized to access protected endpoints.

---

## Why JWT Was Chosen

JWT authentication was selected because it:

- Is **stateless**, making it scalable and suitable for REST APIs  
- Works well with **frontend applications and mobile clients**  
- Avoids **server-side session storage**  
- Is widely adopted in **production-grade APIs**

---

## Authorization Rules

The API uses permission classes to control access:

- **Public access** is allowed for read-only endpoints  
  (e.g., viewing products and categories)
- **Authenticated access** is required for sensitive operations such as:
  - Creating, updating, or deleting products  
  - Managing carts and wishlists  
  - Placing orders  
  - Submitting product reviews  

This is enforced using Django REST Framework permission classes such as:

```python
IsAuthenticated
IsAuthenticatedOrReadOnly
Security Considerations
```
Tokens have a limited lifespan and must be refreshed periodically

Passwords are securely hashed using Django’s built-in authentication system

Authentication logic is centralized, ensuring consistent security across all apps

Summary
By using JWT-based authentication with proper permission controls, the API ensures secure access to user-specific and sensitive resources while maintaining flexibility and scalability for future frontend or mobile integrations.

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🛠️ Requirements

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Python Packages

```
Django==5.0.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
django-filter==23.5
Pillow==10.1.0
python-decouple==3.8
```

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/balogunkehinde13/ecommerce-api.git
cd ecommerce-api
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## ⚙️ Configuration

### Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it into your `.env` file.

## 🗄️ Database Setup

### 1. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 3. Create Media Directory

```bash
mkdir media
mkdir media/products
```

## 🏃 Running the Server

### Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

### Admin Panel

Access the Django admin panel at: `http://127.0.0.1:8000/admin/`

Login with your superuser credentials.

## 📚 API Documentation

### Base URL

```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

#### Register User
```http
POST /api/accounts/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "message": "User registered successfully"
}
```

#### Login (Get Token)
```http
POST /api/token/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Get User Profile
```http
GET /api/accounts/profile/
Authorization: Bearer <access_token>
```

### Category Endpoints

#### List All Categories
```http
GET /api/categories/
```

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Electronics",
      "description": "Electronic devices and gadgets",
      "product_count": 15,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Category
```http
POST /api/categories/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Electronics",
  "description": "Electronic devices and gadgets"
}
```

#### Get Category Details
```http
GET /api/categories/{id}/
```

#### Update Category
```http
PUT /api/categories/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Electronics",
  "description": "Updated description"
}
```

#### Delete Category
```http
DELETE /api/categories/{id}/
Authorization: Bearer <access_token>
```

### Product Endpoints

#### List All Products
```http
GET /api/products/
```

**Query Parameters:**
- `page` - Page number (default: 1)
- `search` - Search term
- `category` - Filter by category name
- `min_price` - Minimum price
- `max_price` - Maximum price
- `in_stock` - Filter by stock availability (true/false)
- `ordering` - Sort by field (price, -price, name, -created_date)

**Example:**
```http
GET /api/products/?search=laptop&min_price=500&max_price=2000&ordering=-price
```

**Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Gaming Laptop",
      "description": "High-performance gaming laptop",
      "price": "1499.99",
      "category": 1,
      "category_name": "Electronics",
      "stock_quantity": 15,
      "image_url": "https://example.com/laptop.jpg",
      "image": null,
      "created_date": "2024-01-15T10:30:00Z",
      "updated_date": "2024-01-15T10:30:00Z",
      "created_by": 1,
      "created_by_username": "admin",
      "is_available": true,
      "in_stock": true
    }
  ]
}
```

#### Create Product
```http
POST /api/products/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Gaming Laptop",
  "description": "High-performance gaming laptop with RTX 4080",
  "price": "1499.99",
  "category": 1,
  "stock_quantity": 15,
  "image_url": "https://example.com/laptop.jpg",
  "is_available": true
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Gaming Laptop",
  "description": "High-performance gaming laptop with RTX 4080",
  "price": "1499.99",
  "category": 1,
  "stock_quantity": 15,
  "image_url": "https://example.com/laptop.jpg",
  "is_available": true
}
```

#### Get Product Details
```http
GET /api/products/{id}/
```

#### Update Product
```http
PUT /api/products/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Gaming Laptop",
  "description": "Updated description",
  "price": "1399.99",
  "category": 1,
  "stock_quantity": 20,
  "is_available": true
}
```

#### Partial Update Product
```http
PATCH /api/products/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "price": "1299.99",
  "stock_quantity": 25
}
```

#### Delete Product
```http
DELETE /api/products/{id}/
Authorization: Bearer <access_token>
```

#### Advanced Search
```http
GET /api/products/search/?q=laptop&category=Electronics&min_price=500
```

#### Get Products by Category
```http
GET /api/products/by_category/?name=Electronics
```

#### Get Available Products Only
```http
GET /api/products/available/
```

## 🧪 Testing

### Using cURL

**Register a user:**
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'
```

**Create a product:**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Test Product",
    "description": "A test product",
    "price": "99.99",
    "category": 1,
    "stock_quantity": 10
  }'
```

**Search products:**
```bash
curl http://localhost:8000/api/products/search/?q=laptop
```

### Using Postman

1. Import the API endpoints into Postman
2. Set up an environment variable for `base_url` = `http://127.0.0.1:8000`
3. Create an environment variable for `access_token` after login
4. Use `{{access_token}}` in Authorization headers

### Run Django Tests

```bash
python manage.py test
```

## 🚀 Deployment

### Heroku Deployment

#### 1. Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

#### 2. Create Heroku App

```bash
heroku login
heroku create your-app-name
```

#### 3. Add Procfile

Create `Procfile` in root directory:

```
web: gunicorn ecommerce_api.wsgi --log-file -
```

#### 4. Install Gunicorn

```bash
pip install gunicorn
pip freeze > requirements.txt
```

#### 5. Update Settings for Production

In `settings.py`:

```python
import dj_database_url

# Update ALLOWED_HOSTS
ALLOWED_HOSTS = ['your-app-name.herokuapp.com', 'localhost']

# Add PostgreSQL database
DATABASES['default'] = dj_database_url.config(
    conn_max_age=600,
    conn_health_checks=True,
)

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

#### 6. Deploy

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### PythonAnywhere Deployment

1. Create an account at https://www.pythonanywhere.com
2. Upload your code via Git or file upload
3. Create a virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Configure WSGI file to point to your Django app
6. Set up static files in the web app configuration
7. Reload your web app

## 📁 Project Structure

```
ecommerce-api/
├── ecommerce_api/          # Main project directory
│   ├── __init__.py
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── accounts/              # User management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py     # User serializers
│   ├── views.py           # User views
│   └── urls.py            # User URLs
├── products/              # Product management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Product model
│   ├── serializers.py     # Product serializers
│   ├── views.py           # Product views
│   ├── filters.py         # Custom filters
│   └── urls.py            # Product URLs
├── categories/            # Category management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Category model
│   ├── serializers.py     # Category serializers
│   ├── views.py           # Category views
│   └── urls.py            # Category URLs
├── media/                 # User uploaded files
│   └── products/          # Product images
├── static/                # Static files
├── venv/                  # Virtual environment (not in git)
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore file
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment
└── README.md            # This file
```

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Add it to `.gitignore`
2. **Use strong SECRET_KEY** - Generate a new one for production
3. **Set DEBUG=False in production** - Never run with DEBUG=True in production
4. **Update ALLOWED_HOSTS** - Specify your domain
5. **Use HTTPS** - Enable SSL/TLS in production
6. **Regular updates** - Keep dependencies updated
7. **Rate limiting** - Implement API rate limiting for production

## 📝 Common Issues & Solutions

### Issue: Module not found

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Database migrations error

**Solution:**
```bash
python manage.py makemigrations --empty appname
python manage.py migrate
```

### Issue: Static files not loading

**Solution:**
```bash
python manage.py collectstatic
```

### Issue: CORS errors from frontend

**Solution:** Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `settings.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Kehinde** - *Initial work* - [Github](https://github.com/balogunkehinde13)

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- All contributors and supporters

## 📞 Contact

Project Link: [https://github.com/balogunkehinde13/ecommerce-api](https://github.com/balogunkehinde13/ecommerce-api)

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using Django & Django REST Framework**