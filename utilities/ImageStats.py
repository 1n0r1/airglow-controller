try:
    import Image
except:
    try:
        from Pillow import Image
    except:
        from PIL import Image


import numpy as np
import glob as glob
import ImgImagePlugin

def convolve2d(a,b):
    '''
    A quick and dirty implementation of
    scipy.signal.convolve2d(a,b,mode='valid').
    
    This was needed because I didn't want to install
    scipy on all of the FPI computers.
    
    INPUTS:
        a - a 2d array of size NxN
        b - a 2d array of size MxM
    OUTPUTS:
        c - a 2d array representing the circular convolution of a with b,
            of size KxK where K = max(M,N)
    HISTORY:
        21 Feb 2014: Written by Brian Harding.
    '''
    # zero-pad
    M = np.shape(a)[0]
    N = np.shape(b)[0]
    K = max((M,N))
    
    a2 = np.zeros((K,K))
    b2 = np.zeros((K,K))
    a2[0:M,0:M] = a
    b2[0:N,0:N] = b
    
    
    afft = np.fft.fft2(a2)
    bfft = np.fft.fft2(b2)
    cfft = afft*bfft
    c = np.real(np.fft.ifft2(cfft))
    return c
    


def GetStats(LastImageFile, stub='/cygdrive/c'):
# Function that will add the INTENSITY and INTTIME to the LastImageFile
#
# INPUT:
#	LastImageFile - full cygwin path to the LastImage file
#
# OPTIONAL INPUT:
#	stub - stub to replace "C:" when converting from Windows to
#	       cygwin-style paths (default '/cygdrive/c')
#
# HISTORY:
#	Written by Jonathan J. Makela on 5 Aug 2013
#       Modified "intensity" calculation by Brian J. Harding on 21 Feb 2014

	# Define rectangle to analyze image in
	i1 = 150
	j1 = 150
	i2 = 200
	j2 = 200
	N = 5 # size of averaging kernel to use
	
	# Open the requested LastImageFile
	fid = open(LastImageFile)
	
	# Parse the info
	OBSUID = int(fid.readline().split()[1])
	START = int(fid.readline().split()[1])
	OUTDIR = fid.readline().split()[1]
	fid.close()

	temp = OUTDIR.replace("\\\\","/")
	path = temp.replace("C:", stub)

	# Find the sky exposures in the requested directory
	skys = glob.glob(path + '/*X*.img')
	
	# File to be sent to airglow
	fid = open(LastImageFile + '.snd', 'w')

	# File to be used locally in case internet goes down
	statsFile = ''.join(LastImageFile.rsplit('.',1)[:-1]) + '_stats.txt'
	fid2 = open(statsFile,'w')

	if len(skys) > 0:
		# There are valid sky images.  Proceed
		im = Image.open(skys[-1])
		im = im.convert('I')
		img = np.asarray(im)
		int_time = im.info['ExposureTime']

		# Calculate the "intensity" statistic
		# to use for exposure time adjustment
		imsub = convolve2d(img[i1:i2,j1:j2], np.ones((N,N))/N**2) # smooth out noise
		Iappx = np.percentile(imsub,75) - np.percentile(imsub,25) # calculate "intensity"

		# Write to file
		fid.write('OBSUID: %04d\n' % OBSUID)
		fid.write('START: %d\n' % START)
		fid.write('INTENSITY: %.1f\n' % Iappx)
		fid.write('INTTIME: %.1f\n' % int_time)
		fid.close()
		fid2.write('lastIntensity %.2f\n' % Iappx)
		fid2.write('lastTime %.1f\n' % int_time)
		fid2.close()
	else:
		fid.write('OBSUID: %04d\n' % OBSUID)
		fid.write('START: %d\n' % START)
		fid.write('INTENSITY: -999.9\n')
		fid.write('INTTIME: -999.9\n')
		fid.close()
		fid2.write('lastIntensity %.2f\n' % -999.9)
		fid2.write('lastTime %.1f\n' % -999.9)
		fid2.close()

