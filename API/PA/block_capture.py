import os
import sys
import time
import pyaudio
import wave


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100    

def main(arg_duration, arg_outfile):
    """
    This is the default approach to a simple audio capture of a fixed duration using PyAudio. The method requires that 4 contants be defined:
        The frames per buffer, an integer.
        The format, in this case we simply point to pyaudio.paInt16
        The number of channels that the audio data will use, in this case 2
        And finally the sample rate as an integer
        Because this implementation does not have concurrent execution, we have to specify the duration in seconds (float or int) that we want to capture.

        Before an audio stream can be opened, we need to initialize a pyaudio.PyAudio() object, which will allow our application to access the PortAudio bindings, our actual C++ audio engine.
    
        We then create an instance of a stream object by calling the pyaudio.PyAudio() method open, providing the format, number of channels, sample rate, chunk size, and give the stream input capability
    """

    DURATION = int(arg_duration)
    OUTFILE = str(arg_outfile).strip()
    
    print("Initializing PyAudio instance..")

    p = pyaudio.PyAudio()

    input("Finished Initialization, press Return to continue >> ")

    print("Opening input stream..")
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording for {} seconds".format(str(DURATION)))
    
    frames = []

    for i in range(0, int(RATE / CHUNK * DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Capture finished")
    input("Press Return to properly close the stream and write the capture to a .wav file >> ")
    print("Stopping and closing the input stream..")
    stream.stop_stream()
    stream.close()
    print("Terminating the PyAudio instance now that we no longer need to utilize any sound devices.")
    p.terminate()

    input("Press Return to build a .wav file and save the captured frames >> ")

    print("Opening new wave file '{}' for writing in binary mode..".format(OUTFILE))

    wf = wave.open(OUTFILE, 'wb')
    print(f"Specifying that there are {CHANNELS}")
    wf.setnchannels(CHANNELS)
    print("Specifying the sample width to equal that of the format of the audio array")
    wf.setsampwidth(p.get_sample_size(FORMAT))
    print(f"Specifying framerate of {RATE}")
    wf.setframerate(RATE)
    print("Arranging the individual frames of audio into one continuous buffer.")
    wf.writeframes(b''.join(frames))
    print("Finished, closing the wave file.")
    wf.close()

    print("Good bye")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage\n===========\n$ python3 block_capture.py [duration] [outfile]")
        sys.exit()

    arg_duration = sys.argv[1]
    arg_outfile = sys.argv[2]

    main(arg_duration, arg_outfile)

