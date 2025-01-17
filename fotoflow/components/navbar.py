# fotoflow/components/navbar.py

import reflex as rx


# Función para crear los enlaces del navbar
def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(rx.text(text, size="4", weight="medium"), href=url)


# Función para crear el navbar
def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                # --
                # --
                rx.link(
                    rx.hstack(
                        rx.image(
                            src="/images/logo.jpg",
                            width="2.25em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.heading("FotoFlow", size="7", weight="bold"),
                        align_items="center",
                    ),
                    href="/dashboard",
                ),
                rx.hstack(
                    navbar_link("Usuarios", "/users"),
                    navbar_link("Galerías", "/galleries"),
                    #navbar_link("Opción 3", "/#"),
                    #navbar_link("Opción 4", "/#"),
                    justify="end",
                    spacing="5",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.link(                
                    rx.hstack(
                        rx.image(
                            src="/images/logo.jpg",
                            width="2em",
                            height="auto",
                            border_radius="25%",
                        ),
                        rx.heading("FotoFlow", size="6", weight="bold"),                    
                        align_items="center",
                    ),
                    href="/dashboard",
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        rx.menu.item("Usuarios", on_click=rx.redirect("/users")),
                        rx.menu.item("Galerías", on_click=rx.redirect("/galleries")),
                        #rx.menu.item("Opción 3"),
                        #rx.menu.item("Opción 4"),
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
