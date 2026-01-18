# 📖 Library Pro: Enterprise Management System

Welcome to the **Library Pro** project manual! This document is designed to serve as a comprehensive guide for anyone—from a project supervisor to a fellow student—who wants to understand, install, and operate this system.

---

## 🌟 Project Overview
**Library Pro** is a sophisticated, full-stack desktop application designed to streamline the operations of a modern library. It replaces manual registers with a digital database, ensuring accuracy in inventory management and book circulation.

### Key Objectives:
- **Efficiency**: Automate the process of adding, updating, and issuing books.
- **Accuracy**: Provide real-time data on asset availability.
- **Aesthetics**: Offer a premium, dark-themed user experience that is both professional and intuitive.

---

## 🏗️ Technical Architecture (The "Under the Hood" View)
This project follows a professional three-tier architecture:

1.  **Frontend (UI Layer)**: Built with **Streamlit**. It handles user interactions, data visualization (using Plotly), and navigation.
2.  **Backend (Logic Layer)**: Written in **Python**. It contains the business logic for connecting to the database and processing CRUD (Create, Read, Update, Delete) operations.
3.  **Database (Data Layer)**: Powered by **MySQL**. It stores all permanent information about books and borrowing records.

---

## 🛠️ Installation & Setup (Step-by-Step)

### 1. Prerequisites
Ensure you have the following installed on your machine:
- [Python 3.10+](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/installer/)

### 2. Environment Configuration
Create a `.env` file in the root directory and add your database credentials:
```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=library_db
```

### 3. Database Initialization
Run the SQL script provided in `database/init.sql` using your MySQL Workbench or terminal to create the necessary tables.

### 4. Install Dependencies
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

### 5. Launch the Application
Start the system by running:
```bash
streamlit run frontend/app.py
```

---

## 📂 Project Structure
- `frontend/`: Contains `app.py`, the core UI and navigation logic.
- `backend/`: Contains `database_utils.py`, the engine for database connections.
- `database/`: Contains `init.sql`, the structural blueprint of the database.
- `.env`: A private file used to store sensitive database credentials safely.
- `requirements.txt`: A list of all external Python libraries needed.

---

## 🎮 How to Use the System

### 📊 Dashboard
- View high-level metrics like **Total Assets**, **Availability**, and **Overdue Books**.
- Analyze the **Portfolio Distribution** graph to see which books are in high demand.

### 📦 Inventory Management
- **Add New Books**: Use the "Register New Title" tab to add stock.
- **Edit/Delete**: Use the "Asset Registry" to update details or decommission old books.

### 🤝 Issuance (Check-out)
- Select a book from the list, enter the borrower's details, and set a return period.
- The system automatically decrements the "Available Quantity".

### 📅 Logistics (Check-in)
- Track who has which book and when it is due.
- Click "Acknowledge Return" to check a book back into the system and update its availability.

---

## 🎓 Academic Q&A (Teacher's Checklist)

**Q: Why use Python for the backend?**
A: Python is highly versatile and offers powerful libraries like `mysql-connector-python` for easy database integration.

**Q: What is the purpose of the `.env` file?**
A: It's a security best practice. By keeping credentials in a separate file, we prevent sensitive passwords from being hardcoded into the script.

**Q: How does the system handle concurrent availability?**
A: Every time a book is issued, the backend runs an `UPDATE` query on the `books` table to subtract 1 from the `available_quantity`.

**Q: What happens if a book is returned late?**
A: The **Logistics** section highlights books with a "CRITICAL" status label if the current date is past the `due_date`.

---

## 🚀 Future Scope
- **User Accounts**: Adding login/signup for different library staff.
- **Barcoding**: Integrating barcode scanners for faster check-outs.
- **Email Alerts**: Automatically emailing students when their books are overdue.
