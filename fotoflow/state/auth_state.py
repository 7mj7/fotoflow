# state/auth_state.py

import reflex as rx
import os
import httpx

# import logging

# Configuración básica del logging
# logging.basicConfig(level=logging.INFO)


class AuthState(rx.State):
    """Estado para autenticación con Token Bearer."""

    username: str = ""
    password: str = ""
    is_authenticated: bool = False
    token: str = ""  # Almacena el token JWT
    token_storage: str = rx.LocalStorage(
        name="token"
    )  # Definir LocalStorage para persistencia del token

    error: str = ""

    
    def set_username(self, value: str):
        """Actualizar el nombre de usuario en el estado."""
        self.username = value

    def set_password(self, value: str):
        """Actualizar la contraseña en el estado."""
        self.password = value

    def get_token(self) -> str:
        """Obtiene el token como cadena de texto."""
        return self.token

    async def handle_login(self):
        """Manejar el inicio de sesión y almacenar el token."""

        if self.username == "" or self.password == "":
            return rx.window_alert("Por favor, complete todos los campos")

        try:
            # Preparar los datos para enviar en formato x-www-form-urlencoded
            data = {
                "username": self.username,
                "password": self.password,
            }

            # Realizar la solicitud POST al endpoint /token
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{os.getenv('API_URL', 'http://localhost:8000')}/token",
                    data=data,  # usa 'data' para form-urlencoded
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

            # logging.info(f"Status Code: {response.status_code}")
            # logging.debug(f"Response JSON: {response.json()}")
            # logging.debug(f"Response Text: {response.text}")

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token", "")
                if self.token:
                    self.token_storage = (
                        self.token
                    )  #  Almacenar el token en LocalStorage
                    self.is_authenticated = True
                    return rx.redirect(
                        "/dashboard"
                    )  # Redireccionar a la página de dashboard
                else:
                    return rx.window_alert("Token no recibido del servidor.")
            else:
                # Manejar errores de autenticación
                error = response.json().get("detail", "Error al autenticar")
                return rx.window_alert(f"Error: {error}")
        except httpx.RequestError as e:
            return rx.window_alert(f"Error de solicitud: {str(e)}")
        except Exception as e:
            return rx.window_alert(f"Error inesperado: {str(e)}")

    async def check_authentication(self):
        """Verificar si el usuario ya está autenticado al cargar la aplicación."""
        token = self.token_storage  # Leer directamente desde localStorage
        if token:
            self.token = token
            self.is_authenticated = True
        else:
            self.is_authenticated = False
            

    async def handle_logout(self):
        """Cerrar sesión y limpiar el token."""
        self.token = ""
        self.token_storage = ""  # Eliminar el token de localStorage
        self.is_authenticated = False
        # self.token_storage.remove()
        return rx.redirect("/login")
