from datetime import date
from marshmallow import Schema, fields


class QuestionSchema(Schema):
    text = fields.Str()
    images = fields.List(fields.Str())
    videos = fields.List(fields.Str())

class RelatedQuestionsSchema(Schema):
    data = fields.List(fields.Nested(QuestionSchema))