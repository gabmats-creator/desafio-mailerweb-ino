from fastapi import HTTPException


class DomainError(Exception):
    def __init__(
        self,
        message: str = "Ocorreu um erro inesperado no domínio!",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class InfraError(Exception):
    def __init__(
        self,
        code: int = 500,
        message: str = "Ocorreu um erro inesperado na infra",
    ) -> None:
        self.code = code
        self.message = message
        super().__init__(self.message)


class RequiresAuthError(InfraError):
    def __init__(
        self,
        message: str = "Requer autenticação",
    ) -> None:
        super().__init__(401, message)


class ForbiddenError(InfraError):
    def __init__(
        self,
        message: str = "Acesso proibido",
    ) -> None:
        super().__init__(403, message)


class UserNotAuthorizedError(DomainError):
    def __init__(self, message: str = "Usuário não autorizado!") -> None:
        super().__init__(message)


class EntityNotFoundError(DomainError):
    def __init__(self, message: str = "Entidade não encontrada!") -> None:
        super().__init__(message)


class CustomValidationError(DomainError):
    def __init__(
        self,
        message: str = "A entidade possui campos inválidos!",
    ) -> None:
        super().__init__(message)


class InvalidFieldError(DomainError):
    def __init__(self, field: str) -> None:
        self.message = f"O campo {field} é invalido!"
        super().__init__(self.message)


class RequiredFieldError(DomainError):
    def __init__(self, field: str) -> None:
        self.message = f"Campo necessário: {field}!"
        super().__init__(self.message)


class InvalidFileError(Exception):
    def __init__(
        self,
        code: int = 422,
        message: str = "Tipo do arquivo é inválido!",
    ) -> None:
        self.status_code = code
        self.message = message
        super().__init__(self.message)


class BadRequestError(Exception):
    def __init__(
        self,
        code: int = 400,
        message: str = "Requisição inválida!",
    ) -> None:
        self.status_code = code
        self.message = message
        super().__init__(self.status_code, self.message)


class NotFoundError(Exception):
    def __init__(
        self,
        code: int = 404,
        message: str = "Não encontrado!",
    ) -> None:
        self.status_code = code
        self.message = message
        super().__init__(self.status_code, self.message)


class ExternalServiceError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class PermissionDeniedServiceError(HTTPException):
    def __init__(
        self,
        status_code: int = 403,
        message: str = "Usuário não tem permissão para acessar este recurso.",
    ) -> None:
        super().__init__(status_code=status_code, detail=message)


class InternalServerError(Exception):
    def __init__(
        self,
        message: str = "Erro interno do servidor",
    ) -> None:
        super().__init__(500, message)


class NotApproveError(DomainError):
    def __init__(
        self,
        message: str = "Erro ao aprovar a solicitação",
    ) -> None:
        super().__init__(message)


class BusinessRuleError(BadRequestError):
    def __init__(
        self,
        message: str = "Regra de negócio violada",
    ) -> None:
        super().__init__(message=message)
