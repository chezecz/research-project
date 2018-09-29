import audioop
import io
import zlib
import os
import sys

file_name = os.path.join(
    os.path.dirname(__file__),
    'resources',
    sys.argv[1])

with io.open(file_name, 'rb') as audio:
    audio_content = audio.read()

compressed_audio = audioop.lin2adpcm(audio_content, 2, None)
zlib_compressed = zlib.compress(audio_content)
zlib_compressed_audio = zlib.compress(compressed_audio[0])
uncompressed_audio = audioop.adpcm2lin(compressed_audio[0], 2, None)

print(len(audio_content))
print(len(compressed_audio[0]))
print(len(zlib_compressed_audio))

compress_ratio_audio = (float(len(audio_content)) - float(len(compressed_audio[0]))) / float(len(audio_content)) 
compress_ratio_zlib = (float(len(audio_content)) - float(len(zlib_compressed))) / float(len(audio_content)) 
compress_ratio_audio_zlib = (float(len(audio_content)) - float(len(zlib_compressed_audio))) / float(len(audio_content)) 

print(f"Only Audio: {compress_ratio_audio}\nOnly zlib: {compress_ratio_zlib}\nzlib and audio: {compress_ratio_audio_zlib}")