# 👕 WearHub - Complete E-commerce Platform

<div align="center">
  <img src="https://via.placeholder.com/200x200.png?text=WearHub" alt="WearHub Logo" width="200"/>
  
  [![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
  [![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://djangoproject.com)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://postgresql.org)
  [![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation Guide](#-installation-guide)
- [Configuration](#-configuration)
- [Running the Project](#-running-the-project)
- [Docker Setup](#-docker-setup)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🎯 Project Overview

**WearHub** is a full-featured e-commerce platform built with Django. It provides a seamless shopping experience for customers while offering powerful management tools for distributors and administrators. The platform supports multi-user roles, product management, cart functionality, order processing, and payment simulation.

### 👥 User Roles

1. **Consumer**: Browse products, add to cart, place orders, track orders
2. **Distributor**: Add/manage products, track inventory, view orders
3. **Admin**: Full system control, user management, approve distributors

## ✨ Features

### ✅ Implemented Features

#### User Module
- User registration with email verification
- Role-based authentication (Consumer/Distributor/Admin)
- Profile management with avatar upload
- Password reset via email
- Multiple address management

#### Product Module
- Product catalog with categories and subcategories
- Product search and filtering
- Product variants (size, color)
- Multiple product images
- Product reviews and ratings
- Wishlist functionality

#### Cart Module
- Add/remove items from cart
- Update quantities
- Session-based cart for guests
- Cart persistence after login
- AJAX cart updates

#### Order Module
- Checkout process with address selection
- Order confirmation emails
- Order history for users
- Order tracking (Pending, Confirmed, Shipped, Delivered)
- Order cancellation (for pending orders)

#### Payment Module
- Dummy payment gateway simulation
- Configurable success/failure rate
- Payment status tracking
- Transaction history

#### Distributor Dashboard
- Add/Edit/Delete products
- Product image management
- Inventory tracking
- Sales overview

#### Admin Panel
- Full Django admin interface
- User management and approval
- Product management
- Order management
- Coupon management

#### API (REST Framework)
- Product API endpoints
- Cart API
- Order API
- JWT Authentication

#### Additional Features
- Responsive design (Bootstrap 5)
- Email notifications
- Coupon system
- Related products
- Product pagination
- Advanced filtering
- Search functionality

## 🛠 Tech Stack

### Backend
- **Python 3.11** - Core programming language
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **JWT** - Authentication
- **Celery** - Async tasks (optional)

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript (ES6+)** - Client-side logic
- **Bootstrap 5** - UI framework
- **Font Awesome** - Icons
- **jQuery** - DOM manipulation

### DevOps
- **Docker** - Containerization
- **Git** - Version control
- **GitHub Actions** - CI/CD (optional)

### Development Tools
- **VS Code** - IDE
- **pgAdmin** - Database management
- **Postman** - API testing

## 📁 Project Structure

```
WearHub/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── wearhub/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── products/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── cart/
│   ├── migrations/
│   ├── __init__.py
│   ├── context_processors.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
├── orders/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── payment/
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── api/
│   ├── __init__.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── migrations/
│   ├── __init__.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── media/
│   ├── products/
│   ├── profiles/
│   └── categories/
├── templates/
│   ├── base.html
│   ├── includes/
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── product_card.html
│   ├── accounts/
│   ├── products/
│   ├── cart/
│   ├── orders/
│   ├── payment/
│   └── core/
└── utils/
    └── helpers.py
```

## 📦 Installation Guide

### Prerequisites
- Python 3.11 or higher
- PostgreSQL (or SQLite for development)
- Git (optional)
- VS Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/wearhub.git
cd wearhub
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

#### Option A: SQLite (Quick Development)
```bash
# No setup required - Django will create it automatically
```

#### Option B: PostgreSQL (Production)

Create a PostgreSQL database:
```sql
CREATE DATABASE wearhub;
CREATE USER wearhub_user WITH PASSWORD 'yourpassword';
ALTER ROLE wearhub_user SET client_encoding TO 'utf8';
ALTER ROLE wearhub_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE wearhub_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE wearhub TO wearhub_user;
```

### Step 5: Environment Configuration

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` file:
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for PostgreSQL)
DATABASE_URL=postgresql://wearhub_user:yourpassword@localhost:5432/wearhub

# For SQLite (comment above and uncomment below)
# DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration (for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# For production:
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# DEFAULT_FROM_EMAIL=WearHub <noreply@wearhub.com>

# Admin Email
ADMIN_EMAIL=admin@wearhub.com

# Payment Simulation
PAYMENT_SUCCESS_RATE=80
```

### Step 6: Run Migrations

```bash
python manage.py makemigrations accounts products cart orders payment
python manage.py migrate
```

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 8: Load Initial Data (Optional)

```bash
python manage.py loaddata initial_data
# OR run custom script
python create_categories.py
```

### Step 9: Collect Static Files

```bash
python manage.py collectstatic
```

### Step 10: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the application.

## 🐳 Docker Setup

### Using Docker Compose (Recommended)

```bash
# Build and start containers
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop containers
docker-compose down
```

### Using Docker Only

```bash
# Build image
docker build -t wearhub .

# Run container
docker run -p 8000:8000 wearhub
```

## 🚀 Usage Guide

### Consumer Guide

1. **Register/Login**
   - Visit `/accounts/register/`
   - Choose "Consumer"
   - Fill registration form
   - Verify email (check console)

2. **Browse Products**
   - Visit home page or `/products/`
   - Use filters and search
   - Click on products for details

3. **Shopping Cart**
   - Add items to cart
   - View cart at `/cart/`
   - Update quantities
   - Proceed to checkout

4. **Place Order**
   - Fill shipping address
   - Choose payment method
   - Confirm order
   - View order history

### Distributor Guide

1. **Register as Distributor**
   - Visit `/accounts/register/`
   - Choose "Distributor"
   - Fill business details
   - Wait for admin approval

2. **Get Approved**
   - Admin must approve your account
   - Check email for notification

3. **Add Products**
   - Login and go to dashboard
   - Click "Add New Product"
   - Fill product details
   - Upload images
   - Submit

4. **Manage Products**
   - View all products in dashboard
   - Edit or delete products
   - Track inventory

### Admin Guide

1. **Login to Admin Panel**
   - Visit `/admin/`
   - Use superuser credentials

2. **Manage Users**
   - Approve distributors
   - Activate/deactivate users
   - View user details

3. **Manage Products**
   - Add/edit/delete any product
   - Manage categories
   - Feature products

4. **Manage Orders**
   - View all orders
   - Update order status
   - Process refunds

## 📚 API Documentation

### Authentication

```http
POST /api/auth/login/
{
    "username": "user",
    "password": "pass"
}

POST /api/auth/register/
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "pass123"
}
```

### Products API

```http
GET /api/products/
GET /api/products/{id}/
GET /api/products/?category=men&min_price=500
POST /api/products/{id}/reviews/
```

### Cart API

```http
GET /api/cart/
POST /api/cart/add/
{
    "product_id": 1,
    "quantity": 2
}
POST /api/cart/update/
{
    "item_id": 5,
    "quantity": 3
}
```

### Orders API

```http
GET /api/orders/
POST /api/orders/create/
GET /api/orders/{id}/
```

Full API documentation available at `/swagger/` or `/redoc/`

## 📸 Screenshots

<div align="center">
  <h3>Home Page</h3>
  <img src="screenshots/home.png" alt="Home Page" width="800"/>
  
  <h3>Product Listing</h3>
  <img src="screenshots/products.png" alt="Products Page" width="800"/>
  
  <h3>Product Detail</h3>
  <img src="screenshots/product-detail.png" alt="Product Detail" width="800"/>
  
  <h3>Shopping Cart</h3>
  <img src="screenshots/cart.png" alt="Cart Page" width="800"/>
  
  <h3>Checkout</h3>
  <img src="screenshots/checkout.png" alt="Checkout" width="800"/>
  
  <h3>Distributor Dashboard</h3>
  <img src="screenshots/dashboard.png" alt="Dashboard" width="800"/>
</div>

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Write docstrings for functions
- Add comments for complex logic
- Test your changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Project Maintainer**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Project Link**: [https://github.com/yourusername/wearhub](https://github.com/yourusername/wearhub)

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Documentation
- All contributors and testers

---

<div align="center">
  Made with ❤️ using Django
</div>
