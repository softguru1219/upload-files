from snakebite.client import Client
client = Client('localhost', 9000)
try:
    for x in client.ls(['/input.txt'], recurse=True):
        print x
except Exception as e:
    print(e)