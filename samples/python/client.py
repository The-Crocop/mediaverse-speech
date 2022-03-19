import subtitling_pb2
import subtitling_pb2_grpc
import grpc
import logging
import os

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    jwt = os.environ['JWT']
    metadata = [('authorization', f"Bearer {jwt}")]
    credentials = grpc.ssl_channel_credentials()

    with grpc.secure_channel('speech.citizenjournalist.io:443', credentials) as channel:
        stub = subtitling_pb2_grpc.SubtitlingStub(channel)
        print("-------------- Transcribe --------------")
        for response in stub.Transcribe(subtitling_pb2.TranscriptionRequest(
                externalReference='1234',
                sourceUrl='https://ipfs.citizenjournalist.io/ipfs/QmPuqoid7n12tR7LkyX6db7hiYWSvXBYTnYejn4rZDJqsY',
                headers=subtitling_pb2.RequestHeaders(headers={"Authorization": "Bearer 1234"}),
                # this is an example header if the target video is secured
                format=['VTT', 'SRT'],
                outputLanguages=["EN", "DE", "ES", "FR", "IT"]
        ), metadata=metadata):
            print('---')
            print(f'cid: {response.cid}')
            print(f'transcriptionUrl: {response.transcriptionUrl}')
            print(f'language: {subtitling_pb2.Language.Name(response.language)}')
            print(f'format: {subtitling_pb2.SubtitleFormat.Name(response.format)}')
            print(f'original: {response.original}')
            print(f'externalReference: {response.externalReference}')
            print('---')


if __name__ == '__main__':
    logging.basicConfig()
    run()
