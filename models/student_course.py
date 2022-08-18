# -*- coding: utf-8 -*-

from odoo import models, fields


class student_course(models.Model):
    _name = 'student.course'
    _description = 'Course'
    name = fields.Char(string="Name", required=True)
    student_ids = fields.One2many('student.student', 'course_id', string='List students')
