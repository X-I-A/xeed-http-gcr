import os
import json
import base64
import gzip
import pytest
from google.cloud import pubsub_v1
from xialib_gcp import PubsubSubscriber
from main import app

credentials = base64.b64encode(b"user:La_vie_est_belle").decode()
headers = {"Content-Type": "text/plain",
           "Authorization": "Basic {}".format(credentials),
           "xeed-aged": "True",
           "xeed-age": "2",
           "xeed-start-seq": "20201125000000000000",
           "xeed-topic-id": "xialib-topic-01",
           "xeed-table-id": "gcr-test",
           "xeed-data-spec": "slt",
           "xeed-data-encode": "flat",
           "xeed-data-store": "body",
           "xeed-data-format": "record"}
data_body = json.dumps([{"_RECNO": 1, "name": "Hello"},
                        {"_RECNO": 2, "name": "World"}],
                       ensure_ascii=False)

@pytest.fixture(scope="module")
def client():
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()

def test_homepage(client):
    reponse = client.get('/')
    assert reponse.status_code == 200
    assert b'Xeed' in reponse.data

def test_check_destination(client):
    reponse = client.get('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01')
    assert reponse.status_code == 401

    reponse = client.get('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-404',
                         headers=headers)
    assert reponse.status_code == 400
    assert b'not found' in reponse.data

    reponse = client.get('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01',
                         headers=headers)
    assert reponse.status_code == 200
    assert b'You can post to destination' in reponse.data

def test_push_flat_data(client):
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01',
                          headers=headers, data=data_body)
    assert reponse.status_code == 200
    assert b'Data has been pushed' in reponse.data

def test_push_blob_data(client):
    blob_headers = headers.copy()
    blob_headers['xeed-data-encode'] = 'blob'
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01',
                          headers=blob_headers, data=data_body.encode())
    assert reponse.status_code == 200
    assert b'Data has been pushed' in reponse.data

def test_push_http_gzipped_flat_data(client):
    gz_headers = headers.copy()
    gz_headers['Content-Encoding'] = 'gzip'
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01',
                          headers=gz_headers, data=gzip.compress(data_body.encode()))
    assert reponse.status_code == 200
    assert b'Data has been pushed' in reponse.data

def test_push_http_gzipped_gzip_data(client):
    gz_headers = headers.copy()
    gz_headers['Content-Encoding'] = 'gzip'
    gz_headers['xeed-data-encode'] = 'gzip'
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01',
                          headers=gz_headers, data=gzip.compress(gzip.compress(data_body.encode())))
    assert reponse.status_code == 200
    assert b'Data has been pushed' in reponse.data

def test_push_flat_file_data(client):
    local_file = os.path.join('.', 'test01.json')
    file_header = headers.copy()
    file_header['xeed-data-store'] = 'file'
    with open(local_file, 'w') as fp:
        fp.write(data_body)
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01',
                          headers=file_header, data=local_file)
    assert reponse.status_code == 200
    assert b'Data has been pushed' in reponse.data

def test_push_b64g_file_data(client):
    local_file = os.path.join('.', 'test01.gz')
    file_header = headers.copy()
    file_header['xeed-data-store'] = 'file'
    file_header['xeed-data-encode'] = 'b64g'
    with open(local_file, 'w') as fp:
        fp.write(base64.b64encode(gzip.compress(data_body.encode())).decode())
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01',
                          headers=file_header, data=local_file)
    assert reponse.status_code == 200
    assert b'Data has been pushed' in reponse.data

def test_push_blob_file_data(client):
    local_file = os.path.join('.', 'test02.json')
    file_header = headers.copy()
    file_header['xeed-data-store'] = 'file'
    file_header['xeed-data-encode'] = 'blob'
    with open(local_file, 'w') as fp:
        fp.write(data_body)
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01',
                          headers=file_header, data=local_file)
    assert reponse.status_code == 200
    assert b'Data has been pushed' in reponse.data

def test_exceptions(client):
    reponse = client.post('/publishers/err/destinations/x-i-a-test/topics/xialib-topic-01',
                          headers=headers, data=data_body)
    assert reponse.status_code == 400
    assert b'Publisher' in reponse.data

    err_header1 = headers.copy()
    err_header1['Content-Encoding'] = 'err'
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test/topics/xialib-topic-01',
                          headers=err_header1, data=data_body)
    assert reponse.status_code == 400
    assert b'Content must be flat or gzip-encoded' in reponse.data

    err_header2 = headers.copy()
    err_header2.pop("xeed-topic-id", None)
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test',
                          headers=err_header2, data=data_body)
    assert reponse.status_code == 400
    assert b'No topic_id' in reponse.data

    err_header3 = headers.copy()
    err_header3.pop("xeed-data-encode", None)
    reponse = client.post('/publishers/pubsub/destinations/x-i-a-test',
                          headers=err_header3, data=data_body)
    assert reponse.status_code == 400
    assert b'Xeed Header check error' in reponse.data

def test_check_messages():
    sub = PubsubSubscriber(sub_client=pubsub_v1.SubscriberClient())
    for message in sub.pull('x-i-a-test', 'xialib-sub-01'):
        header, data, id = sub.unpack_message(message)
        assert len(json.loads(gzip.decompress(data).decode())) == 2
        sub.ack('x-i-a-test', 'xialib-sub-01', id)