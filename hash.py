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
        i=0
        n=len(data)
        state = 0
        while i+6<=n:
            x=int.from_bytes(data[i:i+6],'little')
            state = cls.advance(state ^ x)
            i = i + 6
        x=int.from_bytes(data[i:n],'little') + (1 << (8*(n-i)))
        state = cls.advance(state ^ x)
        return state
