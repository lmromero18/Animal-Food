from decimal import Decimal
from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class OrderExceptions:
    class OrderCreateException(AppExceptionCase):
        """_
        Order creation failed
        """

        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando el pedido"
            AppExceptionCase.__init__(self, status_code, msg)

    class OrderNotFoundException(AppExceptionCase):
        """_
        Order's ID not found
        """

        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "El ID suministrado no se encuentra en la DB"
            AppExceptionCase.__init__(self, status_code, msg)

    class OrderIdNoValidException(AppExceptionCase):
        """_
        Order Id invalid
        """

        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "Id de pedido inválido"
            AppExceptionCase.__init__(self, status_code, msg)

    class OrderInvalidUpdateParamsException(AppExceptionCase):
        """_
        Order Invalid update parameters
        """

        def __init__(self, msg: str = "", e: Any = None):
            error = e
            status_code = 422
            msg = f"Parámetros de actualización inválidos: {str(error)}"
            AppExceptionCase.__init__(self, status_code, msg)

    class OrderDiscountException(AppExceptionCase):
      """_
      Order Discount Exception
      """
    
      def __init__(self, total: Decimal, discount: Decimal, msg: str = ""):
          self.total = total
          self.discount = discount
          status_code = 422
          msg = f"Descuento inválido: El descuento ({self.discount}) no puede ser mayor al total ({self.total})."
          AppExceptionCase.__init__(self, status_code, msg)

    class OrderQuantityException(AppExceptionCase):
      """_
      Order Quantity Exception
      """
    
      def __init__(self, stock: int, quantity: int, msg: str = ""):
          self.stock = stock
          self.quantity = quantity
          status_code = 422
          msg = f"Cantidad inválida: La cantidad ({self.quantity}) no puede ser mayor al stock ({self.stock})."
          AppExceptionCase.__init__(self, status_code, msg)
          
    class OrderQuantityNotAvailableException(AppExceptionCase):
      """_
      Order Quantity Exception
      """
    
      def __init__(self, stock: int, quantity: int, msg: str = ""):
          self.stock = stock
          self.quantity = quantity
          status_code = 422
          msg = f"Cantidad inválida: La cantidad ({self.quantity}) no puede ser mayor al stock ({self.stock})."
          AppExceptionCase.__init__(self, status_code, msg)