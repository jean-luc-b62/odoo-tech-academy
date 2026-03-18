from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of Properties"

    _sql_constraints = [
        ("check_name_unique", "unique(name)", "The Tag's name must be unique."),
    ]

    name = fields.Char(required=True)
