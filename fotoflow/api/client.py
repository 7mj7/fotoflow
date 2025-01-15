# fotoflow/api/client.py



import httpx
from typing import Optional, Dict, Any, List
import os
#from ..state.auth_state import AuthState


class APIClient:

    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000")

    

    def _get_headers(self, token: str) -> Dict[str, str]:
        """Obtiene los headers para la petición."""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    async def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """
        Realiza la autenticación y devuelve los datos de la respuesta.

        :param username: El nombre de usuario para la autenticación.
        :param password: La contraseña para la autenticación.
        :return: Un diccionario con los datos de la respuesta de autenticación.
        """
        data = {
            "username": username,
            "password": password,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/token",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Usuario o contraseña incorrectos"}

    async def get_users(self, token: str) -> List[Dict[str, Any]]:

        print(f"Token: {token}")
        """Obtiene la lista de usuarios."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/users", headers=self._get_headers(token)
                )
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
