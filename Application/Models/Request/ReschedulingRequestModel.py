class ReschedulingRequestModel:
    def __init__(self, scheduling_request):
        self.old_scheduling_id = scheduling_request['OldSchedulingId']
        self.new_scheduling_id = scheduling_request['NewSchedulingId']
        self.person_id = scheduling_request['PersonId']
