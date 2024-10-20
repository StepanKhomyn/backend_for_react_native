from marshmallow import Schema, fields, EXCLUDE


class ChallengeSchema(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True)  # Наприклад: "food", "active_recreation", "architectural_landmarks"
    photo = fields.Str(required=True)
    description = fields.Str(required=False)
    location = fields.Str(required=True)
    short_location = fields.Str(required=True)
    rating = fields.Float(required=True, default=0)
    completed = fields.Int(required=True, default=0)
    participants = fields.Int(required=True, default=0)
    experience = fields.Int(required=True, default=0)

    class Meta:
        unknown = EXCLUDE  # Skip unknown fields during validation


class UpdateChallengeSchema(Schema):
    name = fields.Str(required=True)
    photo = fields.Str(required=True)
    description = fields.Str(required=False)
    location = fields.Str(required=True)
    short_location = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE  # Skip unknown fields during validation