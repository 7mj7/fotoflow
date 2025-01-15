# fotoflow/pages/login.py
import reflex as rx
from ..state.auth_state import AuthState


def login():
    """Página de login"""
    return rx.vstack(
        # navbar(),  # Incluimos el navbar
        login_form(),  # Incluimos el formulario
        width="100%",
        spacing="0",
    )


def login_form():
    """Componente del formulario de login"""
    return rx.vstack(
        rx.heading("FotoFlow Login"),
        rx.input(
            placeholder="Username",
            on_change=AuthState.set_username,
            value=AuthState.username,
            margin_y="2",
        ),
        rx.input(
            type_="password",
            placeholder="Password",
            on_change=AuthState.set_password,
            value=AuthState.password,
            margin_y="2",
        ),
        rx.button(
            "Iniciar sesión",
            on_click=AuthState.handle_login,
            is_loading=AuthState.loading,
            color_scheme="blue",
        ),
        rx.cond(
            AuthState.error != "",
            rx.text(
                AuthState.error,
                color="red",
            ),
        ),
        padding="4",
        spacing="4",
        max_width="400px",
        margin="0 auto",
    )