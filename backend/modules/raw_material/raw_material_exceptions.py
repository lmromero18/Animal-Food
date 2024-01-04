from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class RawMaterialExceptions:
    class RawMaterialCreateException(AppExceptionCase):
        """_
        Raw material creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando la materia prima"
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialNotFoundException(AppExceptionCase):
        """_
        Raw material's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la DB"
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialIdNoValidException(AppExceptionCase):
        """_
        Raw material ID invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de materia prima inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialInvalidUpdateParamsException(AppExceptionCase):
        """_
        Raw material Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)
            
    class RawMaterialInvalidWarehouseIdException(AppExceptionCase):
        """_
        Raw material Invalid warehouse id
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de almacén inválido"
            AppExceptionCase.__init__(self, status_code, msg)