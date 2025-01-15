# fotoflow/pages/login.py
import reflex as rx
from ..state.auth_state import AuthState


def login():
    """Página de login"""

    return rx.vstack(
        # navbar(),  # Incluimos el navbar
        login_form2(),  # Incluimos el formulario
        centered_button_group(),
    #    width="100%",
    #    spacing="0",
    )


def login_form2() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(
                rx.image(
                    src="/images/logo.jpg",
                    width="2.5em",
                    height="auto",
                    border_radius="25%",
                ),
                rx.heading(
                    "Acceder a FotoFlow",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Email",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="user@reflex.dev",
                    type="email",
                    size="3",
                    width="100%",
                    on_change=AuthState.set_username,
                    value=AuthState.username,
                ),
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Contraseña",
                        size="3",
                        weight="medium",
                    ),
                    # rx.link(
                    #    "Forgot password?",
                    #    href="#",
                    #    size="3",
                    # ),
                    justify="between",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("lock")),
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    width="100%",
                    on_change=AuthState.set_password,
                    value=AuthState.password,
                ),
                spacing="2",
                width="100%",
            ),
            rx.button(
                "Iniciar sesión",
                size="3",
                width="100%",
                on_click=AuthState.handle_login,
                is_loading=AuthState.loading,
            ),
            # rx.center(
            #    rx.text("New here?", size="3"),
            #    rx.link("Sign up", href="#", size="3"),
            #    opacity="0.8",
            #    spacing="2",
            #    direction="row",
            #    width="100%",
            # ),
            spacing="6",
            width="100%",
        ),
        max_width="28em",
        size="4",
        width="100%",
        margin="0 auto",        
        margin_top="2em",        
    )


def login_form():
    """Componente del formulario de login"""
    return rx.vstack(
        rx.heading("FotoFlow Login"),
        rx.input(
            placeholder="Username",
            on_change=AuthState.set_username,
            value=AuthState.username,
            # value="fotografo@example.com",
            margin_y="2",
        ),
        rx.input(
            type_="password",
            placeholder="Password",
            on_change=AuthState.set_password,
            value=AuthState.password,
            # value="foto123",
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

def centered_button_group():
    return rx.center(
        rx.hstack(
            rx.button(
                "CLIENTE",
                color_scheme="blue",
                on_click=lambda: AuthState.set_credentials("cliente@example.com", "cliente123"),
            ),
            rx.button(
                "FOTOGRAFO",
                color_scheme="green",
                on_click=lambda: AuthState.set_credentials("fotografo@example.com", "foto123"),
            ),
            rx.button(
                "ADMIN",
                color_scheme="red",
                on_click=lambda: AuthState.set_credentials("admin@example.com", "admin123"),
            ),
            spacing="4",
            align_items="center",
            justify_content="center",
        ),
        width="100%",
    )