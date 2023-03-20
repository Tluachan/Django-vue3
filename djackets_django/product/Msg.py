from rest_framework import serializers
from rest_framework.response import Response

class Msg(serializers.Serializer):
    code = 200
    msg = ""
    data = None

    def __init__(self,  msg=None, data=None,code=200):
        self.code = code
        self.msg = msg
        self.data = data
    
    def serialize(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }

    def response(self):
        return Response(self.serialize())
