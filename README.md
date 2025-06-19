# 📦 TawK – Inventory Management Made Simple

**TawK** is a user-friendly inventory management system designed to streamline stock tracking, product transactions, and category organization. Whether you're managing a small business or a growing operation, TawK helps ensure real-time inventory accuracy, minimizes manual errors, and boosts operational efficiency.

---

## ✨ Key Features

### ✅ For Users

#### 1. **Check Stock**
Need to check a product’s availability?  
Click the **Stock** button in the sidebar to access the stock check page. From there:

- Select a **category** and a **product name**
- Click the **Check Stock** button to view:
  - Product name
  - Real-time stock quantity
  - Product price

> 🕒 Stock data updates instantly after each transaction!

#### 2. **Perform Transactions**
Managing incoming or outgoing inventory is simple:

- Click the **Transaction** button in the sidebar
- Choose the **category**, **product name**, and **transaction type** (`In` / `Out`)
- Enter the **quantity** and submit the transaction

> ⚠️ For "Out" transactions, we recommend checking stock first  
> 🛠 Can't find a product for an "In" transaction? Let an admin know — they’ll add it for you!

---

### 🛠 For Admins

#### 1. **Transaction Log**
Monitor inventory activities:

- Click the **Transaction** button
- View the 10 most recent transactions
- Use this to prepare products for dispatch or storage

#### 2. **Register Users**
Before using TawK, users must be registered:

- Click the **User** button
- Fill in the user’s **name**, **address**, and **phone number**
- Click **Add User**
- Search users by **ID** or **Name** using the search field below

#### 3. **Add New Products**
New products must be registered before stock can be added:

- Click the **Product** button
- Choose a **category**, enter the **product name** and **price**
- Click to add the product to the inventory

#### 4. **Check Stock**
Admins can also check stock:

- Click the **Stock** button
- Select a **category** and **product**
- View current stock and pricing

#### 5. **View Insights**
Track product performance and inventory trends:

- Click the **Insights** button
- Access reports on:
  - 📈 Stock movement
  - ⭐ Most popular products
  - ⚠️ Low stock alerts
  - 💤 Dead stock
- View data monthly or yearly

---

## 🚀 Why TawK?

- 🕒 **Real-time tracking** for up-to-date stock levels
- 🧭 **Intuitive interface** for smooth user experience
- 📊 **Insight-driven dashboards** to support smart decisions
- 🌱 **Scalable** for businesses of any size

---

## 🛠 Tech Stack

- **Frontend & App Framework:** Streamlit
- **Backend/Data Handling:** Python
- **Database:** SQLite / MySQL (based on your config)
- **Visualization:** Streamlit Charts / Matplotlib / Plotly

---

## 🖥️ How to Run TawK
You can choose the way to run the app:

#### 1. Build Manual
```bash
# Step 1: Clone the repository
git clone https://github.com/your-username/tawk.git
cd tawk

# Step 2: Set up the database
# Open MySQL and run the following (or use a GUI like phpMyAdmin)

mysql -u your_username -p < inventory.sql

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the app
streamlit run app.py
```
OR

#### 2. Use Docker (Don't need to cloning the Github Repo)
```bash
# Step 1 : Install Docker Desktop on your device
docker login

# Step 2 : Pull the image from Docker Hub
docker pull ainiyeaay/tawk:latest

# Step 3 : Run the container
docker run -p 8501:8501 ainiyeeay/tawk:latest

# Step 4 : Open your browser and go to
http://localhost:8501
```
