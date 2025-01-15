# fotoflow/components/navbar.py

import reflex as rx
from ..state.auth_state import AuthState

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/images/logo.jpg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "FotoFlow", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Usuarios", "/users"),
                    navbar_link("Opción 2", "/#"),
                    navbar_link("Opción 3", "/#"),
                    navbar_link("Opción 4", "/#"),
                    justify="end",
                    spacing="5",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/images/logo.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Reflex", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        rx.menu.item("Opción 1"),
                        rx.menu.item("Opción 2"),
                        rx.menu.item("Opción 3"),
                        rx.menu.item("Opción 4"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )

'''def navbar():
    return rx.box(
        rx.hstack(
            rx.heading("FotoFlow", size="6"),
            rx.spacer(),
            rx.cond(
                AuthState.is_authenticated,
                # Si el usuario está autenticado
                rx.hstack(
                    rx.link("Dashboard", href="/dashboard"),
                    rx.link("Profile", href="/profile"),
                    rx.button(
                        "Logout",
                        on_click=lambda: rx.redirect("/login"),
                        size="4",
                        color_scheme="red",
                    ),
                    spacing="4",
                ),
                # Si el usuario no está autenticado
                rx.link("Login", href="/login"),
            ),
            spacing="4",
        ),
        width="100%",
        padding="4",
        background="white",
        border_bottom="1px solid #eaeaea",
    )
'''