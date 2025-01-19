# fotoflow/pages/gallery_detail.py
import reflex as rx
from typing import Optional
from ..components.navbar import navbar
from ..components.auth_wrapper import require_auth
from ..api.client import APIClient  # Importar el cliente API


# --------------- Modelos ---------------
class GalleryPhoto(rx.Base):
    """Modelo de datos para una foto en la galería."""

    gallery_photo_id: int
    photo_id: int
    description: str
    path: str
    selected: bool
    favorite: bool


class Galery(rx.Base):
    """Modelo de datos para una galería."""

    id: int
    name: str  # Nombre de la galería
    description: str  # Descripción opcional de la galería
    photographer_id: int  # ID del fotógrafo (se asigna automáticamente)
    client_id: Optional[int] = (
        None  # ID del cliente opcional, puede ser None y ser asignado más tarde
    )
    photos: list[GalleryPhoto] = []  # Lista de fotos de la galería


class GalleryState(rx.State):
    current_gallery: Galery | None = None
    is_loading: bool = False
    error_message: str = ""
    token: str = rx.LocalStorage(name="auth_token")

    @rx.var
    def gallery_id(self) -> int:
        """Obtiene el ID de la galería de la URL"""
        return int(self.router.page.params.get("id", 0))

    @rx.event
    async def get_gallery(self):
        """Obtiene los datos de la galería desde la API"""
        print ("Obteniendo galería")
        try:
            self.is_loading = True
            self.error_message = ""

            client = APIClient()
            response = await client.make_request(
                f"/galleries/{self.gallery_id}", self.token
            )

            if "error" in response:
                self.error_message = response["error"]
            else:
                self.current_gallery = Galery(**response)

        except Exception as e:
            self.error_message = f"Error al cargar la galería: {str(e)}"
        finally:
            self.is_loading = False


@require_auth
@rx.page(on_load=GalleryState.get_gallery)  # Agregamos el decorador page con on_load
def gallery_detail() -> rx.Component:
    """Página de detalle de galería"""
    return rx.hstack(
        rx.box(
            navbar(),
            rx.vstack(
                # Cabecera
                rx.hstack(
                    rx.hstack(
                        rx.heading(
                            f"Galería de Fotos nº {GalleryState.gallery_id}",
                            size="6",
                        ),
                        rx.spacer(),  # Empuja el botón hacia la derecha
                        # rx.button(
                        #    "Nueva Galería",
                        #    on_click=rx.redirect("/galleries/new"),
                        #    color_scheme="green",
                        #    margin_right="2",
                        # ),
                        width="100%",
                        padding="4",
                    ),
                    rx.spacer(),
                    # Botón de actualizar
                    rx.button(
                        "Actualizar",
                        on_click=GalleryState.get_gallery,
                        is_loading=GalleryState.is_loading,
                        color_scheme="blue",
                    ),
                    # Botón de volver
                    rx.button(
                        "Volver",
                        on_click=rx.redirect("/galleries"),
                        color_scheme="gray",
                    ),
                    width="100%",
                    padding="4",
                ),
                # Mensaje de error
                rx.cond(
                    GalleryState.error_message != "",
                    rx.text(GalleryState.error_message, color="red"),
                ),
                # Detalles de la galería
                rx.cond(
                    GalleryState.is_loading,
                    rx.center(
                        rx.spinner(size="3"),
                        padding="8",
                    ),
                    rx.cond(
                        GalleryState.current_gallery is not None,
                        rx.box(
                            rx.vstack(
                                rx.text("ID:", font_weight="bold"),
                                rx.text(GalleryState.current_gallery.id),
                                rx.text("Nombre:", font_weight="bold"),
                                rx.text(GalleryState.current_gallery.name),
                                rx.text("Descripción:", font_weight="bold"),
                                rx.text(GalleryState.current_gallery.description),
                                rx.text("ID del Fotógrafo:", font_weight="bold"),
                                rx.text(GalleryState.current_gallery.photographer_id),
                                rx.text("ID del Cliente:", font_weight="bold"),
                                align_items="start",
                                spacing="2",
                            ),
                            gallery_photos(), # Sección de fotos
                            width="100%",
                            bg="white",
                            border_radius="lg",
                            box_shadow="sm",
                            padding="4",
                        ),
                    ),
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
        ),
    )


def gallery_photos() -> rx.Component:
    return rx.vstack(

        #prueba
        #rx.image(
        #    src='/galleries/001.jpg',
        #    #alt=photo.description,
        #    height="200px",
        #    width="200px",
        #    object_fit="cover",
        #),

        # Sección de fotos
        rx.heading("Fotos de la Galería", size="4", margin_top="6"),
        rx.grid(
            rx.foreach(
                GalleryState.current_gallery.photos,
                lambda photo: rx.box(
                    rx.vstack(
                        rx.image(
                            src=photo.path,
                            alt=photo.description,
                            height="200px",
                            width="200px",
                            object_fit="cover",
                        ),
                        rx.text(
                            photo.description,
                            font_size="sm",
                            text_align="center",
                        ),
                        rx.hstack(
                        rx.cond(
                            photo.selected,
                            rx.icon(
                                "check",
                                color="green",
                            ),
                            rx.icon(
                                "check",
                                color="gray",
                            ),
                        ),
                        rx.cond(
                            photo.favorite,
                            rx.icon(
                                "star",
                                color="yellow",
                            ),
                            rx.icon(
                                "star",
                                color="gray",
                            ),
                        ),
                        spacing="2",
                    )
                    ),
                    padding="2",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="md",
                    margin="2",
                ),
            ),
            spacing="4",
            justify="center",
        ),        
    )
