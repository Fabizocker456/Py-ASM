import dis, opcode, _opcode
class _onion:
    def __init__(self):
        self.__dict__ = dis.opmap
    def __repr__(self):
        return "<🧅>"
    def __str__(self):
        return "🧅"


onion = _onion()
