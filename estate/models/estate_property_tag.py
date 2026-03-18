from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of Properties"

    _check_name_unique = models.Constraint("unique(name)", "The Tag's name must be unique.")

    name = fields.Char(required=True)
