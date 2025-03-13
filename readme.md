# AI Healthcare System

## 📌 Project Overview
The **AI Healthcare System** is a web-based application that integrates **machine learning** with **Django** to assist users in disease prediction, booking appointments with doctors, purchasing medicines, and managing lab tests. This system provides AI-powered insights to help users monitor their health efficiently.

## 🚀 Features
- **🔍 AI-Powered Disease Prediction**: Input symptoms and get AI-driven health analysis.
- **📅 Doctor Appointments**: Schedule and manage appointments with available doctors.
- **🛒 Online Medicine Store**: Browse and order medicines online.
- **🧪 Lab Test Booking**: Schedule diagnostic tests and view results.
- **📄 Medical Reports & History**: Upload, store, and manage reports.
- **📋 Doctor Dashboard**: Manage patients, appointments, and prescriptions.

## 📂 Project Structure
```
HEALTHCARE_APP/
│
├── healthcare_project/         # Main Django project directory
│   ├── __pycache__
│   ├── healthcare_app/         # Core Django app
│   │   ├── __pycache__
│   │   ├── management/
│   │   ├── migrations/
│   │   ├── static/             # CSS, JS, and images
│   │   ├── templates/healthcare_app/  # HTML templates
│   │   │   ├── appointment_list.html
│   │   │   ├── available_lab_tests.html
│   │   │   ├── base.html
│   │   │   ├── book_appointment.html
│   │   │   ├── book_lab_test.html
│   │   │   ├── disease_prediction.html
│   │   │   ├── doctor_dashboard.html
│   │   │   ├── home.html
│   │   │   ├── issue_prescription.html
│   │   │   ├── lab_test_success.html
│   │   │   ├── login.html
│   │   │   ├── medicines.html
│   │   │   ├── my_orders.html
│   │   │   ├── patient_dashboard.html
│   │   │   ├── patient_details.html
│   │   │   ├── prediction_history.html
│   │   │   ├── prescription_list.html
│   │   │   ├── register.html
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── import_medicine_data.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── views_medicine.py
│   │
│   ├── healthcare_project/
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │
│   ├── media/                  # Uploaded media files
│   ├── db.sqlite3               # SQLite database
│   ├── manage.py
│
├── ml_model/                    # Machine learning model directory
│   ├── dataset/
│   ├── app.py
│   ├── data_dict.pkl
│   ├── nb_model.pkl
│   ├── notebook.ipynb
│   ├── rf_model.pkl
│   ├── svm_model.pkl
│   ├── test.py
│
├── myenv/                        # Virtual environment
├── readme.md
```

## 🛠️ Technologies Used
- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Machine Learning:** Scikit-learn, Pandas, NumPy
- **Database:** SQLite

## 🔧 Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/healthcare-app.git
   cd healthcare-app
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On macOS/Linux
   myenv\Scripts\activate     # On Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (optional, for admin panel access):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the app:** Open `http://127.0.0.1:8000/` in your browser.

## 📌 Future Enhancements
- **🧠 AI Chatbot Integration** for instant health queries.
- **📊 Data Visualization** for health trends.
- **🔄 Continuous Model Training** to improve predictions.
- **📡 API Integration** with real-time health data sources.

## 📞 Contact
For contributions or queries, feel free to contact us:
- 📧 Email: vishaal03.it@gmail.com
- 🔗 [GitHub](https://github.com/VISHAL-038))
- 🌐 Website: www.yourhealthcareapp.com

---
Made with ❤️ by AI Healthcare Team 🚀

