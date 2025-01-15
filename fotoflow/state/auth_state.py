# fotoflow/state/auth_state.py

import reflex as rx

from fotoflow.api.client import APIClient

class AuthState(rx.State):
    """Estado global para la autenticación."""
    is_authenticated: bool = False
    token: str = rx.LocalStorage(name="auth_token")
    error: str = ""
    loading: bool = False
    username: str = "fotografo@example.com" # valor por defecto
    password: str = "foto123"               # valor por defecto
    

    @rx.var(cache=True) # Importante el decorador para que sea accesible 
    def is_logged_in(self) -> bool:        
        return self.is_authenticated  
    
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
                self.auth_token = ""
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
        self.is_authenticated = False
        self.token = ""        
        rx.remove_local_storage("token")
        return rx.redirect("/login")
    
    