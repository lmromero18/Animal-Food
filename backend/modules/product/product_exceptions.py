from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class ProductExceptions:
    class ProductCreateException(AppExceptionCase):
        """_
        Product creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando el producto"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductNotFoundException(AppExceptionCase):
        """_
        Product's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la DB"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductIdNoValidException(AppExceptionCase):
        """_
        Product Id invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de producto inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductInvalidUpdateParamsException(AppExceptionCase):
        """_
        Product Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)