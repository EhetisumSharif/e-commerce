<div align="center">

  <h1>🛒 E-Commerce Web Application</h1>
  <p><b>A modern, responsive web-based e-commerce platform built for efficient online shopping, inventory management, and secure transactions.</b></p>

  <!-- Badges -->
  <img src="https://img.shields.io/badge/Course-CSE%203391%20(Web%20Engineering)-blue?style=for-the-badge" alt="Course Code">
  <img src="https://img.shields.io/badge/Framework-Django-green?style=for-the-badge" alt="Django">
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License">

</div>

---

## 📌 About The Project
This project is developed as part of the **Web Engineering** course (CSE 3391) under the Department of Computer Science and Engineering at **IUBAT**. The platform is designed to provide a seamless online shopping experience for customers while offering an easy-to-use management interface for administrators. It specializes in dairy and everyday retail products, featuring user account creation, product browsing, cart and wishlist management, and secure payment processing.

For detailed documentation, system architecture, UML diagrams, and testing results, you can check the complete project report here:
👉 **[View Project Report PDF](https://github.com/EhetisumSharif/e-commerce/blob/main/E-commerce%20project%20reports.pdf)**

---

## ✨ Key Features & Functionalities
- **User Authentication & Profiles:** Secure registration, login, logout, profile management, and password recovery via email.
- **Product Discovery & Search:** Browse products through category-based dropdowns and real-time search filtering.
- **Cart & Wishlist Management:** Add, update, or remove items dynamically with automated price calculations.
- **Checkout & Payments:** Seamless shipping address selection and mock payment gateway integration via **SSLCommerz**.
- **Order Tracking:** Instant order summary and tracking details immediately upon completion.
- **Admin Panel:** Powerful Django admin interface to manage products, categories, inventory, and track customer orders.

---

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3 (Flexbox & Grid), Vanilla JavaScript
- **Backend:** Python, Django Framework (MVC/MVT Architecture)
- **Database:** SQLite (Managed via Django ORM & Admin Panel)
- **Payment Gateway:** SSLCommerz (Demo Integration)
- **Version Control:** Git & GitHub

---

## 🗄️ Database Schema
The database is structured efficiently using Django models with foreign key relationships:
1. **User Table:** Stores core user information, credentials, and profile addresses.
2. **Product Table:** Contains product details, descriptions, prices, stock levels, and category links.
3. **Cart & Wishlist Tables:** Temporary tables to manage user-specific selected items.
4. **Order Table:** Captures confirmed order data and current status (Pending, Shipped, Delivered).
5. **Payment Table:** Records transaction specifics, amounts, and SSLCommerz transaction IDs.

---

## 🚀 Getting Started

To run this project locally, follow these steps:

### Prerequisites
- Python installed on your system.
- Git installed.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/EhetisumSharif/e-commerce.git](https://github.com/EhetisumSharif/e-commerce.git)
