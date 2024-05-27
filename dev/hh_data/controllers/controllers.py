from odoo import http
from odoo.http import content_disposition, request
import csv
import io
from werkzeug.exceptions import InternalServerError
import logging
import json
from .csv_generator import CsvStringGenerator
from odoo.tools import lazy_property, osutil, pycompat


_logger = logging.getLogger(__name__)


class DemoDataExport(http.Controller):
    @http.route('/web/demo_data/export/csv', type='http', auth="user")
    def index(self, model, id):
        try:
            # Fetch the record from the model
            record = request.env[model].browse(int(id))
            if not record.exists():
                return request.not_found()

            # Fetch the data fields to be exported
            fields_to_export = record.data_field_ids

            # Generate header row
            headers = [field.name for field in fields_to_export]

            configs = record.get_fields_config()

            csv_generator = CsvStringGenerator(configs)

            num_rows = record.number_of_rows

            csv_content = csv_generator._generate_data(num_rows)

            response_data = self.from_data(headers, csv_content)

            return request.make_response(
                response_data,
                headers=[
                    (
                        'Content-Disposition',
                        content_disposition(
                            osutil.clean_filename(
                                f"{record.model_id.model}.csv")
                        ),
                    ),
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ],
            )
        except Exception as exc:
            _logger.exception("Exception during request handling.")
            payload = json.dumps({
                'code': 200,
                'message': "Odoo Server Error",
                'data': http.serialize_exception(exc)
            })
            raise InternalServerError(payload) from exc

    def from_data(self, fields, rows):
        fp = io.BytesIO()
        writer = pycompat.csv_writer(fp, quoting=1)

        writer.writerow(fields)

        for data in rows:
            row = []
            for d in data:
                # Spreadsheet apps tend to detect formulas on leading =, + and -
                if isinstance(d, str) and d.startswith(('=', '-', '+')):
                    d = f"'{d}"

                row.append(pycompat.to_text(d))
            writer.writerow(row)

        return fp.getvalue()
