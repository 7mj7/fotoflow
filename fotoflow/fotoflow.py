"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from fotoflow.pages.login import login_page

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