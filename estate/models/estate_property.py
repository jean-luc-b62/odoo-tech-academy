from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Orientation of the garden attached to this property.",
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner")
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.garden_area + prop.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            if prop.offer_ids:
                prop.best_price = max(prop.offer_ids.mapped("price"))
            else:
                prop.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sell_property(self):
        if any(prop.state == "cancelled" for prop in self):
            raise UserError(_("You cannot sell cancelled properties."))
        self.state = "sold"

    def action_cancel_property(self):
        self.state = "cancelled"
