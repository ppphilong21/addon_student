# -*- coding: utf-8 -*-

from odoo import models, fields


class student_major(models.Model):
    _name = 'student.major'
    _description = 'Major'
    name = fields.Char(string="Name", required=True)
