from db import Db
class CSV:
    def __init__(self):
        self.db = Db()
        fh = open("same.csv", "w") 

    def generate(self):
        sql = """
            select original.id original.content original.frequency 
            from phrase original
            join translation t1 on original.id = t1.originalId 
            join phrase translated1 on t1.translatedId = translated1.id 
            join translation t2 on t2.originalId = translated1.id
            join phrase translated2 on t2.translatedId = translated2.id
            where original.id = translated2.id order by original.frequency desc
        """
        cursor = self.db.execute(sql)
        for row in cursor:
            (id,content,frequency)=row
            print(f"{id},{content},{frequency}")


def main():
    csv = CSV()
    csv.generate()

if __name__ == '__main__':
    main()
