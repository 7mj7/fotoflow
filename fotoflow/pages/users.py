# fotoflow/pages/users.py
import reflex as rx
from typing import Dict, Any
from ..components.navbar import navbar
from ..components.auth_wrapper import require_auth
from ..state.auth_state import AuthState
from ..api.client import APIClient


class User(rx.Base):
    """Modelo de datos para una galería."""

    id: int
    name: str  # Nombre de la galería


class UsersState(rx.State):
    """Estado para la página de usuarios"""
    users: list[Dict[str, Any]] = []  # Especificamos el tipo
    is_loading: bool = False
    error: str = ""
    token: str = rx.LocalStorage(name="auth_token")

    async def get_users(self):
        """Obtiene la lista de usuarios desde la API"""
        self.is_loading = True
        self.error = ""
        try:
            client = APIClient()
            # Usando la función genérica que creamos
            response = await client.make_request("/users", self.token)
            if "error" in response:
                self.error = response["error"]
            else:
                self.users = response
        except Exception as e:
            self.error = f"Error al cargar usuarios: {str(e)}"
        finally:
            self.is_loading = False

def users_table():
    """Componente de tabla de usuarios"""
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Nombre"),                
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Acciones"),  # Nueva columna
            ),
        ),
        rx.table.body(
            rx.foreach(
                UsersState.users, generate_user_row
            )
        ),
        width="100%",
    )

def generate_user_row(user: User):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(user.id),
        rx.table.cell(user.name),        
        rx.table.cell(user.email),
        rx.table.cell(
            rx.button(
                "Editar",
                #on_click=lambda: UsersState.handle_edit(user.id),
                color_scheme="blue",
                #size="sm",
            )
        ),
    )



@require_auth
def users():
    """Página de usuarios"""
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.heading("Usuarios del Sistema"),
            rx.button(
                "Actualizar",
                on_click=UsersState.get_users,
                # is_loading=UsersState.is_loading,
                color_scheme="blue",
                margin_bottom="4",
            ),
            rx.cond(
                UsersState.error != "",
                rx.text(UsersState.error, color="red"),
            ),
            rx.cond(
                UsersState.is_loading,
                rx.spinner(),
                users_table(),
            ),
            padding="4",
            spacing="4",
            width="100%",
            max_width="1200px",
            margin="0 auto",
        ),
        width="100%",
        spacing="0",
    )