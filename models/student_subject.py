# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student_subject(models.Model):
    _name = 'student.subject'
    _description = 'Subject'
    name = fields.Char(string="Name Subject", required=True)
    subject_code = fields.Char(string='Key Course', required=True)
    major_id = fields.Many2one('student.major', 'Major')
    subject_class = fields.Many2one('student.class', 'Class')
    subject_state = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], string='Status')

    #Create New Class By Name - SAI
    @api.model
    def name_create(self, subject_class):
        print("class name", subject_class)
        record_current = self.env['student.subject'].browse(self.id)
        new_create = self.create({
            'name': subject_class,
            'major_id': record_current.major_id,
            'subject_code': record_current.subject_code,
        })
        print("checking create", record_current.subject_code)
        return new_create.name_get()[0]

    @api.constrains('subject_code')
    def check_duplicate_student(self):
        student_subject_check = self.env['student.subject'].search([
            ('subject_code', '=', self.subject_code),
            ('id', '!=', self.id)
        ])
        if student_subject_check:
            print("Check List Duplicate")
            raise ValueError(('Exists ! Already existed this code in this name'))

    @api.onchange('major_id')
    def check_change_major(self):
        if self.major_id:
            print('CHECK CHANGING AT SUBJECT')
            print(type(self.major_id))
            self.subject_code = str(self.major_id.major_code) + self.subject_code


