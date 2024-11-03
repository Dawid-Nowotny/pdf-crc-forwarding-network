class CRC:
    def get_crc_function(self, polynomial: str):
        if len(polynomial) == 8:
            return self._crc8
        elif len(polynomial) == 16:
            return self._crc16
        elif len(polynomial) == 32:
            return self._crc32

    def _crc8(self, polynomial: str, data: bytes) -> int:
        poly = int(polynomial, 2)
        crc = 0x00

        for byte in data:
            crc ^= byte
            for _ in range(8):
                if (crc & 0x80) != 0:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
                crc &= 0xFF
        return crc

    def _crc16(self, polynomial: str, data: bytes) -> int:
        poly = int(polynomial, 2)
        crc = 0xFFFF

        for byte in data:
            crc ^= byte << 8
            for _ in range(8):
                if (crc & 0x8000) != 0:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return crc

    def _crc32(self, polynomial: str, data: bytes) -> int:
        poly = int(polynomial, 2)
        crc = 0xFFFFFFFF

        for byte in data:
            crc ^= byte << 24
            for _ in range(8):
                if (crc & 0x80000000) != 0:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
                crc &= 0xFFFFFFFF
        return crc ^ 0xFFFFFFFF