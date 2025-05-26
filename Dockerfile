# Gunakan image Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Salin file requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke container
COPY . .

# Expose port untuk Streamlit
EXPOSE 8501

# Jalankan Streamlit saat container dimulai
CMD ["streamlit", "run", "TawK.py", "--server.port=8501", "--server.address=0.0.0.0"]
