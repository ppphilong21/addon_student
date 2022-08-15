# -*- coding: utf-8 -*-

from odoo import models, fields


class student_student(models.Model):
    _name = 'student.student'
    _description = 'Student'

    name = fields.Char(string='Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    photo = fields.Binary(string='Photo')
    student_dob = fields.Date(string="Date of Birth")
    student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender')
    course_id = fields.Many2one('student.course', 'Course', required=True)
    major_id = fields.Many2one('student.major', 'Major', required=True)
