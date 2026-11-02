from datetime import date


class Business_Relation_Record:
    def __init__(self, id, supplier_id, quantity_deliveries, creation_date=None, update_date=None):
        self.id = id
        self.supplier_id = supplier_id
        self.quantity_deliveries = quantity_deliveries
        self.creation_date = creation_date or date.today()
        self.update_date = update_date or date.today()


    def to_dict(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "quantity_deliveries": self.quantity_deliveries,
            "creation_date": self.creation_date,
            "update_date": self.update_date.isoformat(),
        }