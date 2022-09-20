import random
from flask import Flask, request, render_template  

import grpc
import redis

import proto_message_pb2 as pb2_grpc
import proto_message_pb2_grpc as pb2
import time

app = Flask(__name__)

r = redis.Redis(host="redis1", port=6379, db=0)
r.config_set('maxmemory-policy', 'allkeys-lfu')
r.flushall()

r1 = redis.Redis(host="redis2", port=6379, db=0)
r1.config_set('maxmemory-policy', 'allkeys-lfu')
r1.flushall()

r2 = redis.Redis(host="redis3", port=6379, db=0)
r2.config_set('maxmemory-policy', 'allkeys-lfu')
r2.flushall()


class SearchClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'servidor'
        self.server_port = '50051'
        
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))

        self.stub = pb2.SearchStub(self.channel)

    def get_url(self, message):
        """
        Client function to call the rpc for GetServerResponse
        """
        message = pb2_grpc.Message(message=message)
        print(f'{message}')
        stub = self.stub.GetServerResponse(message)
        return stub


@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/search', methods = ['GET'])
def search():
    client = SearchClient()
    search = request.args['search']
    cache = r.get(search)
    cache1 = r1.get(search)
    cache2 = r2.get(search)
    
    if cache == None and cache1 is None and cache2 is None:
        item = client.get_url(message=search)
        
        shard = random.choice([r, r1, r2])
        shard.set(search, str(item))
        
        return render_template('index.html', datos = item, procedencia = "Datos sacados de PostgreSQL")
    
    elif cache:
        print(cache)
        item = cache.decode("utf-8")
        print(item)
        dicc = dict()
        dicc['Resultado'] = item
        print(cache)
        print(dicc)
        return render_template('index.html', datos = item, procedencia = "Datos sacados de Redis shard 1")
    
    elif cache1:
        print(cache1)
        item = cache1.decode("utf-8")
        print(item)
        dicc = dict()
        dicc['Resultado'] = item
        print(cache1)
        print(dicc)
        return render_template('index.html', datos = item, procedencia = "Datos sacados de Redis shard 2")

    else:
        print(cache2)
        item = cache2.decode("utf-8") if cache2 else None
        print(item)
        dicc = dict()
        dicc['Resultado'] = item
        print(cache2)
        print(dicc)
        return render_template('index.html', datos = item, procedencia = "Datos sacados de Redis shard 3")

if __name__ == '__main__':
    time.sleep(25)