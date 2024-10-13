from marshmallow import Schema, fields

class UserSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)
    age = fields.Int(required=False)


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class TokenSchema(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
