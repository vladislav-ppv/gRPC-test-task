import grpc
from google.protobuf.json_format import MessageToDict

from score_maker.pb.line_provider_pb2_grpc import EventServiceStub
from score_maker.pb.line_provider_pb2 import GetEventsRequest, GetEventsResponse


async def get_events_grpc():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = EventServiceStub(channel)
        response: GetEventsResponse = await stub.GetEvents(GetEventsRequest())
        return MessageToDict(
            response,
            preserving_proto_field_name=True,
        )
        # return response.events

