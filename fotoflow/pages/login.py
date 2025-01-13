# pages/login.py

import reflex as rx

from fotoflow.state.auth_state import AuthState


'''class LoginState(rx.State):
    """El estado del formulario de login."""

    email: str = ""
    password: str = ""
    error: str = ""

    def login(self):
        if self.email == "" or self.password == "":
            self.error = "Por favor, complete todos los campos"
            return
        self.error = ""
        return rx.redirect("/")
'''


# copiado de https://reflex.dev/docs/recipes/auth/login-form/
'''def login_page() -> rx.Component:
    return rx.box(
        rx.center(
            rx.card(
                rx.vstack(
                    rx.center(
                        rx.image(
                            src="/images/logo.jpg",
                            width="2.5em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.heading(
                            "Iniciar sesión",
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
                            "Dirección de correo",
                            size="3",
                            weight="medium",
                            text_align="left",
                            width="100%",
                        ),
                        rx.input(
                            placeholder="usuario@example.com",
                            type="email",
                            name="username",
                            size="3",
                            width="100%",
                            value=AuthState.username,
                            on_change=AuthState.set_username,
                        ),
                        justify="start",
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
                            justify="between",
                            width="100%",
                        ),
                        rx.input(
                            placeholder="Introduzca su contraseña",
                            type="password",
                            name="password",
                            size="3",
                            width="100%",
                            value=AuthState.password,
                            on_change=AuthState.set_password,                            
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.button("Acceder", size="3", width="100%"),
                    spacing="6",
                    width="100%",                    
                    type_="submit",
                    on_submit=AuthState.handle_login,
                ),
                size="4",
                max_width="28em",
                width="100%",
            ),
            h="100vh",  # Altura total de la ventana
            w="100%",  # Ancho total
            padding="2em",  # Espaciado alrededor
            bg="var(--bg)",  # Color de fondo opcional
        )
    )
'''

def login_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Iniciar Sesión"),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Email",
                        type_="email",
                        value=AuthState.username,
                        on_change=AuthState.set_username,
                    ),
                    rx.input(
                        placeholder="Contraseña",
                        type_="password",
                        value=AuthState.password,
                        on_change=AuthState.set_password,                            
                    ),
                    rx.button("Iniciar Sesión", type_="submit"),
                    rx.text(AuthState.error, color="red"),
                ),
                on_submit=AuthState.handle_login,
            ),
        ),
        padding="2em",
    )