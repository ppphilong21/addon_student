import base64
from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

import xlsxwriter
import tempfile

import logging

#create a logger object as the name of the logger itself would tell us from where the events are being logged
#__name__ a special built-in variable in Python which evaluates to the name of the current module
_logger = logging.getLogger(__name__)


class StudentStateActiveReport(models.TransientModel):
    _name = 'student.state.active.report'
    _description = "Student State Active Report"
    name = fields.Char(u'Tên', defualt=u'Báo cáo trạng thái kích hoạt của sinh viên')
    student_ids = fields.Many2many('student.student', string=u'Student Information')
    line_ids = fields.One2many('student.state.active.report.line', 'parent_id', string=u'Chi tiết')
    from_date = fields.Date(string=u'Từ ngày', default=fields.Date.today() - timedelta(days=30), required=True)
    to_date = fields.Date(string=u'Tới ngày', default=fields.Date.today(), required=True)

    @api.multi
    def action_print(self):
        for wiz in self:
            if not wiz.line_ids:
                self.action_preview()
            header = [
                u'STT',
                u'Sinh viên',
                u'Trạng thái'
            ]
            lines = [header] #tạo header
            for line in wiz.line_ids:
                #thêm thông tin vào header
                lines.append([
                    line.stt,
                    line.student_id.name,
                    line.state
                ])
                #tempfile: tạo 1 file tạm thời, .getterpdir:trả về thư muc chưa các file tạm thời
            path = tempfile.gettempdir() + '/tempfile.xlsx'
            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet(u'Sheet0')
            worksheet.set_column('A:A', 10)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 30)
            header_format = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '11',
                'text_wrap': True,
                'italic': False,
                'bold': True,
                'border': 1,
            })
            header_format.set_font_name('Times New Roman')

            bold_no_border = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '11',
                'text_wrap': True,
                'italic': False,
                'bold': True,
            })
            bold_no_border.set_font_name('Times New Roman')

            left_center_wrap = workbook.add_format({
                'align': 'left',
                'valign': 'vcenter',
                'font_size': '11',
                'text_wrap': True,
            })
            left_center_wrap.set_font_name('Times New Roman')

            center_bold_18 = workbook.add_format({
                'font_size': '18',
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
            })
            center_bold_18.set_font_name('Times New Roman')

            center_8 = workbook.add_format({
                'font_size': '11',
                'bold': False,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            })
            center_8.set_font_name('Times New Roman')

            left_8 = workbook.add_format({
                'align': 'left',
                'font_size': '11',
                'valign': 'vcenter',
                'text_wrap': True,
                'border': 1,
            })
            left_8.set_font_name('Times New Roman')

            left_8_no = workbook.add_format({
                'align': 'left',
                'font_size': '11',
            })
            left_8_no.set_font_name('Times New Roman')
            left_8_no.set_num_format('#,##0')

            left_bold_8_no = workbook.add_format({
                'align': 'center',
                'font_size': '11',
                'bold': True,
                'border': 1,
            })
            left_bold_8_no.set_font_name('Times New Roman')
            left_bold_8_no.set_num_format('#,##0')

            center_italic_wrap = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '9',
                'text_wrap': True,
                'italic': True
            })
            center_italic_wrap.set_font_name('Times New Roman')

            right_8_no = workbook.add_format({
                'align': 'right',
                'font_size': '11',
                'border': 1,
            })
            right_8_no.set_font_name('Times New Roman')
            right_8_no.set_num_format('#,##0')

            date_format = workbook.add_format({
                'num_format': 'dd-mm-yyyy hh:mm:ss',
                'font_size': '11',
                'align': 'center',
                'border': 1
            })

            date_format.set_font_name('Times New Roman')

            worksheet.merge_range('A1:C1', u"Báo cáo chi tiết trạng thái sinh viên", header_format)
            row = 2
            for line in lines:
                col = 0
                for item in line:
                    if row == 2:
                        worksheet.write(row, col, item, header_format)
                    elif col == 0:
                        worksheet.write(row, col, item, center_8)
                    elif col == 1:
                        worksheet.write(row, col, item, left_8)
                    elif col == 4:
                        worksheet.write(row, col, item, date_format)
                    else:
                        worksheet.write(row, col, item, right_8_no)
                    col += 1
                row += 1
            workbook.close()
            with open(path, 'rb') as fp:
                print("WIZ TEST ................",wiz)
                file_name = wiz.name + '_' + datetime.strftime(datetime.today(), "%d-%m-%Y") + '.xlsx'
                attach = self.env['ir.attachment'].create({
                    'name': file_name,
                    'res_name': file_name,
                    'res_model': 'student.state.active.report',
                    'res_id': wiz.id,
                    'datas': base64.encodestring(fp.read()),
                    'datas_fname': file_name,
                })
                return {
                    'type': 'ir.actions.act_url',
                    'url': '/web/binary/download_document?model=ir.attachment&field=datas&id=%s&filename=%s' % (
                        attach.id, file_name),
                    'target': 'current',
                }

    @api.multi
    def action_preview(self):
        for wizard in self:
            #xoa path
            wizard.line_ids.unlink()
            #khởi tạo để dùng kiểm tra 2 or nhiều điều kiện khác trong các lệnh truy vấn
            sql_where_1 = "and 1 = 1"
            sql_where_2 = "and 1 = 1"
            if wizard.student_ids and len(wizard.student_ids) > 1:
                sql_where_1 += """and ss.id in {}""".format(tuple(wizard.student_ids.ids))
                sql_where_2 += """and sa.student_id in {}""".format(tuple(wizard.student_ids.ids))
                print("..............TESTING STUDENT_ID LENGTHING - >1..............")
            elif wizard.student_ids:
                sql_where_1 += """and ss.id in ({})""".format(wizard.student_ids.ids[0])
                sql_where_2 += """and sa.student_id in ({})""".format(wizard.student_ids.ids[0])
                print("..............TESTING STUDENT_ID LENGTHING - >1..............")
            sql = """
            select
                t.student_id,
                t.student_name,
                t.student_state
            from 
            (
                (
                    select 
                        ss.id as student_id,
                        ss.name as student_name,
                        case when sa.state = 'active' then 'Kích hoạt'  when sa.state = 'inactive' then 'Chưa kích hoạt' else 'Không xác định' end as student_state 
                    from 
                        student_student ss,
                        student_state_active sa
                    where 
                         sa.student_id = ss.id  
                         {}
                )
            ) t
            order by 
                t.student_name asc
            """.format(sql_where_1, sql_where_2)
            _logger.info(sql)
            print(_logger.info(sql))
            self.env.cr.execute(sql)
            results = self.env.cr.fetchall()
            print("CHEKCING RESULTS", results)
            if results and len(results) > 0:
                vals = {}
                count = 1
                for line in results:
                    vals.update({
                        'stt': count,
                        'student_id': line[0],
                        'state': line[2],
                        'parent_id': wizard.id
                    })
                    self.env['student.state.active.report.line'].create(vals)
                    count += 1
            else:
                raise UserError(u'Không tìm thấy')
            return {
                'name': (u'Báo cáo chi tiết'),
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'student.state.active.report',
                'type': 'ir.actions.act_window',
                'res_id': wizard.id,
                'target': 'main',
            }

class StudentStateActiveReportLine(models.TransientModel):
    _name = 'student.state.active.report.line'
    stt = fields.Integer(string=u'STT')
    student_id = fields.Many2one('student.student', string=u'Student Information')
    state = fields.Char(string=u'Trạng thái')
    duration_status = fields.Char(string=u'Thời lượng trạng thái')
    start_time = fields.Datetime(string=u'Thời điểm bắt đầu')
    parent_id = fields.Many2one('student.state.active.report', string='Report')