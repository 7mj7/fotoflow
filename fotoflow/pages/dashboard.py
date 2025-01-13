# fotoflow/pages/dashboard.py

import reflex as rx
from fotoflow.state.auth_state import AuthState  # Import the AuthState

def dashboard_page() -> rx.Component:
    return rx.container(
        rx.cond(
            AuthState.is_authenticated,
            dashboard_content(),
            rx.redirect("/login"),
        ),
    )

@rx.page(
    "/dashboard",
    on_load=AuthState.check_authentication
)


def dashboard_content() -> rx.Component:
    return rx.container(
        # Botón para cambiar el modo de color (claro/oscuro)
        rx.color_mode.button(position="top-right"),
        
        # Título del Dashboard
        rx.heading("Dashboard", size="8", mb="6"),
        
        # Contenedor vertical para los enlaces
        rx.vstack(
            # Enlace al CRUD de Usuarios
            rx.link(
                rx.button(
                    "Gestión de Usuarios",
                    color_scheme="blue",
                    size="3",  # Cambiado de "lg" a "3"
                    width="200px",
                ),
                href="/users",
            ),
            
            # Enlace al CRUD de Galerías
            rx.link(
                rx.button(
                    "Gestión de Galerías",
                    color_scheme="green",
                    size="3",  # Cambiado de "lg" a "3"
                    width="200px",
                ),
                href="/galleries",
            ),
            
            # Enlace al CRUD de Sesiones Fotográficas
            rx.link(
                rx.button(
                    "Gestión de Sesiones",
                    color_scheme="teal",
                    size="3",  # Cambiado de "lg" a "3"
                    width="200px",
                ),
                href="/sessions",
            ),
            
            # Enlace al CRUD de Fotos
            rx.link(
                rx.button(
                    "Gestión de Fotos",
                    color_scheme="purple",
                    size="3",  # Cambiado de "lg" a "3"
                    width="200px",
                ),
                href="/photos",
            ),

            # Salir de la sesión
            rx.link(
                rx.button(
                    "Cerrar Sesión",
                    color_scheme="red",
                    size="3",  # Cambiado de "lg" a "3"
                    width="200px",
                ),
                href="/logout",
            ),
            
            # Espaciado entre los botones
            spacing="4",
            align="center",
        ),
        
        # Alineación y espacio interno del contenedor principal
        justify="center",
        align="center",
        height="100vh",
    )