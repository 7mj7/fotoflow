# fotoflow/fotoflow.py
import reflex as rx
from .pages.login import login
from .pages.dashboard import dashboard

from .pages.users import users
from .pages.galleries import galleries
from .state.auth_state import AuthState

# Define your app-wide styles
style = {
    "background_color": "rgb(248, 250, 252)",
    "min_height": "100vh",
}


# Define the app layout
def index() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.cond(
                AuthState.is_authenticated,
                rx.vstack(
                    rx.heading("Welcome back!", size="4"),
                    rx.button(
                        "Go to Dashboard",
                        on_click=lambda: rx.redirect("/dashboard"),
                        color_scheme="blue",
                    ),
                ),
                rx.vstack(
                    rx.heading("Bienvenido a FotoFlow", size="4"),
                    rx.text("Por favor inicie sesión para continuar"),
                    rx.button(
                        "Iniciar sesión",
                        on_click=lambda: rx.redirect("/login"),
                        color_scheme="blue",
                    ),
                ),
            ),
            padding="8",
            spacing="4",
            align_items="center",
            margin="0 auto",
            max_width="400px",
        ),
        style=style,
    )


# Create the app instance
app = rx.App()

# Add pages to the app
app.add_page(index, route="/")
app.add_page(login, route="/login")
app.add_page(dashboard, route="/dashboard")
app.add_page(users, route="/users")
app.add_page(galleries, route="/galleries")
# app.add_page(profile, route="/profile")
