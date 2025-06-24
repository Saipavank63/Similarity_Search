# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

COPY Final_cleaned_dataset.csv /app/Final_cleaned_dataset.csv

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Define environment variable
ENV NAME ProductSimilarityApp

# Run FastAPI and Streamlit apps
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
