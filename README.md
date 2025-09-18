# ProDev BE — E-Commerce Backend

An **E-Commerce Backend** project built with Django and PostgreSQL, simulating a real-world development environment with emphasis on **scalability, security, and performance**.

This backend provides APIs for product catalog management, user authentication, and product discovery features like filtering, sorting, and pagination. It also demonstrates database optimization techniques for high-performance queries.

---

## 🚀 Features

### 1. CRUD Operations

* Manage **Products** and **Categories** (Create, Read, Update, Delete).
* User authentication and management via **JWT tokens**.

### 2. API Features

* **Filtering & Sorting**: Filter products by category, price range, and search terms.
* **Pagination**: Efficiently paginate product listings for large datasets.
* **Secure Authentication**: JWT-based login and refresh.

### 3. API Documentation

* Auto-generated **Swagger/OpenAPI** docs with **drf-spectacular**.
* Accessible at `/api/docs/`.

### 4. Performance

* Query optimization with `select_related` to prevent N+1 issues.
* Database indexes on frequently queried fields (`price`, `created_at`, `sku`).
* PostgreSQL trigram indexes for text search (advanced).

---

## 🛠️ Tech Stack

* **Backend Framework**: Django + Django REST Framework (DRF)
* **Database**: PostgreSQL
* **Authentication**: JSON Web Tokens (JWT via `djangorestframework-simplejwt`)
* **Filtering**: django-filter
* **API Documentation**: drf-spectacular (OpenAPI 3)
* **Deployment**: Docker + docker-compose

---

## 📂 Project Structure

```
alx-project-nexus/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── config/                     # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/               # custom user & JWT auth
│   └── products/               # product & category APIs
└── tests/                      # test suite
```

---

## ⚙️ Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/alx-project-nexus.git
cd alx-project-nexus
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file (use `.env.example` as reference):

```
SECRET_KEY=your_secret_key
DEBUG=True
POSTGRES_DB=ecommerce_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Start Development Server

```bash
python manage.py runserver
```

Access API at: `http://127.0.0.1:8000/api/`

---

## 🐳 Run with Docker

### Build & Start Services

```bash
docker-compose up --build
```

API will be available at: `http://localhost:8000/api/`

---

## 🔑 Authentication (JWT)

* **Obtain token**

```http
POST /api/auth/token/
{
  "username": "testuser",
  "password": "password123"
}
```

* **Refresh token**

```http
POST /api/auth/token/refresh/
{
  "refresh": "<refresh_token>"
}
```

Use the `access` token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

---

## 📘 API Endpoints

### Products

* `GET /api/products/` — List products (supports filtering, sorting, pagination)
* `POST /api/products/` — Create new product (JWT required)
* `GET /api/products/{id}/` — Get product by ID
* `PUT /api/products/{id}/` — Update product (JWT required)
* `DELETE /api/products/{id}/` — Delete product (JWT required)

### Categories

* `GET /api/categories/` — List categories
* `POST /api/categories/` — Create new category (JWT required)

### Auth

* `POST /api/auth/token/` — Get JWT tokens
* `POST /api/auth/token/refresh/` — Refresh JWT

### Docs

* `GET /api/docs/` — Swagger UI docs
* `GET /api/schema/` — OpenAPI schema (JSON)

---

## 📊 Filtering, Sorting, Pagination

Examples:

```bash
# Filter by category ID
GET /api/products/?category=2

# Price range filter
GET /api/products/?min_price=20&max_price=100

# Sort by price ascending
GET /api/products/?ordering=price

# Sort by price descending
GET /api/products/?ordering=-price

# Paginate results
GET /api/products/?page=2&page_size=10
```

---

## 🛠️ Database Optimization

* Indexes added on `price`, `sku`, `created_at`, `name`.
* Use `select_related('category')` to optimize joins.
* PostgreSQL trigram index enabled for product search (advanced).

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX product_name_trgm_idx 
ON apps_products_product USING gin (name gin_trgm_ops);
```

---

## ✅ Testing

Run tests with:

```bash
python manage.py test
```

Sample test:

```py
from django.urls import reverse
from rest_framework.test import APITestCase
from apps.products.models import Category, Product

class ProductListTests(APITestCase):
    def setUp(self):
        cat = Category.objects.create(name='Shoes', slug='shoes')
        for i in range(10):
            Product.objects.create(name=f'Product {i}', sku=f'SKU{i}', price=10+i, category=cat)

    def test_list_products(self):
        url = reverse('product-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.json())
```

---

## 📦 Deployment

* Package app into Docker image
* Deploy with Docker Compose or Kubernetes
* Use managed PostgreSQL (e.g., AWS RDS, Railway, Render)
* Run `python manage.py migrate --noinput`
* Collect static files: `python manage.py collectstatic --noinput`
* Serve via **gunicorn** or **uvicorn workers** for production

---

## 📝 Evaluation Criteria

1. **Functionality**: CRUD APIs, filtering, sorting, pagination, auth
2. **Code Quality**: Clean, maintainable, documented
3. **User Experience**: Comprehensive API docs
4. **Performance**: DB indexing, query optimization
5. **Version Control**: Frequent, descriptive commits

---

## 📌 Commit Workflow Examples

```
feat: set up Django project with PostgreSQL
feat: implement JWT authentication
feat: add product APIs with filtering and pagination
feat: integrate Swagger docs
perf: add DB indexing for product queries
docs: update README with setup instructions
test: add integration tests for product APIs
```

---

## 👨‍💻 Author

**ProDev Final Exam — E-Commerce Backend**
Developed by: *Ugochukwu Chukwuemeka*
