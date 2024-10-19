from Domain.Entities.Scheduling import Scheduling


class SchedulingRequestModel:
    def __init__(self, scheduling_request):
        scheduling = Scheduling()
        self.person_id = scheduling_request[scheduling.person_id]
        self.organizer_id = scheduling_request[scheduling.organizer_id]
        self.scheduling_id = scheduling_request[scheduling.scheduling_id]
