# fotoflow/pages/dashboard.py
import reflex as rx
from ..components.auth_wrapper import require_auth
from ..state.auth_state import AuthState
from ..components.navbar import navbar  # Importar el navbar

def dashboard_content():
    """Contenido del dashboard que requiere autenticación"""
    return rx.vstack(
        navbar(),  # Incluir el navbar
        rx.vstack(
            rx.heading("FotoFlow Dashboard"),
            rx.text("Contenido del dashboard"),
            rx.button(
                "Salir",
                on_click=AuthState.handle_logout,
                color_scheme="red",
            ),
            padding="4",
            spacing="4",
        ),
        width="100%",
        #spacing="0",  # Eliminar espacio entre navbar y contenido
    )
def login_redirect():
    """Componente de redirección a login"""
    return rx.vstack(
        rx.script(
            "window.location.href = '/login'"
        )
    )

@require_auth
def dashboard():
    """Página principal del dashboard"""
    return rx.fragment(
        rx.cond(
            AuthState.is_authenticated,
            dashboard_content(),
            login_redirect()
        )
    )