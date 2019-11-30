import hashlib

class Hash:
    """ 48 bit hash based on the Java Random algorithm """

    A = 25214903917
    B = 11

    @classmethod
    def advance(cls,state):
        return (cls.A * state + cls.B) & ((1 << 48) - 1)
        
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
        state = int.from_bytes(digest[0:6],'little')
        return state
