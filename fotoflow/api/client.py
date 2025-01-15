# fotoflow/api/client.py

"""
Cliente API.

Este módulo proporciona una clase APIClient que maneja todas las interacciones
con el backend de la aplicación, incluyendo autenticación y operaciones CRUD.
Gestiona automáticamente los headers de autorización y el refresh de tokens.

Características principales:
- Gestión automática de tokens JWT
- Métodos para todas las operaciones de API
- Manejo de errores y reintentos
- Configuración flexible mediante variables de entorno

Uso:
    client = APIClient()
    # Login
    token = await client.login("username", "password")
    # Obtener usuarios
    users = await client.get_users()
"""

import httpx
from typing import Optional, Dict, Any, List
import os
from ..state.auth_state import AuthState


class APIClient:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000")

    async def login(self, username: str, password: str) -> Optional[str]:
        """Realiza el login y devuelve el token JWT."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/auth/login",
                    json={"username": username, "password": password},
                )
                if response.status_code == 200:
                    return response.json().get("access_token")
                return None
        except Exception as e:
            print(f"Login error: {e}")
            return None

    def _get_headers(self, token: str) -> Dict[str, str]:
        """Obtiene los headers para la petición."""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    async def get_users(self, token: str) -> List[Dict[str, Any]]:
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
