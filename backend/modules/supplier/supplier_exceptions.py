from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class SupplierExceptions:
    class SupplierCreateException(AppExceptionCase):
        """_
        Supplier creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando el proveedor"
            AppExceptionCase.__init__(self, status_code, msg)

    class SupplierNotFoundException(AppExceptionCase):
        """_
        Supplier's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la DB"
            AppExceptionCase.__init__(self, status_code, msg)

    class SupplierIdNoValidException(AppExceptionCase):
        """_
        Supplier ID invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de proveedor inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class SupplierInvalidUpdateParamsException(AppExceptionCase):
        """_
        Supplier Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)
            
    class SupplierInvalidWarehouseIdException(AppExceptionCase):
        """_
        Supplier Invalid warehouse id
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de almacén inválido"
            AppExceptionCase.__init__(self, status_code, msg)
