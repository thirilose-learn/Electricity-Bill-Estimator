# ⚡ Electricity Bill Estimator

> A Python + Gradio web app that helps households track energy consumption and estimate electricity bills — from simple flat-rate calculations to a full monthly comparison dashboard.

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Features](#-features)
- [Concepts Covered](#-concepts-covered)
- [Tech Stack](#-tech-stack)
- [Project Variations](#-project-variations)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 💡 Problem Statement

Many households are unaware of how much electricity they consume daily and struggle to predict their monthly bills. This project aims to bridge that gap by providing a simple, interactive tool to estimate electricity costs based on usage patterns — empowering users to make informed decisions about energy consumption.

---

## ✨ Features

- ✅ Calculate electricity bill based on units consumed
- ✅ Support for flat-rate and slab-based pricing models
- ✅ Input validation and error handling
- ✅ Interactive web interface built with Gradio
- ✅ Monthly comparison dashboard *(Extended version)*

---

## 🧠 Concepts Covered

| Concept | Description |
|---|---|
| **Functions** | Modular calculation logic broken into reusable functions |
| **Conditional Logic** | Slab-wise rate selection using `if-elif-else` chains |
| **Error Handling** | Validates user input with `try-except` blocks |

---

## 🛠 Tech Stack

- **Language:** Python 3.x
- **UI Framework:** [Gradio](https://gradio.app/)

---

## 🚀 Project Variations

This project is built in three progressive levels of complexity:

### 🟢 Basic — Single Rate Calculation
A straightforward bill calculator using a flat per-unit rate.

```
Bill = Units Consumed × Rate per Unit
```

### 🟡 Intermediate — Slab-Based Pricing
Implements a tiered pricing model (common in Indian electricity billing):

| Units Consumed | Rate per Unit |
|---|---|
| 0 – 100 units | ₹1.50 |
| 101 – 200 units | ₹2.50 |
| 201 – 300 units | ₹4.00 |
| Above 300 units | ₹6.00 |

### 🔴 Extended — Monthly Comparison Dashboard
- Enter consumption data for multiple months
- Visual bar chart comparing monthly bills
- Highlights the highest and lowest billing months
- Built entirely within the Gradio interface

---

## ⚙️ Getting Started

### Prerequisites

Make sure you have Python 3.7+ installed.

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/kalyan-0911/electricity-bill-estimator.git
cd electricity-bill-estimator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

The app will launch in your browser at `http://localhost:7860`

---

## 🖥 Usage

1. Enter the number of units consumed in the input field.
2. Select the pricing model (Basic / Slab-based).
3. Click **Calculate** to see your estimated bill.
4. *(Extended version)* Enter consumption for each month and view the comparison chart.

---

## 📁 Project Structure

```
electricity-bill-estimator/
│
├── app.py                  # Main Gradio application & core logic
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

---

## 📸 Screenshots

> *(Note: The images below are placeholders. Please add actual Gradio app screenshots here after running the project)*

| Basic Calculator | Slab-Based | Monthly Dashboard |
|---|---|---|
| ![Basic](Screenshots/basic.png) | ![Slab](screenshots/slab.png) | ![Dashboard](screenshots/dashboard.png) |

---

## 🔮 Future Improvements

- [ ] Add support for different state electricity tariffs (TNEB, BESCOM, etc.)
- [ ] Include fixed charges, taxes, and surcharges in calculation
- [ ] Export bill summary as PDF
- [ ] Add appliance-wise consumption tracker
- [ ] Deploy to Hugging Face Spaces

---

## 👥 Contributors

- **Kalyan** (Repository Owner)
- **Thirilose Jones Nithish R** (Collaborator)
- **Ramyasrik17** (Collaborator)

---

## 👨‍💻 Author

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kalyan-0911)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/your-profile)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> *"Awareness is the first step toward conservation."*
