import hashlib

class Hash:
    @classmethod    
    def hashString(cls,string):
        if string == None:
            return None
        utf8=bytes(str(string),'utf-8')
        hash=cls.hashBytes(utf8)
        return hash

    @classmethod    
    def hashBytes(cls,data):
        if data == None:
            return None
        encoder = hashlib.sha256()
        encoder.update(data)
        digest = encoder.digest()
        state = (digest[0]<<(0*8))|(digest[1]<<(1*8))|(digest[2]<<(2*8))|(digest[3]<<(3*8))|(digest[4]<<(4*8))|(digest[5]<<(5*8))
#        n = int.from_bytes(digest, byteorder='little', signed=False)
#        state = n & ( (1 << 48) - 1 )
        return state
