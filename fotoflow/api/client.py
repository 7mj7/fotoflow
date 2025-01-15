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


    async def make_request(
        self, 
        endpoint: str, 
        token: str, 
        method: str = "GET", 
        data: Dict = None
    ) -> Dict[str, Any]:
        """
        Función genérica para hacer peticiones a la API.
        
        Args:
            endpoint: Ruta del endpoint (ej: '/users')
            token: Token de autenticación
            method: Método HTTP ('GET', 'POST', 'PUT', 'DELETE')
            data: Datos para enviar en el body (opcional)
        """
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}{endpoint}"
                headers = self._get_headers(token)
                
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    response = await client.post(url, headers=headers, json=data)
                elif method == "PUT":
                    response = await client.put(url, headers=headers, json=data)
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers)
                
                if response.status_code == 200:
                    return response.json()
                return {"error": f"Status code: {response.status_code}"}
                
        except Exception as e:
            print(f"Error in API request: {e}")
            return {"error": str(e)}


    # Métodos específicos usando la función genérica
    async def get_users(self, token: str) -> List[Dict[str, Any]]:
        response = await self.make_request("/users", token)
        print(f"Response: {response}")
        return response if not response.get("error") else []
    

    '''async def get_users(self, token: str) -> List[Dict[str, Any]]:        
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
            return []'''
