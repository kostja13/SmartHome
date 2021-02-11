from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift import Thrift
from smart_home_thrift import SmartHome

import time


def main():
    print('starting RPC client')
    time.sleep(5)
    # Make socket
    transport = TSocket.TSocket('thriftserver', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = SmartHome.Client(protocol)


    for x in range(1000):
        # Connect!
        transport.open()


        start = int(round(time.time()*1000000))
        client.test("""
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42 
name: windsendsor1, ID:10, value:42
name: windsendsor1, ID:10, value:42 
name: wi, ID:1, value:42
""")
        stop = int(round(time.time()*1000000))
        print(stop-start)
        # Close!
        transport.close()
    time.sleep(3)


if __name__ == '__main__':
    main()