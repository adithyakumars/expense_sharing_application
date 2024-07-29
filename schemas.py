from marshmallow import Schema, fields, validate, validates, ValidationError

class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    mobile_number = fields.Str(required=True, validate=validate.Length(min=10, max=15))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class ExpenseSchema(Schema):
    email = fields.Email(required=True)
    description = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    amount = fields.Float(required=True)
    split_method = fields.Str(required=True, validate=validate.OneOf(["equal", "exact", "percentage"]))
    split_details = fields.Dict(keys=fields.Email(), values=fields.Float(), required=False)

    @validates('split_details')
    def validate_split_details(self, value):
        if self.context['split_method'] == 'percentage':
            if sum(value.values()) != 100:
                raise ValidationError('Percentages must add up to 100')
