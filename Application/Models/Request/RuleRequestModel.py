class RuleRequestModel:
    def __init__(self, rule_id: int, gift_id: int, residue_id: int, conversion_value: int):
        self.rule_id = rule_id
        self.gift_id = gift_id
        self.residue_id = residue_id
        self.conversion_value = conversion_value
