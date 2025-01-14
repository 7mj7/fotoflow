# pages/galleries.py

import reflex as rx

from rxconfig import config
from fotoflow.state.auth_state import AuthState

import httpx
import os


class Galery(rx.Base):
    """Modelo de datos para una galería."""

    id: int
    name: str  # Nombre de la galería
    description: str  # Descripción opcional de la galería
    photographer_id: int  # ID del fotógrafo (se asigna automáticamente)
    client_id: int  # ID del cliente opcional, puede ser None y ser asignado más tarde


class GalleryState(rx.State):
    """Estado para la gestión de galerías."""
        
    galleries: list[Galery] = []
    is_loading: bool = False
    error_message: str = ""

    # Lista de galerías de prueba
    test_galleries: list[Galery] = [
        Galery(
            id=1,
            name="Galería 1",
            description="Descripción de la galería 1",
            photographer_id=1,
            client_id=1,
        ),
        Galery(
            id=2,
            name="Galería 2",
            description="Descripción de la galería 2",
            photographer_id=2,
            client_id=2,
        ),
        Galery(
            id=3,
            name="Galería 3",
            description="Descripción de la galería 3",
            photographer_id=3,
            client_id=3,
        ),
        Galery(
            id=4,
            name="Galería 4",
            description="Descripción de la galería 4",
            photographer_id=4,
            client_id=4,
        ),
    ]

    """ Esto es lo siguiente """
    galleries: list[Galery] = []

    # Metodo para obtener las galerias desde la API
    async def get_galleries(self):
        async with httpx.AsyncClient() as client:

            api_url = f"{os.getenv('API_URL', 'http://localhost:8000')}/galleries/me"
            # print(f"Intentando conectar a: {api_url}")  # Debug

            # Obtener el token del AuthState
            token = AuthState.token_cookie

            print(f"Token: {token}")  # Debug
            mis_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            #print(f"Headers: {mis_headers}") # Debug

            # response = await client.get(api_url)
            response = await client.get(api_url, headers=mis_headers)
            print(f"Status code: {response.status_code}")  # Debug
            print(f"Response content: {response.content}")  # Debug
            

            if response.status_code == 200:
                data = response.json()
                self.galleries = [Galery(**gallery) for gallery in data]
            else:
                self.error_message = f"Error del servidor: {response.status_code}"
                # Usar datos de ejemplo si la API falla
                self.galleries = self.test_galleries
                

    # selected_gallery: dict = None


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
            rx.table.body(rx.foreach(GalleryState.galleries, generate_gallery_row)),
            variant="surface",
            size="3",
            width="100%",
        )
    )


# Decorador de la página para obtener las galerías
@rx.page(
    "/galleries", 
    on_load=[AuthState.check_authentication, GalleryState.get_galleries]
)
def galleries_page() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Galerías", size="8", mb="6"),
            gallery_table(),
            spacing="4",
            justify="center",
        ),
    )


'''import reflex as rx


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
