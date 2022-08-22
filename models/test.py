import base64
from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

import xlsxwriter
import tempfile

import logging
class StudentStateActiveReport():
    _name = 'student.state.active.report'
    _description = "Student State Active Report"
    name = "Student State Active Report"
    student_ids = fields.Many2many('student.student', string=u'Student Information')
    line_ids = fields.One2many('student.state.active.report.line', 'parent_id', string=u'Chi tiết')
    from_date = fields.Date(string=u'Từ ngày', default=fields.Date.today() - timedelta(days=30), required=True)
    to_date = fields.Date(string=u'Tới ngày', default=fields.Date.today(), required=True)
    def action_print(self):
        for wiz in self:
            print(wiz)

a = StudentStateActiveReport()
a.action_print()
