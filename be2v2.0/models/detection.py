class DetectionLog:
    def __init__(self, id: int, model_type: str, result: dict):
        self.id = id
        self.model_type = model_type
        self.result = result
