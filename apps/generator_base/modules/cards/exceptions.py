class GPTWrapResponseFailed(Exception): pass 
class GPTAccessFailed(Exception): pass
class CardGenFailed(Exception): 
    def __init__(self, message, card_id=None):
        super().__init__(message)
        self.card_id = card_id
class ProductsGetFailed(Exception): pass 