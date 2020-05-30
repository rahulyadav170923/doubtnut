from flask import Flask, make_response, render_template
from flask import request
from schema import RelatedQuestionsSchema
from marshmallow import ValidationError as MarshmallowValidationError
import pdfkit
import json

app = Flask(__name__)


@app.route('/build', methods=['GET'])
def pdf():
    if request.content_type != 'application/json':
        return make_response(
            json.dumps(
                {'message': 'Invalid Content-Type'}
            ), 400,
            {'Content-Type': 'application/json'}
        )

    try:
        input_data_schema = RelatedQuestionsSchema()
        input_data = input_data_schema.load(request.json)
    except MarshmallowValidationError:
        return make_response(
            json.dumps(
                {'message': 'Invalid input data'}
            ), 400,
            {'Content-Type': 'application/json'}
        )
    rendered_template = render_template('related_questions.html', questions=input_data.data['data'])
    pdf = pdfkit.from_string(rendered_template, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application-pdf'
    response.headers['Content-Disposition'] = 'inline; filename=related_questions.pdf'
    return response


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0',port=5000)