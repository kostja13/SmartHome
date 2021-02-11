from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from smart_home_thrift import SmartHome

supportedVersions = [
    '1.0',
    '1.1',
    '1.2',
    '2.0'
]

class SmartHomeHandler:
    def __init__(self):
        self.log = {}

    def test(self, teststring):
        return len(teststring)

    def checkVersion(self, version):
        if version in supportedVersions:
            return True
        else:
            return False
    def safeDailyValues(self, id, values):
        print(id + ' : ' + str(values))
        return True

if __name__ == '__main__':
    print('starting RPC server')
    handler = SmartHomeHandler()
    processor = SmartHome.Processor(handler)
    transport = TSocket.TServerSocket(host='0.0.0.0', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    server.serve()