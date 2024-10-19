import logging
from Application.Models.Request.OrganizerRequestModel import OrganizerRequestModel
from Services.Services.OrganizerService import OrganizerService
from Services.Services.ValidationService import ValidationService
from Domain.Entities.Organizer import Organizer
from Services.Services.ConnectionService import ConnectionService
from Application.Models.Response.ErrorResponseModel import ErrorResponseModel
from Application.Models.Response.OrganizerResponseModel import OrganizerResponseModel
from Application.Models.Request.OrganizerLoginRequestModel import OrganizerLoginRequestModel
from flask import jsonify, request


class OrganizerController:
    @staticmethod
    def setup_controller(app):
        @app.route('/Organizer/Organizer', methods=['GET'])
        def get_organizer():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()

            try:
                organizer_df = OrganizerService().get_organizer(cursor)

                organizer_response = organizer_df.to_dict(orient='records')
                organizer_response = OrganizerResponseModel(Organizers=organizer_response)

                return jsonify(organizer_response.dict()), 200

            except Exception as e:
                logging.error(e)
                error_response = ErrorResponseModel(Errors=[str(e)])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Organizer/Organizer', methods=['PUT'])
        def update_organizer():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                organizer = Organizer()
                organizers_request = request.get_json()
                organizers_request_list = organizers_request.get("Organizers", [])
                organizers_request = [OrganizerRequestModel
                                      (organizer_request[organizer.organizer_id],
                                       organizer_request[organizer.organizer_name],
                                       organizer_request[organizer.login],
                                       organizer_request[organizer.secret_key])
                                      for organizer_request in organizers_request_list]

                organizer_df = OrganizerService.update_organizer(organizers_request, cursor)

                organizer_response = organizer_df.to_dict(orient='records')
                organizer_response = OrganizerResponseModel(Organizers=organizer_response)

                connection.commit()
                return jsonify(organizer_response.dict()), 200

            except Exception as e:
                logging.error(e)
                error_response = ErrorResponseModel(Errors=[str(e)])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Organizer/Organizer', methods=['POST'])
        def create_organizer():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                organizer = Organizer()
                organizers_request = request.get_json()
                organizers_request_list = organizers_request.get("Organizers", [])
                organizers_request = [OrganizerRequestModel
                                      (organizer_request[organizer.organizer_id],
                                       organizer_request[organizer.organizer_name],
                                       organizer_request[organizer.login],
                                       organizer_request[organizer.secret_key])
                                      for organizer_request in organizers_request_list]

                organizer_df = OrganizerService.create_organizer(organizers_request, cursor)

                organizer_response = organizer_df.to_dict(orient='records')
                organizer_response = OrganizerResponseModel(Organizers=organizer_response)

                connection.commit()
                return jsonify(organizer_response.dict()), 200

            except Exception as e:
                logging.error(e)
                error_response = ErrorResponseModel(Errors=[str(e)])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Organizer/Organizer', methods=['DELETE'])
        def delete_organizer():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                organizer = Organizer()
                organizers_request = request.get_json()
                organizers_request_list = organizers_request.get("Organizers", [])
                organizers_request = [OrganizerRequestModel
                                      (organizer_request[organizer.organizer_id],
                                       organizer_request[organizer.organizer_name],
                                       organizer_request[organizer.login],
                                       organizer_request[organizer.secret_key])
                                      for organizer_request in organizers_request_list]

                organizer_df = OrganizerService.delete_organizer(organizers_request, cursor)

                organizer_response = organizer_df.to_dict(orient='records')
                organizer_response = OrganizerResponseModel(Organizers=organizer_response)

                connection.commit()
                return jsonify(organizer_response.dict()), 200

            except Exception as e:
                logging.error(e)
                error_response = ErrorResponseModel(Errors=[str(e)])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Organizer/Login', methods=['PUT'])
        def login():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()

            try:
                login_request = request.get_json()
                login_request = OrganizerLoginRequestModel(login_request)

                validations = ValidationService.validate_login(login_request, cursor)
                if validations.is_valid is False:
                    return jsonify(ErrorResponseModel(Errors=validations.errors).dict()), 422

                organizer_df = OrganizerService.login(login_request, cursor)

                if organizer_df.empty:
                    return jsonify(ErrorResponseModel(Errors=["Dados incorretos"]).dict()), 422

                organizer_response = organizer_df.to_dict(orient='records')
                organizer_response = OrganizerResponseModel(Organizers=organizer_response)

                connection.commit()
                return jsonify(organizer_response.dict()), 200

            except Exception as e:
                logging.error(e)
                error_response = ErrorResponseModel(Errors=[str(e)])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        """
        @app.route('/Organizer/Logout', methods=['PUT'])
        def logout():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()

            try:
                login_request = request.get_json()
                service_type = login_request['ServiceType']
                service_id = login_request['ServiceId']

                OrganizerService.logout(service_id, service_type, cursor)

                connection.commit()
                return jsonify(), 200

            except Exception as e:
                logging.error(e)
                error_response = ErrorResponseModel(Errors=[str(e)])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)
        """
