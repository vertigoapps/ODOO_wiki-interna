from odoo import models, fields

class WikiTag(models.Model):
    _name = 'wiki.tag'
    _description = 'Wiki Tag'
    _order = 'name'

    name = fields.Char(string="Etiqueta", required=True, size=50)
    article_ids = fields.Many2many('wiki.article', string="Artículos")
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "La etiqueta debe ser única"),
    ]
