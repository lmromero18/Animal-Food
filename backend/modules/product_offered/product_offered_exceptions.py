from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class ProductOfferedExceptions:
    class ProductOfferedCreateException(AppExceptionCase):
        """_
        Product offered creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando el producto ofrecido"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductOfferedNotFoundException(AppExceptionCase):
        """_
        Product offered's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID del producto ofrecido no se encuentra en la base de datos"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductOfferedIdNoValidException(AppExceptionCase):
        """_
        Product offered ID invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "ID del producto ofrecido inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductOfferedInvalidUpdateParamsException(AppExceptionCase):
        """_
        Product offered invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización del producto ofrecido inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)
            
    class ProductOfferedInvalidWarehouseIdException(AppExceptionCase):
        """_
        Product offered invalid warehouse id
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "ID de almacén inválido para el producto ofrecido"
            AppExceptionCase.__init__(self, status_code, msg)
            
    class ProductOfferedInvalidProductIdException(AppExceptionCase):
        """_
        Product offered invalid product id
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "ID de producto inválido para el producto ofrecido"
            AppExceptionCase.__init__(self, status_code, msg)