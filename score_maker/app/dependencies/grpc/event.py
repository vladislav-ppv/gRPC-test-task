import grpc
from google.protobuf.json_format import MessageToDict

from score_maker.pb.line_provider_pb2_grpc import EventServiceStub
from score_maker.pb.line_provider_pb2 import GetEventsRequest, GetEventsResponse


async def get_events_grpc():
    async with grpc.aio.insecure_channel('line-provider:50051') as channel:
        stub = EventServiceStub(channel)
        response: GetEventsResponse = await stub.GetEvents(GetEventsRequest())
        return MessageToDict(
            response,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
            use_integers_for_enums=True
        ).get("events")


