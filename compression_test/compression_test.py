import audioop
import io
import zlib
import os
import sys
import wave

from opuslib import Encoder, Decoder

enc = Encoder(48000, 2, 'audio')

dec = Decoder(48000, 2)

file_name = os.path.join(
    os.path.dirname(__file__),
    '../resources',
    sys.argv[1])

with io.open(file_name, 'rb') as audio:
    audio_content = audio.read()

wf = wave.open(file_name, 'rb')

orig = []
encoded = []

zlib_compressed = zlib.compress(audio_content)
adpcm_audio = audioop.lin2adpcm(audio_content, 2, None)
while True:
	data = wf.readframes(960)
	if data == b'':
		break
	orig.append(data)

for element in orig:
	opus_audio = enc.encode(element, 960)
	encoded.append(opus_audio)

zlib_compressed_adpcm = zlib.compress(adpcm_audio[0])
uncompressed_audio = audio_content

opus_audio = b''.join(encoded)

zlib_compressed_opus = zlib.compress(opus_audio)

print(len(uncompressed_audio))
print(len(zlib_compressed))
print(len(adpcm_audio[0]))
print(len(opus_audio))
print(len(zlib_compressed_adpcm))
print(len(zlib_compressed_opus))

wf.close()

compress_ratio_audio = (float(len(audio_content)) - float(len(audio_content))) / float(len(audio_content)) * 100
compress_ratio_zlib = (float(len(audio_content)) - float(len(zlib_compressed))) / float(len(audio_content)) * 100
compress_ratio_adpcm = (float(len(audio_content)) - float(len(adpcm_audio[0]))) / float(len(audio_content)) * 100
compress_ratio_opus = (float(len(audio_content)) - float(len(opus_audio))) / float(len(audio_content)) * 100
compress_ratio_adpcm_zlib = (float(len(audio_content)) - float(len(zlib_compressed_adpcm))) / float(len(audio_content)) * 100
compress_ratio_opus_zlib = (float(len(audio_content)) - float(len(zlib_compressed_opus))) / float(len(audio_content)) * 100

print(f"Original: {compress_ratio_audio:.2f}%\nzlib: {compress_ratio_zlib:.2f}%\nadpcm: {compress_ratio_adpcm:.2f}%\nopus: {compress_ratio_opus:.2f}%\nzlib+adpcm: {compress_ratio_adpcm_zlib:.2f}%\nzlib+opus:{compress_ratio_opus_zlib:.2f}%")