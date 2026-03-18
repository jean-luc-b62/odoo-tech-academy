from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
	_description = "Estate Property Model"

	name = fields.Char()
