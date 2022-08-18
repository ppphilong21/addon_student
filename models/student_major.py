# -*- coding: utf-8 -*-

from odoo import models, fields


class student_major(models.Model):
    _name = 'student.major'
    _description = 'Major'
    name = fields.Char(string="Name", required=True)
    major_code = fields.Char(string="Major Code", required=True)
    subject_id = fields.One2many('student.subject', 'major_id', string="Subject List" )