from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class WarehouseExceptions:
    class WarehouseCreateException(AppExceptionCase):
        """_
        Warehouse creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando el almacén"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseNotFoundException(AppExceptionCase):
        """_
        Warehouse's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la DB"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseIdNoValidException(AppExceptionCase):
        """_
        Warehouse Id invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de almacén inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseInvalidUpdateParamsException(AppExceptionCase):
        """_
        Warehouse Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)
            