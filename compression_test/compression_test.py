import audioop
import io
import zlib
import os
import sys

from opuslib import Encoder

enc = Encoder(48000, 2, 'audio')

file_name = os.path.join(
    os.path.dirname(__file__),
    '../resources',
    sys.argv[1])

with io.open(file_name, 'rb') as audio:
    audio_content = audio.read()

zlib_compressed = zlib.compress(audio_content)
adpcm_audio = audioop.lin2adpcm(audio_content, 2, None)
opus_audio = enc.encode(audio_content, 960)
zlib_compressed_adpcm = zlib.compress(adpcm_audio[0])
zlib_compressed_opus = zlib.compress(opus_audio)
uncompressed_audio = audio_content

print(len(uncompressed_audio))
print(len(zlib_compressed))
print(len(adpcm_audio[0]))
print(len(opus_audio))
print(len(zlib_compressed_adpcm))
print(len(zlib_compressed_opus))

compress_ratio_audio = (float(len(audio_content)) - float(len(audio_content))) / float(len(audio_content)) * 100
compress_ratio_zlib = (float(len(audio_content)) - float(len(zlib_compressed))) / float(len(audio_content)) * 100
compress_ratio_adpcm = (float(len(audio_content)) - float(len(adpcm_audio[0]))) / float(len(audio_content)) * 100
compress_ratio_opus = (float(len(audio_content)) - float(len(opus_audio))) / float(len(audio_content)) * 100
compress_ratio_adpcm_zlib = (float(len(audio_content)) - float(len(zlib_compressed_adpcm))) / float(len(audio_content)) * 100
compress_ratio_opus_zlib = (float(len(audio_content)) - float(len(zlib_compressed_opus))) / float(len(audio_content)) * 100

print(f"Original: {compress_ratio_audio:.2f}%\nzlib: {compress_ratio_zlib:.2f}%\nadpcm: {compress_ratio_adpcm:.2f}%\nopus: {compress_ratio_opus:.2f}%\nzlib+adpcm: {compress_ratio_adpcm_zlib:.2f}%\nzlib+opus:{compress_ratio_opus_zlib:.2f}%")