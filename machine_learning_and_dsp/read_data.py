import wave


def read_chunk(file,size_of_chunk):
    if file.endswith('.wav') or file.endswith('.WAV'):

        wavefile = wave.open(file, 'r')
	length = wavefile.getnframes()
	Fs = waveFile.getframerate()
	num_chunks = int(length/size_of_chunk)

	for i in range(num_chunks):
	    data = waveFile.readframes(size_chunk)
	    """
		Do processing here and save results
	    """		
    else:
	raise Exception('Incorrect file format!')
