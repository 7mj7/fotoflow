# fotoflow/pages/galleries.py
import reflex as rx
from typing import Optional
from ..components.navbar import navbar
from ..components.auth_wrapper import require_auth


# Para las peticiones a la API
from ..api.client import APIClient


# --------------- Modelos ---------------
class Galery(rx.Base):
    """Modelo de datos para una galería."""

    id: int
    name: str  # Nombre de la galería
    description: str  # Descripción opcional de la galería
    photographer_id: int  # ID del fotógrafo (se asigna automáticamente)
    client_id: Optional[int] = (
        None  # ID del cliente opcional, puede ser None y ser asignado más tarde
    )


# --------------- Estados ---------------
class GalleryState(rx.State):
    """Estado para la gestión de galerías."""

    galleries: list[Galery] = []
    is_loading: bool = False
    error_message: str = ""
    token: str = rx.LocalStorage(name="auth_token")

    """ Esto es lo siguiente """
    galleries: list[Galery] = []

    # Función para obtener la lista de galerías
    async def get_galleries(self):
        """Obtiene la lista de usuarios desde la API"""
        self.is_loading = True
        self.error_message = ""
        try:
            client = APIClient()
            # Usando la función genérica que creamos
            response = await client.make_request("/galleries/me/", self.token)
            if "error" in response:
                self.error_message = response["error"]
            else:
                # Convertimos cada diccionario a un objeto User
                self.galleries = [Galery(**gallery) for gallery in response]
        except Exception as e:
            self.error_message = f"Error al cargar galerías: {str(e)}"
        finally:
            self.is_loading = False


# --------------- Componentes ---------------


# Tabla de galerías
def gallery_table() -> rx.Component:
    return rx.vstack(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("ID"),
                    rx.table.column_header_cell("Nombre"),
                    rx.table.column_header_cell("Descripción"),
                    rx.table.column_header_cell("ID del Fotógrafo"),
                    rx.table.column_header_cell("ID del Cliente"),
                    rx.table.column_header_cell("Acciones"),
                )
            ),
            rx.table.body(rx.foreach(GalleryState.galleries, generate_gallery_row)),
            variant="surface",
            size="3",
            width="100%",
        )
    )


# Función para generar una fila de la tabla
def generate_gallery_row(gallery: Galery) -> rx.Component:
    return rx.table.row(
        rx.table.cell(gallery.id),
        rx.table.cell(gallery.name),
        rx.table.cell(gallery.description),
        rx.table.cell(gallery.photographer_id),
        rx.table.cell(gallery.client_id),
        rx.table.cell("ver galeria"),
    )


# --------------- Página ---------------

@require_auth
def galleries():
    """Página de galerías"""
    return rx.vstack(
        navbar(),
        rx.vstack(            
            # Cabecera con título y botones
            rx.hstack(
                rx.heading(
                    "Galerías del Sistema",
                    size="6",
                ),
                rx.spacer(),  # Empuja el botón hacia la derecha
                rx.button(
                    "Nueva Galería",
                    on_click=rx.redirect("/galleries/new"),
                    color_scheme="green",
                    margin_right="2",
                ),
                rx.button(
                    "Actualizar",
                    on_click=GalleryState.get_galleries,
                    is_loading=GalleryState.is_loading,
                    color_scheme="blue",
                ),
                width="100%",
                padding="4",                
            ),
            # Mensaje de error
            rx.cond(
                GalleryState.error_message != "",
                rx.text(GalleryState.error_message, color="red"),
            ),
            # Contenido principal
            rx.box(
                rx.cond(
                    GalleryState.is_loading,
                    rx.center(
                        rx.spinner(
                            size="3",
                            color="blue",
                            thickness=4,
                        ),
                        padding="8",
                    ),
                    gallery_table(),
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
            spacing="4",
            padding="4",
            margin_top="4",  # Agregar margen superior
        ),
        width="100%",
        min_height="100vh",
        bg="gray.50",
        spacing="0",
    )