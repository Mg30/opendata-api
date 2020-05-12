from marshmallow import Schema, fields


class RecordSchema(Schema):
    start_time = fields.Str()
    end_time = fields.Str()
    verification = fields.Int()
    validity = fields.Int()
    value = fields.Float()


class ObservationSchema(Schema):
    polluant = fields.Str()
    records = fields.List(fields.Nested(RecordSchema))
