from functools import wraps
from fastapi import HTTPException
import traceback
import logging

from app.exceptions.base import BusinessRuleError, NotFoundError, RequiresAuthError


def handle_route_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Tenta executar a rota normalmente
            return await func(*args, **kwargs)

        except BusinessRuleError as e:
            # 1. Erros mapeados que vieram do Service com 'code' e 'message'
            raise HTTPException(status_code=e.status_code, detail=e.message)

        except RequiresAuthError as e:
            # 1. Erros mapeados que vieram do Service com 'code' e 'message'
            raise HTTPException(status_code=e.code, detail=e.message)

        except NotFoundError as e:
            # 1. Erros mapeados que vieram do Service com 'code' e 'message'
            raise HTTPException(status_code=e.status_code, detail=e.message)

        except HTTPException:
            # 2. Se já for um erro nativo do FastAPI (ex: erro de validação de Schema), deixa passar
            raise

        except Exception as e:
            # 3. O erro genérico 500 (Banco caiu, erro de sintaxe, etc)
            logging.error(f"Erro Crítico não tratado: {str(e)}")
            traceback.print_exc()  # Imprime no terminal para você debugar
            raise HTTPException(
                status_code=500, detail="Ocorreu um erro interno no servidor."
            )

    return wrapper
