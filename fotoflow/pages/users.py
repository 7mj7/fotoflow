# fotoflow/pages/users.py
import reflex as rx
from ..components.navbar import navbar
from ..components.auth_wrapper import require_auth

# Para las peticiones a la API
from ..api.client import APIClient

# --------------- Modelos ---------------
class User(rx.Base):
    """Modelo de datos para un usuario"""
    id: int
    name: str
    email: str

# --------------- Estados ---------------
class UsersState(rx.State):
    """Estado para la página de usuarios"""
    users: list[User] = []  
    is_loading: bool = False
    error: str = ""
    token: str = rx.LocalStorage(name="auth_token")


    # Función para obtener la lista de usuarios
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
                # self.users = response
                # Convertimos cada diccionario a un objeto User
                self.users = [User(**user) for user in response]
        except Exception as e:
            self.error = f"Error al cargar usuarios: {str(e)}"
        finally:
            self.is_loading = False


# --------------- Componentes ---------------

# Tabla de usuarios
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
        rx.table.body(rx.foreach(UsersState.users, generate_user_row)),
        width="100%",
    )


# Función para generar una fila de la tabla
def generate_user_row(user: User):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(user.id),
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(
            # boton para editar
            edit_user_dialog(user),
        ),
    )


@require_auth # Agregamos el decorador para proteger la página
def users():
    """Página de usuarios"""
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.heading("Usuarios del Sistema"),
            rx.button(
                "Actualizar",
                on_click=UsersState.get_users,
                is_loading=UsersState.is_loading,
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


# --------------- Dialogos ---------------


# Agregamos la definición del modal
def edit_user_dialog(user: User):
    """Componente Dialog para editar usuario"""
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Ver", color_scheme="blue")),
        rx.dialog.content(
            rx.dialog.title("Datos del Usuario"),
            # rx.dialog.description(
            #    "Descripción",
            #    size="2",
            #    margin_bottom="16px",
            # ),
            rx.form(
                rx.flex(
                    rx.text(
                        "CÓDIGO #",user.id,
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold",
                    ),
                    rx.text(                       
                        "Nombre",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold",
                    ),
                    rx.input(
                        default_value=user.name,  # este no se muestra
                        read_only=True,
                        # placeholder="Ingrese el nombre",
                        name="name",
                    ),
                    rx.text(
                        "Email",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold",
                    ),
                    rx.input(
                        default_value=user.email,
                        read_only=True,
                        # placeholder="Ingrese el email",
                        name="email",
                    ),
                    direction="column",
                    spacing="3",
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cerrar",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    # rx.dialog.close(
                    #    rx.button(
                    #        "Guardar",
                    #        type_="submit",
                    #    ),
                    # ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                # Como esto es una prueba, no usaremos on_submit
                # on_submit=UsersState.update_user,
            ),
        ),
    )
