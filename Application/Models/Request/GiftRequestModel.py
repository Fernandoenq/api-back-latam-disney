class GiftRequestModel:
    def __init__(self, gift_id: int, gift_name: str, starting_inventory: int, origin: int):
        self.gift_id = gift_id
        self.gift_name = gift_name
        self.starting_inventory = starting_inventory
        self.origin = origin
