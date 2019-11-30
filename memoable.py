import copy

class Memoable:
    """
    Memoable objects have a simple type/update structure.  They accept memos (dictionaries) with type
    restrictions to create/update themselves, and can produce a memo of themselves.  Memoable objects
    are connected to a database table.  The TYPES dictionary defines allowed names, and a mapper for
    type safety as python / database components.

    Ex: A person is an object with an id (int) and name (string).  The database version ('db') does
    not allow null types, but the python version does.

        import memoable,table
        class Person(memoable.Memoable):
            NAME="person" # the table name
            TYPES={
                'id' : {
                    'dbType' : 'integer primary key',
                    'db'  : lambda value : int(value),
                    'py'  : lambda value : int(value) if value != None else None,
                    'default': None
                },
                'name' : {
                    'dbType' : 'text not null',
                    'db'  : lambda value : str(value),
                    'py'  : lambda value : str(value) if value != None else None,
                    'default': None
                }
            }
            def __init__(self,memo={}):
                super().__init__(Bad.TYPES,memo)

        def ex():
            alice=Person({'name': 'alice'}) # id is None as per TYPES['id']['default']
            alice.defaults = ({ 'id' : None, 'name': None }) # deep copy of default values

            android=Person({'id': 32, 'name': 32})  # name becomes '32' as per TYPES['name']['py']
            android.id = 43
            print(repr(android.memo))  # {'id': 43, 'name': '32' }
            alice.update({'id': "300.4", 'dress': 'blue'}) # id becomes 300, 'dress' is ignored.
            alice.defaults = ({ 'id' : None, 'name': None }) # al

    """
    def __init__(self,types,memo={}):
        self.__dict__['_types'] = types
        self.__dict__['_memo'] = self.defaults
        self.update(memo)

    @property
    def defaults(self):
        """ produce a dictionary of default values as a deep copy of 'default' value in TYPES """
        values = {}
        types=self.__dict__['_types']
        for name in types:
            values[name]=copy.deepcopy(types[name]['default'])
        return values

    @property
    def memo(self):
        """ copy the current state of this object """
        return self.__dict__['_memo'].copy()

    def update(self,memo):
        """ update the current state using the provided memo.  These values are mapped through
        the 'py' function of the corresponding fields defined in TYPES """
        _types=self.__dict__['_types']
        _memo=self.__dict__['_memo']
        for name in _types:
            if name in memo:
                _memo[name]=_types[name]['py'](memo[name])
                
    def __repr__(self):
        return repr(self._memo)

    def __getattr__(self, name):
        _memo=self.__dict__['_memo']
        return _memo[name]

    def __setattr__(self,name,value):
        _memo=self.__dict__['_memo']        
        _types=self.__dict__['_types']        
        _memo[name]=_types[name]['py'](value)
