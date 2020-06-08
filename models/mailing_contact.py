# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class IsSegment(models.Model):
    _name = 'is.segment'
    _description = "Segment"
    _order = 'name'

    name = fields.Char("Segment", required=True, index=True)


class IsRegion(models.Model):
    _name = 'is.region'
    _description = "Région"
    _order = 'name'

    name = fields.Char("Région", required=True, index=True)


class MassMailingContact(models.Model):
    _inherit = 'mailing.contact'

    is_code_ape      = fields.Char(string='Code APE')
    is_ville         = fields.Char(string='Ville')
    is_code_postal   = fields.Char(string='Code Postal')
    is_rue           = fields.Char(string='Rue')
    is_region_id     = fields.Many2one('is.region', "Région")
    is_telephone     = fields.Char(string='Numéro de téléphone')
    is_fax           = fields.Char(string='Numéro de fax')
    is_site_internet = fields.Char(string='Site internet')
    is_segment_id    = fields.Many2one('is.segment', "Segment")


    def add_last_mailing_list_action(self):
        lists = self.env['mailing.list'].search([], limit=1, order='id desc')
        if len(lists):
            for obj in self.browse(self.env.context['active_ids']):
                list_id = lists[0].id
                ids=[]
                for line in obj.subscription_list_ids:
                    ids.append(line.list_id.id)
                if list_id not in ids:
                    vals={
                        'list_id'   : list_id,
                        'contact_id': obj.id,
                    }
                    res = self.env['mailing.contact.subscription'].create(vals)
                    print(obj, list_id,res)

