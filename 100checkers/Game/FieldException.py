class FieldCizeErr(Exception):
    def __init__(self, text):
        FieldCizeErr.text = text
