""" Module providing serialization schema for
models module using marshmallow librairies
ref : https://marshmallow.readthedocs.io/en/stable/
"""

from marshmallow import Schema, fields


class RecordSchema(Schema):
    """ Schema for serialization of model Record """
    start_time = fields.Str()
    end_time = fields.Str()
    verification = fields.Int()
    validity = fields.Int()
    value = fields.Float()


class ObservationSchema(Schema):
    """ Schema for serialization model Observation """
    polluant = fields.Str()
    sample_point = fields.Str()
    records = fields.List(fields.Nested(RecordSchema))
