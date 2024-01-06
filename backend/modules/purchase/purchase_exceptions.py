from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class PurchaseExceptions:
    class PurchaseCreateException(AppExceptionCase):
        """_
        Purchase creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando la compra"
            AppExceptionCase.__init__(self, status_code, msg)

    class PurchaseNotFoundException(AppExceptionCase):
        """_
        Purchase's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la DB"
            AppExceptionCase.__init__(self, status_code, msg)

    class PurchaseIdNoValidException(AppExceptionCase):
        """_
        Purchase Id invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de compra inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class PurchaseInvalidUpdateParamsException(AppExceptionCase):
        """_
        Purchase Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)
            
