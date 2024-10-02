import logging
from concurrent import futures

import grpc

from line_provider.app.services.event import BaseEventServicer
from line_provider.pb.line_provider_pb2_grpc import add_EventServiceServicer_to_server


class EventServicer(BaseEventServicer):
    pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_EventServiceServicer_to_server(EventServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
