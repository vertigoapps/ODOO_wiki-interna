from odoo import models, fields, api


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    preview_image = fields.Binary(string="Vista previa", compute="_compute_preview_image")

    @api.depends("mimetype", "datas")
    def _compute_preview_image(self):
        for record in self:
            if not (record.mimetype and record.mimetype.startswith("image")):
                record.preview_image = False
                continue
            data = record.datas
            record.preview_image = data.decode() if isinstance(data, bytes) else data