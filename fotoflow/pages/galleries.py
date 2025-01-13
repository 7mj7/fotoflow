# pages/galleries.py

import reflex as rx

from rxconfig import config

import httpx

class Galery(rx.Base):
    """ Modelo de datos para una galería."""
    id: int
    name: str  # Nombre de la galería
    description: str  # Descripción opcional de la galería
    photographer_id: int  # ID del fotógrafo (se asigna automáticamente)
    client_id: int  # ID del cliente opcional, puede ser None y ser asignado más tarde


class GalleryState(rx.State):
    """Estado para la gestión de galerías."""

    
    # Lista de galerías
    galleries: list[Galery] = [
        Galery(id=1, name="Galería 1", description="Descripción de la galería 1", photographer_id=1, client_id=1),
        Galery(id=2, name="Galería 2", description="Descripción de la galería 2", photographer_id=2, client_id=2),
        Galery(id=3, name="Galería 3", description="Descripción de la galería 3", photographer_id=3, client_id=3),
        Galery(id=4, name="Galería 4", description="Descripción de la galería 4", photographer_id=4, client_id=4),
    ]

    
    galleries: list[Galery] = []
    #Metodo para obtener las galerias desde la API
    async def get_galleries(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{config.api_url}/galleries/")
            self.galleries = [Galery(**gallery) for gallery in response.json()]


    selected_gallery: dict = None

def generate_gallery_row(gallery: Galery) -> rx.Component:
    return rx.table.row(
        rx.table.cell(gallery.id),
        rx.table.cell(gallery.name),
        rx.table.cell(gallery.description),
        rx.table.cell(gallery.photographer_id),
        rx.table.cell(gallery.client_id),
    )

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
                )
            ),
            rx.table.body(
                rx.foreach(GalleryState.galleries, generate_gallery_row)
            ),
            variant="surface",
            size="3",
            width="100%",
    )
        
    )

# Decorador de la página para obtener las galerías
@rx.page(on_load=GalleryState.get_galleries)
def galleries_page() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Galerías", size="8", mb="6"),
            gallery_table(),
            spacing="4",
            justify="center",
        )
    )

'''import reflex as rx
from fotoflow.state.auth_state import AuthState

class GalleryState(rx.State):
    """Estado para la gestión de galerías."""
    galleries: list = []
    selected_gallery: dict = None
    
    async def get_galleries(self):
        """Obtener las galerías del usuario."""
        try:
            response = await self.client.get("/api/galleries")
            self.galleries = response.json()
        except Exception as e:
            return rx.window_alert(f"Error al cargar galerías: {str(e)}")
    
    async def select_photos(self, gallery_id: int, photo_id: int):
        """Seleccionar fotos para un álbum."""
        try:
            await self.client.post(
                f"/api/galleries/{gallery_id}/photos/{photo_id}/select"
            )
            await self.get_galleries()
        except Exception as e:
            return rx.window_alert(f"Error al seleccionar foto: {str(e)}")

def gallery_card(gallery: dict) -> rx.Component:
    """Componente para mostrar una galería."""
    return rx.box(
        rx.vstack(
            rx.heading(gallery["name"], size="lg"),
            rx.text(f"Fecha: {gallery['created_at']}"),
            rx.text(f"Fotos seleccionadas: {gallery['selected_photos_count']}"),
            rx.hstack(
                rx.link(
                    rx.button("Ver fotos"),
                    href=f"/galleries/{gallery['id']}/photos",
                ),
                rx.button(
                    "Descargar selección",
                    on_click=lambda: rx.window_alert("Función en desarrollo"),
                ),
            ),
        ),
        padding="4",
        border="1px solid",
        border_radius="md",
        margin="2",
    )

def galleries_page() -> rx.Component:
    """Página principal de galerías."""
    return rx.container(
        rx.cond(
            AuthState.is_authenticated,
            rx.vstack(
                rx.heading("Mis Galerías"),
                rx.button(
                    "Actualizar",
                    on_click=GalleryState.get_galleries,
                    margin_bottom="4",
                ),
                rx.cond(
                    len(GalleryState.galleries) > 0,
                    rx.vstack(
                        rx.foreach(
                            GalleryState.galleries,
                            gallery_card,
                        ),
                    ),
                    rx.text("No hay galerías disponibles"),
                ),
                spacing="4",
                width="100%",
                padding="4",
            ),
            rx.redirect("/login"),
        ),
        max_width="1200px",
        padding="4",
    )

# Página de fotos de una galería específica
def gallery_photos_page(gallery_id: int) -> rx.Component:
    return rx.container(
        rx.cond(
            AuthState.is_authenticated,
            rx.vstack(
                rx.heading("Fotos de la Galería"),
                rx.button(
                    "Volver a galerías",
                    on_click=rx.redirect("/galleries"),
                ),
                # Aquí iría el grid de fotos
                rx.text("Implementación del grid de fotos pendiente"),
            ),
            rx.redirect("/login"),
        ),
    )'''
