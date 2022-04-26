import os
import vlc
import time
import pydub
import pyaudio
import wave
import threading
from datetime import datetime


class RecordingLogic:
    def __init__(self, station, output_name, start_time, end_time):
        start_time = datetime.strptime(start_time, "%H:%M")
        end_time = datetime.strptime(end_time, "%H:%M")
        self.output_name = output_name
        self.file_name = 'output.wav'

        length_of_recording = self._get_length(start_time, end_time)

        now = datetime.now().strftime("%H:%M")
        while now != start_time.strftime("%H:%M"):
            now = datetime.now().strftime("%H:%M")
            time.sleep(1)

        t1 = threading.Thread(target=self._play, args=(station, end_time), name='t1')
        t2 = threading.Thread(target=self._record_audio, args=(length_of_recording, self.file_name), name='t2')

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print('Playback & Recording - Complete')
        self._convert_to_mp3(self.file_name)

        print("Process Complete. Have a nice day!")

    def _play(self, url, end_time):
        print("Audio Playback - Initiated")

        player = vlc.MediaPlayer(url)
        player.play()

        now = datetime.now().strftime("%H:%M")
        while now != end_time.strftime("%H:%M"):
            now = datetime.now().strftime("%H:%M")
            print("Current Time =", now)
            time.sleep(1)
        player.stop()

        print("Audio Playback - Complete")

    def _record_audio(self, seconds, file_name):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second
        # seconds = 10
        filename = file_name

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Audio Recording - Initiated')

        info = p.get_host_api_info_by_index(0)
        device_count = info.get('deviceCount')
        for i in range(0, device_count):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
            else:
                print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True,
                        input_device_index=3
                        )

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        time.sleep(5)

        print('Audio Recording - Complete')

    def _convert_to_mp3(self, wave_file):
        print("MP3 Conversion - Initiated")
        sound = pydub.AudioSegment.from_wav(wave_file)
        sound.export(f"{self.output_name}.mp3", format='mp3')
        print('MP3 Conversion - Complete')
        print('Removing Wave File - Initiated')
        os.remove(wave_file)
        print('Removing Wave File - Complete')

    def _get_length(self, start_time, end_time):
        diff = end_time - start_time
        return diff.seconds
