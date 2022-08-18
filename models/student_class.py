# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student_class(models.Model):
    _name = 'student.class'
    _description = 'Class'
    name = fields.Char(string='Name Class', required=True) #active when subject_code exist
    class_code = fields.Char(string="Class Code", required=True)
    subject_name = fields.Many2one('student.subject', 'Subject')
    student_id = fields.Many2one('student.student', 'Student')
    major_id = fields.Many2one('student.major', 'Major')


    # def action_add_student(self):
    #     class_current = self.env['student.class'].browse(self.id)



""" 
 @api.constrains('subject_code')
    def check_duplicate_student(self):
        student_subject_check = self.env['student.subject'].search([
            ('subject_code', '=', self.subject_code),
            ('id', '!=', self.id)
        ])
        if student_subject_check:
            print("Check List Duplicate")
            raise ValueError(('Exists ! Already existed this code in this name'))


def action_add_student(self, name, subject_code, student_id):
    print(self.name)
    new_create = {
        'name': name,
        'subject_code': subject_code,
        'student_id': student_id
    }
    self.env['student.register'].create(new_create)"""




