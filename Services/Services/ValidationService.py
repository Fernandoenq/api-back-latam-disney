from datetime import datetime
from Services.Models.Results.ValidationResult import ValidationResult
from Application.Models.Request.PersonRequestModel import PersonRequestModel
from Application.Models.Request.OrganizerLoginRequestModel import OrganizerLoginRequestModel
from Services.Services.PersonService import PersonService
from Services.Services.OrganizerService import OrganizerService
from Services.Services.SchedulingService import SchedulingService
from Application.Models.Request.SchedulingRequestModel import SchedulingRequestModel
from Application.Models.Request.ReschedulingRequestModel import ReschedulingRequestModel
from Domain.Entities.Scheduling import Scheduling
from Domain.Enums.SchedulingStatus import SchedulingStatus


class ValidationService:
    @staticmethod
    def validate_register_person(person_request: PersonRequestModel, cursor) -> ValidationResult:
        result = ValidationResult()

        if person_request is None:
            result.add_error("Dados de requisição não enviados")
            return result

        if (person_request.register_date is None or person_request.person_name is None
                or person_request.cpf is None or person_request.phone is None or person_request.birth_date is None
                or person_request.mail is None or person_request.has_accepted_promotion is None
                or person_request.has_accepted_participation is None or person_request.country_name is None):
            result.add_error("Dados de requisição não enviados")
            return result

        if not person_request.has_accepted_participation:
            result.add_error("É necessário o compartilhamento dos dados para poder jogar")
            return result

        person_df = PersonService().get_person_by_cpf(person_request.cpf, cursor)
        if person_df.empty is False:
            result.add_error("Participante já consta no sistema. Não é necessário este cadastro")
            return result

        cpf_validation = ValidationService.validate_cpf(person_request.cpf)
        if cpf_validation.is_valid is False:
            result.add_errors(cpf_validation.errors)
            return result

        """
        if person_request.birth_date is not None:
            underage_validation = ValidationService.underage_verifier(person_request.birth_date)
            if underage_validation.is_valid is False:
                result.add_errors(underage_validation.errors)
                return result
        """

        return result

    @staticmethod
    def validate_cpf(request_cpf: str) -> ValidationResult:
        result = ValidationResult()

        cpf = request_cpf

        if cpf == '24624624624':
            return result

        if len(cpf) != 11:
            result.add_error(f"CPF inválido! Este CPF possui {len(cpf)} dígitos")
            return result

        if cpf == cpf[0] * 11 or cpf == '0' * 11:
            result.add_error("CPF inválido!")
            return result

        sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
        first_digit = (sum_digits * 10 % 11) % 10

        sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
        second_digit = (sum_digits * 10 % 11) % 10

        if cpf[-2:] != f"{first_digit}{second_digit}":
            result.add_error("CPF inválido!")

        return result

    @staticmethod
    def underage_verifier(award_date: str) -> ValidationResult:
        today = datetime.today().date()
        award_date_converted = datetime.strptime(award_date.split()[0], "%Y-%m-%d").date()
        age = today.year - award_date_converted.year

        if (today.month, today.day) < (award_date_converted.month, award_date_converted.day):
            age -= 1

        result = ValidationResult()
        if age < 18:
            result.add_error("De acordo com o regulamento da promoção, não é permitida a participação de menores.")
            return result

        return result

    @staticmethod
    def validate_login(login_request: OrganizerLoginRequestModel, cursor) -> ValidationResult:
        result = ValidationResult()

        organizer_df = OrganizerService().get_organizer_by_login(login_request.login, cursor)
        if organizer_df.empty:
            result.add_error("Dados incorretos")
            return result

        return result

    @staticmethod
    def validate_scheduling(cursor, scheduling_request: SchedulingRequestModel) -> ValidationResult:
        result = ValidationResult()

        scheduling_df = SchedulingService.get_schedules_by_id(cursor, scheduling_request.scheduling_id)
        scheduling = Scheduling()

        if int(scheduling_df[scheduling.scheduling_status][0]) != SchedulingStatus.available.value:
            result.add_error("Poltrona indisponível")
            return result

        scheduling_df = SchedulingService.get_turns_by_schedule_id(cursor, scheduling_request.scheduling_id)
        if scheduling_request.person_id in scheduling_df[scheduling.person_id].values:
            result.add_error("Este participante já possui uma reserva de poltrona neste horário")
            return result

        return result

    @staticmethod
    def validate_rescheduling(cursor, rescheduling_request: ReschedulingRequestModel) -> ValidationResult:
        result = ValidationResult()
        scheduling = Scheduling()

        scheduling_df = SchedulingService.get_schedules_by_id(cursor, rescheduling_request.old_scheduling_id)
        if int(scheduling_df[scheduling.scheduling_status][0]) == SchedulingStatus.confirmed.value:
            result.add_error("Este agendamento já foi confirmado. Não é possível reagendar")
            return result

        scheduling_df = SchedulingService.get_schedules_by_id(cursor, rescheduling_request.new_scheduling_id)
        if int(scheduling_df[scheduling.scheduling_status][0]) != SchedulingStatus.available.value:
            result.add_error("Poltrona indisponível")
            return result

        scheduling_df = SchedulingService.get_turns_by_schedule_id(cursor, rescheduling_request.new_scheduling_id)
        if rescheduling_request.person_id in scheduling_df[scheduling.person_id].values:
            result.add_error("Este participante já possui uma reserva de poltrona neste horário")
            return result

        return result

    @staticmethod
    def validate_confirmation(cursor, scheduling_id: int) -> ValidationResult:
        result = ValidationResult()
        scheduling_df = SchedulingService.get_schedules_by_id(cursor, scheduling_id)
        scheduling = Scheduling()

        if int(scheduling_df[scheduling.scheduling_status][0]) != SchedulingStatus.busy.value:
            result.add_error("Só é possível confirmar a presença em poltronas que estão ocupadas")
            return result

        return result
