from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class PriceExceptions:
    class PriceCreateException(AppExceptionCase):
        """_
        Price creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando el precio"
            AppExceptionCase.__init__(self, status_code, msg)

    class PriceNotFoundException(AppExceptionCase):
        """_
        Price's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la DB"
            AppExceptionCase.__init__(self, status_code, msg)

    class PriceIdNoValidException(AppExceptionCase):
        """_
        Price ID invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de precio inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class PriceInvalidUpdateParamsException(AppExceptionCase):
        """_
        Price Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)
            
    class PriceInvalidWarehouseIdException(AppExceptionCase):
        """_
        Price Invalid warehouse id
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de almacén inválido"
            AppExceptionCase.__init__(self, status_code, msg)
