from odoo import models, fields, api

class WikiSection(models.Model):
    _name = 'wiki.section'
    _description = 'Wiki Section'
    _order = 'sequence, name'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    sequence = fields.Integer(string="Orden", default=10)
    article_ids = fields.One2many('wiki.article', 'section_id', string="Artículos")
    linked_article_ids = fields.Many2many(
        'wiki.article',
        string="Artículos asignados",
        compute="_compute_linked_article_ids",
        inverse="_inverse_linked_article_ids",
    )

    @api.depends('article_ids')
    def _compute_linked_article_ids(self):
        for rec in self:
            rec.linked_article_ids = rec.article_ids

    def _inverse_linked_article_ids(self):
        for rec in self:
            current = set(rec.article_ids.ids)
            target = set(rec.linked_article_ids.ids)
            to_add = target - current
            to_remove = current - target
            if to_add:
                self.env['wiki.article'].browse(list(to_add)).write({'section_id': rec.id})
            if to_remove:
                self.env['wiki.article'].browse(list(to_remove)).write({'section_id': False})