# fotoflow/components/auth_wrapper.py
"""
Componente de autenticación (Auth Wrapper).

Este módulo proporciona un decorador 'require_auth' que protege las rutas
que requieren autenticación. Cuando se aplica a un componente:

1. Verifica si el usuario está autenticado usando AuthState
2. Si está autenticado, muestra el componente original
3. Si no está autenticado, muestra una pantalla de acceso denegado
   con opción para ir a la página de login

Uso:
    @require_auth
    def protected_component():
        return rx.text("Este contenido solo es visible para usuarios autenticados")

"""

import reflex as rx
from ..state.auth_state import AuthState

def require_auth(component):
    def wrapper():

        return rx.fragment(
            rx.cond(
                AuthState.is_authenticated,  
                component(),
                rx.box(
                    rx.vstack(
                        rx.heading("Acceso denegado", size="4"),
                        rx.text("Por favor inicie sesión para continuar"),
                        rx.button(
                            "Iniciar sesión",
                            on_click=AuthState.handle_logout,  
                            color_scheme="blue",
                        ),
                        padding="4",
                        spacing="4",
                        align_items="center",
                        justify_content="center",
                    ),
                    width="100%",
                    height="100vh",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                )
            )
        )
    return wrapper