from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class FormulaExceptions:
    class FormulaCreateException(AppExceptionCase):
        """_
        Formula creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando la fórmula"
            AppExceptionCase.__init__(self, status_code, msg)

    class FormulaNotFoundException(AppExceptionCase):
        """_
        Formula's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID de la fórmula no se encuentra en la base de datos"
            AppExceptionCase.__init__(self, status_code, msg)

    class FormulaIdNoValidException(AppExceptionCase):
        """_
        Formula ID invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "ID de la fórmula inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class FormulaInvalidUpdateParamsException(AppExceptionCase):
        """_
        Formula invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización de la fórmula inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)
            
    class FormulaInvalidWarehouseIdException(AppExceptionCase):
        """_
        Formula invalid warehouse id
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "ID de almacén inválido para la fórmula"
            AppExceptionCase.__init__(self, status_code, msg)
            
    class FormulaInvalidProductIdException(AppExceptionCase):
        """_
        Product invalid formula id
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "ID del producto inválido para la fórmula"
            AppExceptionCase.__init__(self, status_code, msg)