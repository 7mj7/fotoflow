# fotoflow/pages/gallery_detail.py
import reflex as rx
from ..components.navbar import navbar
from ..components.auth_wrapper import require_auth


class GalleryState(rx.State):
    # current_gallery: Galery | None = None

    @rx.var
    def gallery_id(self) -> int:
        """Obtiene el ID de la galería de la URL"""
        return int(self.router.page.params.get("id", 0))


@require_auth
def gallery_detail() -> rx.Component:  # Añadimos el parámetro id
    """Página de detalle de galería"""
    return rx.vstack(
        navbar(),
        rx.vstack(
            # Cabecera
            rx.hstack(
                rx.heading(
                    f"Galería:  {GalleryState.gallery_id}",  # Usamos el id recibido
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
