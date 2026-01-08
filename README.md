# 🏋️‍♂️ FitTrack - ICT 4879 Capstone Project

**FitTrack** is a comprehensive web-based fitness platform designed to promote healthy lifestyle habits. It combines professional workout programs, advanced nutrition tracking, e-commerce functionality, and an AI-powered personal assistant into a single, cohesive application.

![Status](https://img.shields.io/badge/Status-Maintained-success?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-Django%20%7C%20Python%20%7C%20Bootstrap-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## 🌐 Live Demo
Checking out the project is just a click away:
👉 **[View Live Demo on PythonAnywhere](https://nikolasorf.pythonanywhere.com)**

---

## ✨ Key Features

### 🛡️ Security (Enterprise-Grade)
*   **Brute-Force Protection**: Intelligent rate limiting blocks suspicious IPs after 5 failed login attempts (`django-axes`).
*   **Security Logging**: Detailed audit trails for all security-critical events.
*   **Payment Verification**: Server-side validation prevents price tampering during checkout.
*   **Data Privacy**: Automated PII masking in logs (configurable for admins).

### 🤖 AI-Powered Coach
*   **Smart Assistant**: Integrated Chatbot (OpenAI/Gemini) provides personalized fitness and nutrition advice.
*   **Context Aware**: The backend manages the AI logic, ensuring consistent and safe responses.

### 📊 User Dashboard
*   **Progress Tracking**: Interactive charts visualize weight trends and workout frequency (`Chart.js`).
*   **BMI Calculator**: Real-time health metrics calculation.
*   **Recent Activity**: Scrollable history of past orders and logs.

### 🛒 FitShop (E-Commerce)
*   **Product Catalog**: Browse supplements and gear.
*   **Shopping Cart**: Dynamic cart management with stock checks.
*   **Secure Checkout**: Integration with PayPal API for safe transactions.

### 🍎 Nutrition & Training
*   **Calorie Tracker**: Log daily meals and track macro/micronutrients.
*   **Workout Library**: curated exercise programs for various goals (Strength, Weight Loss, Flexibility).

---

## 🛠️ Technologies Used

*   **Backend**: Python, Django 5.x
*   **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
*   **Database**: SQLite (Development) 
*   **AI Integration**: OpenAI API
*   **Security**: Django-Axes, CSP Headers, Secure Session Management

---

## 🚀 Installation & Setup

Follow these steps to run the project locally.

### 1. Prerequisites
*   Python 3.10+
*   Git

### 2. Clone the Repository
```bash
git clone https://github.com/Nickthequick2002/ICT-4879_Capstone-Project_Orfanidis.git
cd ICT-4879_Capstone-Project_Orfanidis
```

### 3. Set Up Environment
Create a `.env` file in the root directory (same folder as `manage.py`) with your secrets:
```ini
DEBUG=True
SECRET_KEY=your_secret_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Initialize Database
```bash
python manage.py migrate
```

### 6. Run the Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

