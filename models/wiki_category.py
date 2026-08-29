from odoo import models, fields, api

class WikiCategory(models.Model):
    _name = 'wiki.category'
    _description = 'Wiki Category'
    _order = 'name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    parent_id = fields.Many2one('wiki.category', string="Categoría padre", ondelete='cascade')
    child_ids = fields.One2many('wiki.category', 'parent_id', string="Subcategorías")
    article_ids = fields.One2many('wiki.article', 'category_id', string="Artículos")
    user_ids = fields.Many2many('res.users', string="Usuarios asignados")
    color = fields.Integer(string="Color")
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El nombre de la categoría debe ser único"),
    ]
