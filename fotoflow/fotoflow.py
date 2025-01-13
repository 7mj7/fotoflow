# fotoflow/fotoflow.py

import reflex as rx

from fotoflow.pages.login import login_page
from fotoflow.pages.dashboard import dashboard_page
from fotoflow.pages.galleries import galleries_page
#from fotoflow.pages.profile import profile_page

from rxconfig import config


class State(rx.State):
    """El estado de la aplicación."""
    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("FotoFlow", size="9"),
            rx.text("Gestión profesional de fotografías"),
            rx.link(
                rx.button("Iniciar Sesión"),
                href="/login",
            ),
            rx.heading("Pruebas", size="6"),
            # Dashboard
            rx.link(
                rx.button("Dashboard"),
                href="/dashboard",
            ),
            # Galerías
            rx.link(
                rx.button("Galerías"),
                href="/galleries",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            
        ),
        # rx.logo(),
    )


# Crear la aplicación
app = rx.App()
app.add_page(index)
app.add_page(login_page, route="/login")
app.add_page(dashboard_page, route="/dashboard")
app.add_page(galleries_page, route="/galleries")
#app.add_page(profile_page, route="/profile")