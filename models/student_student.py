# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class student_student(models.Model):
    _name = 'student.student'
    _description = 'Student'

    student_code = fields.Char(string="Student Code", required=True)
    name = fields.Char(string='Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    photo = fields.Binary(string='Photo')
    student_dob = fields.Date(string="Date of Birth")
    student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender')
    course_id = fields.Many2one('student.course', 'Course')
    major_id = fields.Many2one('student.major', 'Major')
    student_state = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], string='Status')
    student_class = fields.One2many('student.class', 'student_id', string="Class Joined")

    @api.constrains('student_code')
    def check_duplicate_student(self):
        student_check = self.env['student.student'].search([
            ('student_code', '=', self.student_code),
            ('id', '!=', self.id)
        ])
        #Error User
        if student_check:
            print("Check List Duplicate")
            raise ValueError(('Exists ! Already a vendor exists in this name'))

    @api.onchange('course_id')
    def check_change(self):
        if self.course_id:
            print('CHECK CHANGING')
            print(type(self.course_id))
            self.student_code = '{}{}'.format(self.course_id.name, self.student_code)
