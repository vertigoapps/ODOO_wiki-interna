from odoo import models, fields, api

class WikiArticle(models.Model):
    _name = 'wiki.article'
    _description = 'Wiki Article'
    _order = 'create_date desc'

    name = fields.Char(string="Título", required=True)
    body = fields.Html(string="Contenido", sanitize=False)
    category_id = fields.Many2one("wiki.category", string="Categoría", required=True)
    section_id = fields.Many2one("wiki.section", string="Sección", ondelete="set null")
    tag_ids = fields.Many2many('wiki.tag', string="Etiquetas")
    author_id = fields.Many2one('res.users', string="Autor", default=lambda self: self.env.user)
    is_public = fields.Boolean(string="Visible para todos", default=False)
    is_locked = fields.Boolean(string="Solo lectura", help="Solo Admin y Socios pueden editar o borrar", default=False)
    locked_for_user = fields.Boolean(compute="_compute_locked_for_user")
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'wiki.article')])

    @api.depends("is_locked")
    def _compute_locked_for_user(self):
        can_edit = self._is_admin_and_socios()
        for rec in self:
            rec.locked_for_user = rec.is_locked and not can_edit

    def _is_admin_and_socios(self):
        uid = self.env.uid
        if uid == 1:
            return True
        user = self.env['res.users'].browse(uid)
        return user.has_group('wiki_interna.group_wiki_admin') or user.has_group('wiki_interna.group_wiki_socios')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for vals, record in zip(vals_list, records):
            if "attachment_ids" in vals:
                record._link_attachment_ids()
        return records

    def write(self, vals):
        res = super().write(vals)
        if "attachment_ids" in vals:
            self._link_attachment_ids()
        return res

    def _link_attachment_ids(self):
        for article in self:
            missing = self.env["ir.attachment"].search([
                ("res_id", "=", article.id),
                ("res_model", "in", [False, ""]),
            ])
            if missing:
                missing.write({"res_model": article._name})

    def read(self, fields=None, load='_classic_read'):
        """Override para incluir body en search_read"""
        return super().read(fields=fields, load=load)