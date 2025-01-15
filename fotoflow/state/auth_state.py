# fotoflow/state/auth_state.py

"""
Módulo de Estado de Autenticación.

Este módulo implementa el estado global de autenticación usando Reflex State.
Gestiona todo el ciclo de vida de la autenticación de usuarios, incluyendo:

Funcionalidades:
- Manejo del token JWT y estado de autenticación
- Proceso de login/logout
- Gestión de errores de autenticación
- Estado de carga durante operaciones asíncronas
- Almacenamiento temporal de credenciales

Variables de estado:
- token: Almacena el token JWT actual
- is_authenticated: Boolean que indica si el usuario está autenticado
- error: Mensajes de error durante la autenticación
- loading: Estado de carga durante operaciones
- username/password: Credenciales temporales durante el login

Uso:
    auth_state = AuthState()
    # Login
    await auth_state.handle_login()
    # Verificar autenticación
    if auth_state.is_authenticated:
        # Usuario autenticado
    # Logout
    auth_state.handle_logout()


"""

import reflex as rx
import httpx

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

            print (f"Username: {self.username}")
            print (f"Password: {self.password}")

            # Preparar los datos para enviar en formato x-www-form-urlencoded
            data = {
                "username": self.username,
                "password": self.password,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/token",
                    data=data,  # usa 'data' para form-urlencoded
                    headers={"Content-Type": "application/x-www-form-urlencoded"},                    
                )

                
                #print (f"Status code: {response.status_code}")
                #print (f"Response content: {response.content}")
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get("access_token", "")
                    self.is_authenticated = bool(self.token)
                    self.username = ""
                    self.password = ""
                    return rx.redirect("/dashboard")
                else:
                    self.error = "Usuario o contraseña incorrectos"
        except Exception as e:
            self.error = str(e)
        finally:
            self.loading = False

    def handle_logout(self):
        """Método para hacer logout."""
        self.token = ""
        self.is_authenticated = False
        return rx.redirect("/login")