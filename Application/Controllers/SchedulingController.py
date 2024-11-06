from flask import jsonify, request
from datetime import datetime
import traceback
import pandas as pd
from Services.Services.ConnectionService import ConnectionService
from Services.Services.ValidationService import ValidationService
from Application.Models.Request.SchedulingRequestModel import SchedulingRequestModel
from Application.Models.Request.ReschedulingRequestModel import ReschedulingRequestModel
from Services.Services.SchedulingService import SchedulingService
from Application.Models.Response.ErrorResponseModel import ErrorResponseModel
from Services.Services.SqsService import SqsService
from Domain.Entities.Scheduling import Scheduling


class SchedulingController:
    @staticmethod
    def setup_controller(app):
        @app.route('/Scheduling/SchedulingsByCpf/<int:cpf>', methods=['GET'])
        def get_schedulings_by_cpf(cpf):
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                schedule_df = SchedulingService().get_schedules_by_cpf(cursor, cpf)

                return jsonify(schedule_df.to_dict(orient='records')), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Scheduling/NotViewedSchedules', methods=['GET'])
        def get_not_viewed_schedules():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                schedule_df = SchedulingService().get_schedules(cursor)

                return jsonify(schedule_df.to_dict(orient='records')), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Scheduling/Dashboard/<int:day>', methods=['GET'])
        def get_dashboard(day):
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                schedule_df = SchedulingService().get_all_schedules(cursor, day)

                return jsonify(schedule_df.to_dict(orient='records')), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Scheduling/Scheduling', methods=['PUT'])
        def to_schedule():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                scheduling_request = request.get_json()
                scheduling_request = SchedulingRequestModel(scheduling_request)

                validations = ValidationService.validate_scheduling(cursor, scheduling_request)
                if validations.is_valid is False:
                    return jsonify(ErrorResponseModel(Errors=validations.errors).dict()), 422

                is_scheduled = SchedulingService().to_schedule(cursor, scheduling_request.person_id,
                                                               scheduling_request.organizer_id,
                                                               scheduling_request.scheduling_id)
                if is_scheduled is False:
                    return jsonify(
                        ErrorResponseModel(Errors=['Não foi possível realizar este agendamento']).dict()), 422

                connection.commit()

                person_to_confirm_df = SchedulingService.get_person_to_confirm(cursor, scheduling_request.scheduling_id)
                scheduling = Scheduling()
                name = str(person_to_confirm_df[scheduling.person.person_name][0])
                phone = str(person_to_confirm_df[scheduling.person.phone][0])
                turn_time = pd.to_datetime(person_to_confirm_df[scheduling.turn.turn_time][0])
                message_sqs = {
                    "origin": 1,
                    "phone": phone,
                    "message": (f"Seu embarque com a LATAM está confirmado! "
                                f"Prepare-se para explorar os Destinos Encantados às {turn_time.strftime('%H:%M')}")
                }

                is_notified = SqsService().notify(message_sqs, name, phone)
                if is_notified is False:
                    return jsonify(
                        ErrorResponseModel(Errors=['Agendamento realizado com sucesso. Porém, não foi enviar a confirmação do agendamento para o cliente']).dict()), 422

                return jsonify(), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Scheduling/Rescheduling', methods=['PUT'])
        def to_reschedule():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                rescheduling_request = request.get_json()
                rescheduling_request = ReschedulingRequestModel(rescheduling_request)

                validations = ValidationService.validate_rescheduling(cursor, rescheduling_request)
                if validations.is_valid is False:
                    return jsonify(ErrorResponseModel(Errors=validations.errors).dict()), 422

                is_rescheduled = SchedulingService().to_reschedule(cursor, rescheduling_request)
                if is_rescheduled is False:
                    return jsonify(
                        ErrorResponseModel(Errors=['Não foi possível realizar este reagendamento']).dict()), 422

                connection.commit()
                return jsonify(), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Scheduling/ConfirmPresence/<int:scheduling_id>', methods=['PUT'])
        def confirm_presence(scheduling_id):
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                validations = ValidationService.validate_confirmation(cursor, scheduling_id)
                if validations.is_valid is False:
                    return jsonify(ErrorResponseModel(Errors=validations.errors).dict()), 422

                is_confirmed = SchedulingService().confirm_presence(cursor, scheduling_id)
                if is_confirmed is False:
                    return jsonify(
                        ErrorResponseModel(Errors=['Não foi possível realizar esta confirmação']).dict()), 422

                connection.commit()
                return jsonify(), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Scheduling/CancelSchedule/<int:scheduling_id>', methods=['PUT'])
        def cancel_schedule(scheduling_id):
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                is_canceled = SchedulingService().cancel_schedule(cursor, scheduling_id)
                if is_canceled is False:
                    return jsonify(
                        ErrorResponseModel(Errors=['Não foi possível cancelar este agendamento']).dict()), 422

                connection.commit()
                return jsonify(), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)

        @app.route('/Scheduling/InsertSchedules', methods=['POST'])
        def insert_schedules():
            connection = ConnectionService.open_connection()
            cursor = connection.cursor()
            connection.start_transaction()

            try:
                schedules = request.get_json()
                schedules = schedules.get('Schedules', [])
                schedules = [datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S') for date_str in schedules]

                is_inserted = SchedulingService().insert_schedules(cursor, schedules)
                if is_inserted is False:
                    return jsonify(
                        ErrorResponseModel(Errors=['Não foi possível inserir os horários de agendamentos']).dict()), 422

                connection.commit()
                return jsonify(), 200

            except Exception as e:
                if connection.is_connected():
                    connection.rollback()
                error_response = ErrorResponseModel(Errors=[f"{str(e)} | {traceback.format_exc()}"])
                return jsonify(error_response.dict()), 500
            finally:
                if connection.is_connected():
                    ConnectionService.close_connection(cursor, connection)
