# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

STUDENT_STATE = [
    ('active', u'Kích hoạt'), ('inactive', u'Chưa kích hoạt'),
]

class student_student(models.Model):
    _name = 'student.student'
    _description = 'Student'

    student_id = fields.Char(string="Student Code", required=True)
    name = fields.Char(string='Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    photo = fields.Binary(string='Photo')
    student_dob = fields.Date(string="Date of Birth")
    student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender')
    course_id = fields.Many2one('student.course', 'Course')
    major_id = fields.Many2one('student.major', 'Major')
    state_id = fields.One2many('student.state.active', 'student_id', string="Trạng thái Student")
    student_state = fields.Selection(STUDENT_STATE,
                                      string=u'Trạng thái hiện tại', default='active')
    student_class = fields.One2many('student.class', 'student_id', string="Class Joined")

    @api.multi
    def action_confirm_write(self):
        for rec in self:
            student_state = {
                'student_id': rec.id,
                'state': self.student_state
            }
            self.env['student.state.active'].create(student_state)
        #return super(student_student, self).write(student_state)

    @api.constrains('student_id')
    def check_duplicate_student(self):
        student_check = self.env['student.student'].search([
            ('student_id', '=', self.student_id),
            ('id', '!=', self.id)
        ])
        #Error User
        if student_check:
            print("Check List Duplicate")
            raise ValueError(('Exists ! Already a vendor exists in this name'))

    @api.onchange('course_id')
    def check_change(self):
        if self.course_id:
            print("CHECKING RESULT .................", self.student_state)
            self.student_id = '{}{}'.format(self.course_id.name, self.student_id)

class student_state_active(models.Model):
    _name = "student.state.active"
    _description = "Student State Active"
    state = fields.Selection(STUDENT_STATE, string="Trạng thái", defualt="active")
    student_id = fields.Many2one('student.student', string="Student")