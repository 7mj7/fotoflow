import reflex as rx

config = rx.Config(
    app_name="fotoflow",
    api_url="http://localhost:8000",  # URL de tu API FastAPI
    env=rx.Env.DEV, # Modo desarrollo 
)