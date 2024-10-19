from Services.Services.PersonService import PersonService
from flask import jsonify, request
import traceback
from Services.Services.ConnectionService import ConnectionService
from Services.Services.ValidationService import ValidationService
from Application.Models.Response.ErrorResponseModel import ErrorResponseModel
from Application.Models.Request.PersonRequestModel import PersonRequestModel


class PersonController:
    @staticmethod
    def setup_controller(app):
        @app.route('/Person/Person', methods=['POST'])
        def register_person():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                person_request = request.get_json()
                person_request = PersonRequestModel(person_request)

                validations = ValidationService.validate_register_person(person_request, cursor)
                if validations.is_valid is False:
                    return jsonify(ErrorResponseModel(Errors=validations.errors).dict()), 422

                person_df = PersonService.create_person(person_request, cursor)

                connection.commit()

                return jsonify(person_df.iloc[0].to_dict()), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Person/PersonByCpf/<int:cpf>', methods=['GET'])
        def get_person_by_cpf(cpf):
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                person_df = PersonService.get_person_by_cpf(cpf, cursor)

                if person_df.empty:
                    return jsonify(ErrorResponseModel(
                        Errors=['Participante não encontrado. Realizar cadastro primeiro']).dict()), 422

                return jsonify(person_df.iloc[0].to_dict()), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)
