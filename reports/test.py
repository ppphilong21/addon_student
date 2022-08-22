# -*- coding: utf-8 -*-
import base64
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import xlsxwriter
import tempfile

import logging

_logger = logging.getLogger(__name__)

CALL_TEAM = \
    [('front_line', 'Front line'), ('undefined', 'Không xác định'),
     ('back_line', 'Back line'), ('outside_working_hours', 'Ngoài giờ')]


class CallAgentStatusReport(models.TransientModel):
    _name = 'call.agent.status.report'

    name = fields.Char(u'Tên', default=u'R002 Báo cáo chi tiết trạng thái tổng đài viên')
    agent_ids = fields.Many2many('call.agent', string=u'Tổng đài viên')
    from_date = fields.Date(string=u'Từ ngày', default=fields.Date.today() - timedelta(days=30), required=True)
    to_date = fields.Date(string=u'Tới ngày', default=fields.Date.today(), required=True)
    call_team = fields.Selection(CALL_TEAM,
                                 string=u'Nhánh tổng đài')
    team_ids = fields.Many2many('call.team', string=u'Nhánh tổng đài')
    line_ids = fields.One2many('call.agent.status.report.line', 'parent_id', string=u'Chi tiết')

    @api.multi
    def action_print(self):
        for wiz in self:
            if not wiz.line_ids:
                self.action_preview()
            header = [
                u'STT',
                u'Tổng đài viên',
                u'Trạng thái',
                u'Thời lượng trạng thái',
                u'Thời điểm bắt đầu'
            ]
            lines = [header]
            for line in wiz.line_ids:
                start_time = line.start_time + timedelta(hours=7)
                lines.append([
                    line.stt,
                    line.agent_id.name, line.status, line.duration_status if line.duration_status else '', start_time])
            path = tempfile.gettempdir() + '/tempfile.xlsx'
            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet(u'Sheet0')
            worksheet.set_column('A:A', 10)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 20)
            worksheet.set_column('E:E', 20)
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

            worksheet.merge_range('A1:E1', u"Báo cáo chi tiết trạng thái tổng đài viên", header_format)
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
                file_name = wiz.name + '_' + datetime.strftime(datetime.today(), "%d-%m-%Y") + '.xlsx'
                attach = self.env['ir.attachment'].create({
                    'name': file_name,
                    'res_name': file_name,
                    'res_model': 'call.agent.status.report',
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
            wizard.line_ids.unlink() #xóa path

            sql_where_1 = " and  1 = 1 "
            sql_where_2 = " and 1 = 1 "
            if wizard.from_date:
                sql_where_1 += """
                                and ua.time + INTERVAL '7 hours' >='{}' 
                            """.format(wizard.from_date)
                sql_where_2 += """
                                and cs.time + INTERVAL '7 hours' >='{}' 
                            """.format(wizard.from_date)
            if wizard.to_date:
                to_date = wizard.to_date + timedelta(days=1)
                sql_where_1 += """
                                and ua.time < '{}' 
                            """.format(to_date)
                sql_where_2 += """
                                and cs.time < '{}' 
                            """.format(to_date)
            if wizard.agent_ids and len(wizard.agent_ids) > 1:
                sql_where_1 += """
                                and ca.id in {}
                            """.format(tuple(wizard.agent_ids.ids))
                sql_where_2 += """
                                and cs.agent_id in {}
                            """.format(tuple(wizard.agent_ids.ids))
            elif wizard.agent_ids:
                sql_where_1 += """
                                and ca.id in ({})
                                           """.format(wizard.agent_ids.ids[0])
                sql_where_2 += """
                                and cs.agent_id in ({})
                                            """.format(wizard.agent_ids.ids[0])
            if wizard.call_team:
                sql_where_1 += """
                                and ca.call_team = '{}'
                                            """.format(wizard.call_team)
                sql_where_2 += """
                                and ca.call_team = '{}'
                                            """.format(wizard.call_team)

            sql = """
                select 
                  t.agent_id,
                  t.agent_name,
                  t.agent_status,
                  t.duration_status,
                  t.start_time,
                  TO_CHAR((t.duration_status || ' second')::interval, 'HH24:MI:SS') as duration 
                from 
                  (
                    (
                      select 
                        ca.id as agent_id, 
                        ca.name as agent_name, 
                        ua.description as agent_status, 
                        0 as duration_status, 
                        ua.time as start_time 
                      from 
                        user_activity ua, 
                        res_users ru, 
                        call_agent ca 
                      where 
                        ua.user_id = ru.id 
                        and ru.id = ca.user_id
                        {}
                    ) 
                    union all 
                      (
                        select 
                          ca.id as agent_id, 
                          ca.name as agent_name, 
                          case when cs.status = 'available' then 'Sẵn sàng' when cs.status = 'lunch_break' then 'Ăn trưa' when cs.status = 'short_break' then 'Làm việc riêng' when cs.status = 'key_in' then 'Nhập liệu' when cs.status = 'not_available' then 'Không sẵn sàng'  when cs.status = 'call_out' then 'Gọi ra' else 'Không xác định' end as agent_status, 
                          cs.duration_status as duration_status, 
                          cs.time as start_time 
                        from 
                          call_agent_status cs, 
                          call_agent ca 
                        where 
                          cs.agent_id = ca.id
                          {}
                      )
                  ) t 
                order by 
                  t.agent_name asc, #lọc theo thứ tự tăng dần
                  t.start_time desc #lọc theo thứ tự giảm dần 


            """.format(sql_where_1, sql_where_2)
            _logger.info(sql) #
            self.env.cr.execute(sql)
            results = self.env.cr.fetchall() #kiểu fetch api, truyền vào result để render ra :3
            if results and len(results) > 0:
                vals = {}
                count = 1
                #nếu có "kết quả" thì truyền vào "line" để từ line sang res_model
                for line in results:
                    vals.update({
                        'stt': count,
                        'agent_id': line[0],
                        'status': line[2],
                        'duration_status': line[5],
                        'start_time': line[4],
                        'parent_id': wizard.id
                    })
                    self.env['call.agent.status.report.line'].create(vals)
                    count += 1
            else:
                raise UserError(u'Không có kết quả báo cáo với các lựa chọn, vui lòng thử lại với các tham số khác')
            return {
                'name': _(u"R002 Báo cáo chi tiết trạng thái tổng đài viên"),
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'call.agent.status.report',
                'type': 'ir.actions.act_window',
                'res_id': wizard.id,
                'target': 'main',
            }


class CallAgentStatusReportLine(models.TransientModel):
    _name = 'call.agent.status.report.line'

    stt = fields.Integer(string=u'STT')
    agent_id = fields.Many2one('call.agent', string=u'Tổng đài viên')
    status = fields.Char(string=u'Trạng thái')
    duration_status = fields.Char(string=u'Thời lượng trạng thái')
    start_time = fields.Datetime(string=u'Thời điểm bắt đầu')
    parent_id = fields.Many2one('call.agent.status.report', string='Report')
