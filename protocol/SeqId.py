
class SeqId:

    _seqId = -1

    def set(self, seqId: int):
        self._seqId = seqId

    def getId(self):
        self.set(self._seqId + 1)

        if self._seqId == 256:
            self.reset()

        return self._seqId

    def reset(self):
        self.set(0)