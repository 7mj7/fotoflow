# fotoflow/state/auth_state.py

import reflex as rx
#import httpx

from fotoflow.api.client import APIClient

class AuthState(rx.State):
    """Estado global para la autenticación."""
    token: str = ""
    is_authenticated: bool = False
    error: str = ""
    loading: bool = False
    username: str = ""
    password: str = ""

    @rx.var(cache=True) # Importante el decorador para que sea accesible 
    def is_logged_in(self) -> bool:
        #return bool(self.token)
        return self.is_authenticated  # Usamos is_authenticated en lugar de token
    
    def set_username(self, username: str):
        """Establece el nombre de usuario."""
        self.username = username
        self.error = ""  # Limpiar errores previos

    def set_password(self, password: str):
        """Establece la contraseña."""
        self.password = password
        self.error = ""  # Limpiar errores previos    

    async def handle_login(self):
        """Método para hacer login."""
        try:
            self.loading = True
            self.error = ""

            api_client = APIClient()
            auth_response = await api_client.authenticate(self.username, self.password)
            
            if "error" in auth_response:
                self.error = auth_response["error"]
            else:
                self.token = auth_response.get("access_token", "")
                self.is_authenticated = bool(self.token)
                self.username = ""
                self.password = ""
                return rx.redirect("/dashboard")
        
        except Exception as e:
            self.error = str(e)
        finally:
            self.loading = False

    def handle_logout(self):
        """Método para hacer logout."""
        self.token = ""
        self.is_authenticated = False
        return rx.redirect("/login")