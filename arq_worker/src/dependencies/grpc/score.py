import grpc
from google.protobuf.json_format import MessageToDict

from arq_worker.pb.line_provider_pb2 import UpdateEventStatusByScoreRequest, UpdateEventStatusByScoreResponse
from arq_worker.pb.line_provider_pb2_grpc import EventServiceStub


async def process_score_grpc(event_id: int, rate: int) -> bool:
    async with grpc.aio.insecure_channel('line-provider:50051') as channel:
        stub = EventServiceStub(channel)
        response: UpdateEventStatusByScoreResponse = await stub.UpdateEventStatusByScore(
            UpdateEventStatusByScoreRequest(event_id=event_id, score=rate))
        return response.success
