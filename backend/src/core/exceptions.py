class BaseError(Exception):
    """Simplifies creation of custom errors by using msg from declared class attr
    without need of overriding init"""

    msg: str = "base error"

    def __init__(self, custom_msg: str | None = None):
        msg = custom_msg or self.msg
        self.msg = msg
        return super().__init__(msg)
