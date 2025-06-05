from fastapi import Response

class SetTokenCookie():
    def __init__(self,
                 token: str, 
                 key: str = 'refresh_token',
                 httponly: bool = True,
                 secure: bool = True,
                 samesite: str = 'lax',
                 max_age: int = 60*60*24*7, 
                 ):
        self.key = key
        self.value = token
        self.httponly = httponly
        self.secure = secure
        self.samesite = samesite
        self.max_age = max_age

    def create_response(self, response: Response):
        response.set_cookie(
            key= self.key,
            value=self.value,
            httponly=self.httponly,
            secure=self.secure,
            samesite=self.samesite,
            max_age=self.max_age,
        )
        return response

    def delete_cookie(self, response: Response):
        response.delete_cookie(response)

        return response
