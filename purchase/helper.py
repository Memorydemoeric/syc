class OrderDetail(object):

    def __init__(self, pro_id, pro_count, storage_detail, half_storage_detail):
        self.pro_id = pro_id
        self.pro_count = pro_count
        self.storage_count = storage_detail.get(pro_id=self.pro_id).pro_count
        self.half_storage_count = half_storage_detail.get(half_id=self.pro_id).half_count

    @property
    def subtotal_count(self):
        if not hasattr(self, '_subtotal_count'):
            self._subtotal_count = self.storage_count + self.half_storage_count - self.pro_count
        return self._subtotal_count

    @property
    def pro_surplus(self):
        if not hasattr(self, '_pro_surplus'):
            self._pro_surplus = self.storage_count - self.pro_count
        return self._pro_surplus