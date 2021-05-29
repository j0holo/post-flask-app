class UserNotFoundError(Exception):
    pass


class IncorrectPassword(Exception):
    pass


class PasswordsDoNotMatch(Exception):
    pass


class InvalidEmail(Exception):
    pass


class PostNotFoundError(Exception):
    pass


# TODO: Implements this way of exception and exception handler.
#    class UserNotFoundError(Exception):
#         error = {"error": "This user was not found"}

#     def catch_exception(e: Exception)
#     # errors = {
#     #     "error1": Exception1,
#     #     "error2": Exception2,
#     # }
#     if e is not Exception:
#         return e.error
#     else:
#         return {"error": "generic error message"}
