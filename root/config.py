import os

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
    MONGO_URI = 'mongodb+srv://skhomyn12:Skhomyn123@cluster0.1tpyf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    refresh_tokens = {}  # Додано для зберігання токенів
