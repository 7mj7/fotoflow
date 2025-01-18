# fotoflow/pages/gallery_detail.py
import reflex as rx
from ..components.navbar import navbar
from ..components.auth_wrapper import require_auth

@require_auth
def gallery_detail():
    """Página de detalle de galería"""
    return rx.vstack(
        navbar(),
        rx.vstack(
            # Cabecera
            rx.hstack(
                rx.heading(
                    f"Galería: XXX",
                    size="6",
                ),
                rx.spacer(),
                rx.button(
                    "Volver",
                    on_click=rx.redirect("/galleries"),
                    color_scheme="gray",
                ),
                width="100%",
                padding="4",
            ),
            
            # Detalles de la galería
            rx.box(
                rx.vstack(
                    rx.text(
                        "Descripción:",
                        font_weight="bold",
                    ),
                    rx.text("Descripción de la galería"),
                    rx.text(
                        "ID del Fotógrafo:",
                        font_weight="bold",
                    ),
                    rx.text(str("Fotógrafo ID")),
                    rx.text(
                        "ID del Cliente:",
                        font_weight="bold",
                    ),
                    rx.text("Cliente ID"),
                    align_items="start",
                    spacing="2",
                ),
                width="100%",
                bg="white",
                border_radius="lg",
                box_shadow="sm",
                padding="4",
            ),
            
            width="100%",
            max_width="1200px",
            margin="0 auto",
            margin_top="4",
            spacing="4",
            padding="4",
        ),
        width="100%",
        min_height="100vh",
        bg="gray.50",
        spacing="4",
    )