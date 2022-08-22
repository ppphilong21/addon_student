import base64
from odoo.addons.web.controllers.main import serialize_exception, content_disposition
from odoo import http
from odoo.http import request
import logging
import json

_logger = logging.getLogger(__name__)


class Binary(http.Controller):
    @http.route('/web/binary/download_document', type='http', auth="public")
    @serialize_exception
    def download_document(self, model, field, id, filename=None, **kw):
        Model = request.env[model]
        res = Model.browse([int(id)])
        filecontent = base64.b64decode(res.datas)
        if not filecontent:
            res.unlink()
            return request.not_found()
        else:
            res.unlink()
            return request.make_response(filecontent,
                                         [('Content-Type', 'application/octet-stream'),
                                          ('Content-Disposition', content_disposition(filename))])
