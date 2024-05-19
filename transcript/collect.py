from typing import List, Dict
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


def extractVideoId(video_url: str):
    parsed_url = urlparse(video_url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params['v'][0]
    return video_id


def mergeMiniChunks(transcript_chunks: List[List[Dict]]):
    transcript = []
    for chunks in transcript_chunks:
        text = " ".join(list(map(lambda chunk: chunk.get("text"), chunks)))
        st_time = chunks[0].get('start')
        total_duration = sum([c.get("duration") for c in chunks])
        transcript.append({
            "text": text,
            "start": st_time,
            "duration": total_duration
        })
    return transcript


def chunkTranscript(transcript: List[Dict], max_time: int = 60):
    transcript_chunks = [[]]
    index = 0
    current_time = 0
    while index < len(transcript):
        content = transcript[index]
        duration = content.get("duration")
        if current_time + duration > max_time:
            transcript_chunks += [[]]
            current_time = 0
            index -= 1  # to create an overlap
        transcript_chunks[-1] += [content]
        current_time += duration
        index += 1
    transcript = mergeMiniChunks(transcript_chunks)
    return transcript


def getTranscriptData(video_url: str):
    video_id = extractVideoId(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    if not transcript:
        raise Exception("Transcript Not Available")
    transcript = chunkTranscript(transcript)
    return transcript
