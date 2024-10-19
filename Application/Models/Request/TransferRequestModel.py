from Domain.Entities.Scheduling import Scheduling


class TransferRequestModel:
    def __init__(self, transfer_request):
        transfer = Scheduling()

        self.sender_collect_point_id = transfer_request[transfer.sender_collect_point_id]
        self.recipient_collect_point_id = transfer_request[transfer.recipient_collect_point_id]
        self.sender_event_day = transfer_request[transfer.sender_event_day]
        self.recipient_event_day = transfer_request[transfer.recipient_event_day]
        self.gift_id = transfer_request[transfer.gift_id]
        self.transferred = transfer_request[transfer.transferred]
        self.transferred_date = transfer_request[transfer.transferred_date]
        self.organizer_id = transfer_request[transfer.organizer_id]
