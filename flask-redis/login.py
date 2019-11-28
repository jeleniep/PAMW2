import redis
import uuid

class Login:
    def __init__(self):
        self.redis_conn = redis.Redis(host='db', port=6379, db=0)
    
    def generate_uuid(self):
        new_uuid = uuid.uuid4()
        self.redis_conn.hset('sessions', str(new_uuid), 'ELO')
        while self.redis_conn.hget('sessions', str(new_uuid)):
            print("TEEEEEEEEEEEEEEEEEEEEEST", flush=True)
            new_uuid = uuid.uuid4()
        return str(new_uuid)

    def test(self):
        print("test", self.redis_conn.get("lol"), flush=True)
    
