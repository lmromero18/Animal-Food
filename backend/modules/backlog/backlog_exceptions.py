from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class BacklogExceptions:
    class BacklogCreateException(AppExceptionCase):
        """_
        Backlog creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando el backlog"
            AppExceptionCase.__init__(self, status_code, msg)

    class BacklogNotFoundException(AppExceptionCase):
        """_
        Backlog's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la DB"
            AppExceptionCase.__init__(self, status_code, msg)

    class BacklogIdNoValidException(AppExceptionCase):
        """_
        Backlog Id invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de backlog inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class BacklogInvalidUpdateParamsException(AppExceptionCase):
        """_
        Backlog Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)
