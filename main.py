from flask import Flask, make_response, render_template
from flask import request
from schema import PDFDataSchema
from marshmallow import ValidationError as MarshmallowValidationError
import pdfkit
import json
import os
from constants import pdf_data_schema_mapping

app = Flask(__name__)

@app.route('/build_pdf', methods=['GET'])
def pdf():
    if request.content_type != 'application/json':
        return make_response(
            json.dumps(
                {'message': 'Invalid Content-Type'}
            ), 400,
            {'Content-Type': 'application/json'}
        )

    try:
        input_body_schema = PDFDataSchema()
        input_body = input_body_schema.load(request.json)
        input_data_schema = pdf_data_schema_mapping[input_body.data['pdf_type']]
        input_data = input_data_schema().load({"data": input_body.data['data']})
    except MarshmallowValidationError:
        return make_response(
            json.dumps(
                {'message': 'Invalid input data'}
            ), 400,
            {'Content-Type': 'application/json'}
        )
    except KeyError:
        return make_response(
            json.dumps(
                {'message': 'Invalid pdf type'}
            ), 400,
            {'Content-Type': 'application/json'}
        )

    rendered_template = render_template('related_questions.html', questions=input_data.data['data'])
    pdf = pdfkit.from_string(rendered_template, False, css='static/styles/related_questions.css')
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application-pdf'
    response.headers['Content-Disposition'] = 'inline; filename=related_questions.pdf'
    return response

if __name__ == "__main__":
    app.run(debug=os.environ.get('DEBUG', False), host='0.0.0.0', port=os.environ.get('PORT', 5000))
