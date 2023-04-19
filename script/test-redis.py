import redis

conn = redis.Redis(host='123.57.138.63', port=6379, password='123Suyufan^')
# conn.set('foo','Bar')
# result = conn.get('foo')
# print(result)
print(conn.keys())