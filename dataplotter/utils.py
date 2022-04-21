from matplotlib import pyplot as plt
import numpy as np
import tkinter as tk


def get_timestamp(path):

    with open(path,'r') as f:

        for line in f:
            if line.startswith('1'):
                break

        # Skips the next two lines
        next(f)
        next(f)
        line = next(f)

        data = line.split('\t')
        tstamp = data[1]

    return float(tstamp)


def plot(files,channels):

    print('New selection made. Analyzing data.\nFiles complete: 0/'+str(len(files)))
    # get data from files
    all_data = []
    for i,file in enumerate(sorted(files,key=lambda x:get_timestamp(x))):

        f = open(file)

        # get number of lines in f then set pointer back to top
        len_f = len(f.readlines())
        f.seek(0)

        # this loop skips through the metadata
        counter = 0
        for line in f:
            counter += 1
            if line.startswith('1'):
                break

        len_f = len_f - counter - 2 # find number of lines of actual data (total lines - meta data - 2 lines of header)

        all_channels = next(f).strip().split('\t')
        next(f)
        idx = [all_channels.index(i) for i in channels]

        data = np.zeros((len_f,len(idx)),dtype=np.float16)

        for j,line in enumerate(f):

            tmp = line.split('\t')
            data[j] = np.array([tmp[k] for k in idx])
            pct_complete = '{:.2%}'.format(j/len_f)
            print(pct_complete, end='\r')

        all_data.append(data)

        f.close()
        print('\nFiles complete: '+str(i+1)+'/'+str(len(files)))

    print('-------------------\n')
    all_data = np.vstack(all_data) # combine data from each file into one large numpy array

    for i in range(all_data.shape[1]):
        plt.plot(all_data[:,i],label=channels[i])

    plt.legend(loc='upper right')
    plt.xlabel('Time (s)')
    plt.title(','.join(channels) + ' vs. Time')
    plt.grid()
    plt.show()

if __name__ == '__main__':

    files = [r'C:\Users\LZHL65\Desktop\TC57ASeal12021614091551_nTrans_0.dat',r'C:\Users\LZHL65\Desktop\TC57ASeal12021614091551_nTrans_1.dat']
    channels = ['humEcc1Feedback','tEcc1Feedback','tChiller2Feedback']
    plot(files,channels)