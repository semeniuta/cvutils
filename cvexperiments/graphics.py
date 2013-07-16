import matplotlib.pyplot as plt

def create_and_save_histogram(data, nbins, title, filename):
    ''' 
    Saves the histogram for the given data under the specified filename    
    '''
    plt.figure()    
    plt.hist(data, nbins)
    plt.title(title)
    plt.savefig(filename)