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
    
    @rx.event
    async def create_gallery(self, form_data: dict):
        """Crea una nueva galería"""
        try:
            client = APIClient()
            response = await client.make_request(
                "/galleries/",
                self.token,
                method="POST",
                data=form_data
            )

            if "error" in response:
                self.error_message = response["error"]
            else:
                # Redirigir a la lista de galerías
                return rx.redirect("/galleries/")

        except Exception as e:
            self.error_message = f"Error al crear la galería: {str(e)}"

    @rx.event
    async def update_gallery(self, form_data: dict):
        """Actualiza una galería existente"""
        try:
            client = APIClient()
            response = await client.make_request(
                f"/galleries/{self.gallery_id}",
                self.token,
                method="PUT",
                data=form_data
            )

            if "error" in response:
                self.error_message = response["error"]
            else:
                # Actualizar la galería
                await self.get_gallery()

        except Exception as e:
            self.error_message = f"Error al actualizar la galería: {str(e)}"



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
        rx.table.cell(
            #rx.link(
            #    "Ver galería",
            #    href=f"/galleries/{gallery.id}",
            #    color="blue.500",
            #    text_decoration="none",
            #),
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.icon(
                            tag="eye",  # Reemplaza "eye" con el nombre del icono que deseas usar
                            color="blue.500",
                        ),
                        "Ver",
                        #variant="ghost",  # Puedes ajustar el estilo del botón según tus necesidades
                    ),
                    href=f"/galleries/{gallery.id}",
                    text_decoration="none",
                ),
                # Añadimos el diálogo de edición
                gallery_dialog( 
                    gallery
                ),    
            ),
            
        ), 
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
                #rx.button(
                #    "Nueva Galería",
                #    on_click=rx.redirect("/galleries/new"),
                #    color_scheme="green",
                #    margin_right="2",
                #),
                # Por este:
                gallery_dialog(),
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


# --------------- Dialogos ---------------
#def gallery_dialog(gallery: Optional[Galery] = None, is_edit: bool = False):
def gallery_dialog(galeria: Optional[Galery] = None):
    """Componente Dialog para crear/editar galería"""
    is_edit = galeria is not None
    title = "Editar Galería" if is_edit else "Nueva Galería"
    button_text = "Editar" if is_edit else "Crear"

    if galeria is None:
        codigo_galeria = ""
        nombre = ""
        descripcion = ""
        codigo_cliente = ""
    else:
        codigo_galeria = galeria.id
        nombre = galeria.name
        descripcion = galeria.description
        codigo_cliente = str(galeria.client_id)
        #print(f"Nombre: {galeria.name}")
        #print(f"Descripcion: {galeria.description}")
        #print(f"Cliente: {galeria.client_id}")
    
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon(
                    tag="file-pen-line",  # Reemplaza "eye" con el nombre del icono que deseas usar
                    color="blue.500",
                ),
                button_text, 
                color_scheme="blue" if is_edit else "green"
            )
        ),
        rx.dialog.content(
            rx.dialog.title(title),
            rx.form(
                rx.flex(
                    # ID (solo visible en edición)
                    rx.cond(
                        is_edit,
                        rx.hstack(
                            rx.text(
                                f"CÓDIGO #{codigo_galeria}",
                                #as_="div",
                                #size="2",
                                #margin_bottom="4px",
                                weight="bold",
                            ),
                            #rx.text(codigo_galeria),
                            #rx.cond(
                            #    galeria,
                            #    rx.text(galeria.id),
                            #    rx.text(""),
                            #),
                            margin_bottom="3",
                        ),
                    ),
                    # Nombre
                    rx.text(
                        "Nombre",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold",
                    ),
                    rx.input(
                        default_value=nombre,        
                        placeholder="Ingrese el nombre de la galería",
                        name="name",
                        required=True,
                    ),
                    # Descripción
                    rx.text(
                        "Descripción",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold",
                    ),
                    rx.text_area(
                        default_value=descripcion,
                        placeholder="Ingrese la descripción",
                        name="description",
                    ),
                    # ID del Cliente
                    rx.text(
                        "ID del Cliente",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold",
                    ),
                    rx.input(
                        default_value=codigo_cliente,
                        placeholder="Ingrese el ID del cliente",
                        name="client_id",
                    ),
                    direction="column",
                    spacing="3",
                ),
                # Botones
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Guardar",
                            type="submit",
                            color_scheme="blue",
                        ),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                #on_submit=GalleryState.update_gallery if is_edit else GalleryState.create_gallery,
                on_submit=GalleryState.create_gallery,
            ),
        ),
    )