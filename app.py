#coding: utf-8
import os

import pypandoc
from flask import Flask, jsonify, send_file, request
from io import BytesIO
from docxtpl import DocxTemplate


#############

from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions


app = Flask(__name__)

DEBUG = os.environ.get("DEBUG")


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['BUNDLE_ERRORS'] = os.environ.get("BUNDLE_ERRORS")

db = SQLAlchemy(app)
api_app = Api(app)
api_app.prefix = '/api'

from api.docs.resource import DocsResource

api_app.add_resource(DocsResource, '/docs', '/docs/<int:docs>')


if __name__ == '__main__':
    app.run()




# путь к папке где лежат наши шаблоны
# FORMS_FOLDER = os.path.join(app.root_path, "forms")
# DEBUG = os.environ.get("DEBUG")



# # вовзвращает список шаблонов
# @app.route('/api/form')
# def forms():
#     form_list = []
#     for f in os.listdir(FORMS_FOLDER):
#         if f.endswith('.docx'):
#             form_list.append(dict(
#                 filename = f,
#                 path=FORMS_FOLDER
#             ))

#     return jsonify({
#         'forms': form_list
#     })


# @app.route("/api/form/print/<name>")
# def print_form(name):
#     filename = os.path.join(FORMS_FOLDER, name)

#     # открываем шаблон
#     doc = DocxTemplate(filename)
#     # передаем параметры запроса как значени плейсхолеров для шаблона
#     doc.render(request.args.to_dict())

#     # сохраняем результат заполнения docx в память
#     stream = BytesIO()
#     doc.get_docx().save(stream)
#     stream.seek(0)

#     # возвращаем файл
#     return send_file(stream, mimetype='docx')

# # вовзвращает содержимое шаблона в html формате
# @app.route("/api/form/<name>")
# def form(name):
#     # вообще так делать не рекомендуется,
#     # будет лучше если доступ к шаблонам будет осуществлятся по идентификатору
#     # но для примера пойдет
#     filename = os.path.join(FORMS_FOLDER, name)

#     # сконвертируем файл с помощью pandoc
#     output = pypandoc.convert_file(filename, "html")

#     return jsonify({
#         "html": output
#     })


# if __name__ == '__main__':
#     # я поставил тут debug чтобы приложение
#     # автоматически перезапускалось при изменениях кода
#     app.run(host="0.0.0.0",port=5000,debug=DEBUG)