# -*- coding: utf-8 -*-
from odoo import http

# class StudentAddon(http.Controller):
#     @http.route('/student_addon/student_addon/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/student_addon/student_addon/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('student_addon.listing', {
#             'root': '/student_addon/student_addon',
#             'objects': http.request.env['student_addon.student_addon'].search([]),
#         })

#     @http.route('/student_addon/student_addon/objects/<model("student_addon.student_addon"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('student_addon.object', {
#             'object': obj
#         })