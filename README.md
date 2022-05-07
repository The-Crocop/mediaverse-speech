# mediaverse-speech
Grpc Speech API for mediaverse. 
The mediaverse Speech API allows users to transcribe and translate their video assets. 
It is a grpc based API and supports many different programming languages.
An API key can be created on demand.

This repository contains the protobuf file and samples in different languages. 

Supported Languages are English (EN), German (DE), French (FR), Italian (IT),Spanish (ES), Ukrainian (UK), and Catalan (CA)

## Usage

The api is located at [speech.citizenjournalist.io:443][url].

Beyond clients in different languages you can also use tools designed to access GRPC Apis.

One very popular client is [grpcurl](https://github.com/fullstorydev/grpcurl)
It is like curl but for GRPC.

The Mediaverse Speech API has the following endpoint

`sftpprocessor.Subtitling/Transcribe`

It takes all the TranscriptionRequest Options as intput and returns a stream of results for different languages.
In core you pass a video link, desired languages, desired subtitle formats as input
and you will receive links for the different subtitle files with some additonal Information.
Sample Request:

```
grpcurl  -d '{"sourceUrl": "https://media.swissinfo.ch/media/video/ffd360ee-24ac-4ea0-b3c0-7ac062cacb31/rendition/65278f48-c0ec-4669-98de-793674c9cee2.mp4", "format" : ["SRT", "VTT"], "outputLanguages" : ["EN","DE","FR","IT","ES"], "externalReference": "1234", "headers": {"headers": {"Authorization":"Basic dGVzdDp0ZXN0"}   }}' -H "Authorization: Bearer $JWT" speech.citizenjournalist.io:443  sftpprocessor.Subtitling/Transcribe
```

where $JWT is your API Key.

The service will return a stream of generated subtitle links with the detected language and additional information.

```
{
  "externalReference": "1234",
  "transcriptionUrl": "https://ipfs.citizenjournalist.io/ipfs/QmV98UL67tsSyNHjL3F3CaBHSktKkjAL5yinwePaFNYXQo",
  "format": "SRT",
  "language": "DE",
  "original": true,
  "cid": "QmV98UL67tsSyNHjL3F3CaBHSktKkjAL5yinwePaFNYXQo"
}
...
```
## Request Fields

| Field Name          | Explanation                                                                                                                                                                                                                                                                                                                                  | Sample Value                                                                                                                     |
|:--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| externalReference   | can be an arbitrary value. Usually you can use the id of the video asset in your system as reference                                                                                                                                                                                                                                         | "1234"                                                                                                                           |
| sourceUrl (*)       | url where the video asset can be downloaded. Must be reachable from the internet                                                                                                                                                                                                                                                             | "https://media.swissinfo.ch/media/video/ffd360ee-24ac-4ea0-b3c0-7ac062cacb31/rendition/65278f48-c0ec-4669-98de-793674c9cee2.mp4" |
| format (*)          | output format of the generated subtitle files. This is an array. Possible values  "SRT" , "VTT" and "MP3", Srt and VTT will generate a subtitle file as text, while mp3 will generate a spoken transcription as audio file (mp3)                                                                                                             | ["SRT", "VTT"]                                                                                                                   |
| outputLanguages (*) | desired Languages the subtitles will be generated in. The service will automaticall detect the language in the video and translate to other languages appropriately. Possible Values: "EN","DE","FR","IT","ES","CA","UK"                                                                                                                     | ["EN","DE","FR","IT","ES"]                                                                                                       |
| headers             | if we require additional headers to access the sourceUrl (source video). Those can be passed in this field. Eg if the source video is protected with Basic Authentication it would be the basic Auth header. Could also be an OAuth2 Bearer token. Or some other headers required for access to sourceUrl. Its a Map containing the headers. | {"headers": {"Authorization":"Basic dGVzdDp0ZXN0"}   }                                                                           |


`* means required other fields are optional`

## Response Fields:

| Field Name        | Explanation                                                                                                                                                                              | Sample Value                                                                            |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| externalReference | same external reference value that was passed in request. Can be used for matching on client side                                                                                        | "1234"                                                                                  |
| transcriptionUrl  | url of the subtitle file. It can be downloaded from there. Or used directly in an html player                                                                                            | "https://ipfs.citizenjournalist.io/ipfs/QmNgDcKGoAds1cSUZVRui6LyN1hRvjCNW6BhpM61N5eeTs" |
| format            | subtitle format of the transcription or translation subtitle file. Can be VTT, SRT or MP3 if you requested multiple there will be one entry for VTT and one for SRT in the result stream | "SRT"                                                                                   |
| language          | the language of the subtitle. It will be one of the outputLanguages from the request. There will be an event for each Subtitle Format and Language Pair.                                 | "ES"                                                                                    |
| original          | true or false. If this is the detected language from the source video the field will be true. If it is one of the  translated subtitles it will be false                                 | false                                                                                   |
| cid               | ipfs multihash. this  is the unique hashed content identifier for the subtitle file                                                                                                      | "QmV98UL67tsSyNHjL3F3CaBHSktKkjAL5yinwePaFNYXQo"                                        |

### Links

[Java Client Library](https://github.com/The-Crocop/mediaverse-speech-lib)