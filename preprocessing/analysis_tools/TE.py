import os


import analysis_tools.entropy_estimators as ee
#import entropy_estimators as ee
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def getDT(data): 
    df = pd.read_csv(data)
    DT = np.mean(np.diff(df['seconds'].values))
    
    return DT
    


def getPreprocessedData(dat, frame_step): 
    df = pd.read_csv(dat)
    cols = df.columns
    agent_names = [a[: a.find('_vx')] for a in cols if a.find('_vx') >=0]
    print(agent_names)
    vels = []
    for an in agent_names: 
        vx = df[an + '_vx'].values
        vy = df[an + '_vy'].values
        print('len vx before downsampling', len(vx))
        if frame_step > 0:
            vx = vx[::frame_step]
            vy = vy[::frame_step]
            print('len vx after downsampling', len(vx))
        vels.append(np.vstack((vx, vy)).T)
        print(len(vels))
    #DT = np.mean(np.diff(df['seconds'].values))
    
    return vels, agent_names


    
def CreateTEObservables(P0,P1,ds=3,obstype='vel',normalizedvel=False):
    ''' Generates the observable arrays for transfer entropy calculation

        Input:
        P0: position vector individual 0, array(timesteps,2)
        P1: position vector individual 1, array(timesteps,2)
        ds: sampling rate (ds=3 default - use every 3rd frame)
        obstype: velocity vectors -> 'vel' (default), vel. towards (scalar) 'veltow'
        normalizedvel: normalization by speed, only used for obstype='veltow'
        
    '''
    # make sure position vectors are of the same length
    dl = min(len(P0), len(P1))
    P0 = P0[:dl]
    P1 = P1[:dl]
    print(P0.shape)
    print(P0[::ds].shape)
    #calculate velocity and accellerartion #TODO: this doesn't need an extra function
    vel0,acc0=CalcVelAcc(P0[::ds]) #slicing the array in steps of ds (here take only every 3rd frame)
    vel1,acc1=CalcVelAcc(P1[::ds])

    if(obstype=='vel'):
        obs0=vel0
        obs1=vel1
    elif(obstype=='veltow'):
        relvec0=P1[::ds]-P0[::ds]
        relvec1=P0[::ds]-P1[::ds]
        speed0  =np.reshape(np.linalg.norm(vel0,axis=1),(-1,1))
        speed1  =np.reshape(np.linalg.norm(vel1,axis=1),(-1,1))
        reldist0=np.reshape(np.linalg.norm(relvec0,axis=1),(-1,1))
        reldist1=np.reshape(np.linalg.norm(relvec1,axis=1),(-1,1))
        relvec0=np.divide(relvec0,reldist0)
        relvec1=np.divide(relvec1,reldist1)
        if(normalizedvel):
            vel0=np.divide(vel0,speed0)
            vel1=np.divide(vel1,speed1)
        obs0=np.dot(vel0,relvec0.T)[:,0]
        obs1=np.dot(vel1,relvec1.T)[:,0]
        obs0=np.reshape(obs0,(-1,1))
        obs1=np.reshape(obs1,(-1,1))

    return obs0,obs1





def CalcCMIPair(obs0,obs1,lag=1,k=3,t0=0): 
    '''
    Calculates conditional mutual information for a pair of observables in both directions. Calculation
    uses entropy estimators.
    
    Inputs:
    obs0, obs1......vectors of shape (samples, 2) either raw or directed velocity
    lag.............shift in prediction eg. predict x(n+lag) from x(n), y(n) 
    k...............order of Markov process eg predict x(n+lag) from x(n, n-1, .., n-k), y(n, n-1, .., n-k) 
    t0..............cutoff for vectors i.e don't consider values smaller than index t0
    
    Outputs: 
    cmi10...........Conditional Mutual information from obs1 to obs0  
    cmi01...........Conditional Mutual information from obs0 to obs1  
    '''
    print('lag, k, t0', lag, k, t0) 
    total_points=len(obs0)
    
    x10=list(obs0[t0+lag:, :]) # future of 0 
    y10=list(obs1[t0:-lag, :]) # past of 1
    z10=list(obs0[t0:-lag, :]) # past of 0

    cmi10=ee.cmi(x10,y10,z10,k=k) #output is one number i.e sum over all x 
            
    x01=list(obs1[t0+lag:]) # future of 1
    y01=list(obs0[t0:-lag]) # past of 0
    z01=list(obs1[t0:-lag]) # past of 1

    cmi01=ee.cmi(x01,y01,z01,k=k)
    return cmi01,cmi10  
    
def CalcSingleTE(obs0,obs1,results,parameters,i):
    ''' gets called by RunParallelTE. For giben index i a corresponding set of paarmeters is used to
    call CalcCMIPair. 
    
    Inputs
    obs0, obs1......vectors of shape (samples, 2) either raw or directed velocity
    results.........empty array of shape (iterations, 2)
    parameters......array of shape (iterations, 2), here for each iteration we get a different lag (increasing from 1 to 9)
                    but always k= 3, and t0 = 18
    i...............index for the parameter vectorize
    
    Outputs
    results.........list of TE values for different lags    
    '''
   
    loc_params=parameters[i]
    print(parameters[i])
    lag = loc_params[0]
    k   = loc_params[1]
    t0  = loc_params[2]
    cmi01,cmi10 = CalcCMIPair(obs0,obs1,lag=lag,k=k,t0=t0)
    
    results[i,0] = cmi01
    results[i,1] = cmi10
    
    #global GLOBAL_COUNTER = GLOBAL_COUNTER-1
    
    return

def RunParallelTE(obs0,obs1,parameter_array,threads=1):
    import multiprocessing as mp
    import multiprocessing.managers
    from functools import partial

    class MyManager(multiprocessing.managers.BaseManager):
        pass

    MyManager.register('np_zeros',np.zeros,multiprocessing.managers.ArrayProxy)
    m=MyManager()
    m.start()
    results=m.np_zeros((len(parameter_array),2))
    func=partial(CalcSingleTE,obs0,obs1,results,parameter_array)
    pool=mp.Pool(threads)
    run_list=range(len(parameter_array))
    pool.map(func,run_list) # calls CalcSingleTE with i in range 0 to 9
    pool.close()
    pool.join()

    return results
    
def write2file(results, lags, filename, folder, name0, name1): 
    N = len(results)
    
    with open(folder + filename, 'w') as f: 
        f.write('lags[s] + \t' + name0 + '\t' + name1 + '\n')
        for n in range(N): 
            f.write(str(lags[n]) + '\t' + str(results[n, 0]) + '\t' + str(results[n, 1]) + '\n')

        

def plot_results(results, lags, filename, folder, name01, name10):  
    
    plt.figure(figsize = (8, 3))
    plt.plot(lags, results[:, 0], label = name01)
    plt.plot(lags, results[:, 1], label = name10)
    plt.ylabel('TE')
    plt.xlabel('lag[s]')
    plt.legend()
    
    plt.savefig(folder +filename)

        
def TE(datafile = 'TE_test_sin.csv', folder = '/home/claudia/Dokumente/Uni/lab_rotation_FU/pyQt/preprocessing/stats', csv_name = '/TE_test_results_sin.csv', img_name = '/TE_test_sin.jpg', start_frame = 18, maxtime = 10, k_te = 3, frame_step = None): 
    
    #params
    #frame_step = 5
#    start_frame = 18 #original 18
#    maxtime = 10 # in seconds 
#    k_te = 3 #original 3
    
    DT = getDT(datafile)
    print('dt before downsampling', DT)
    # goal: calculate frame_step as a function of dt
    # such that the resulting file has dt' = 0.3
    if frame_step == None or int(frame_step) == 0: 
        print('set to 1')
        frame_step = 1
        #frame_step = int(np.ceil(0.3 / DT))
    else: 
        frame_step = int(frame_step)
    print('chosen frame_step', frame_step)
    
    
    #preprocess
    v, an = getPreprocessedData(datafile, frame_step)
    
    DT_prime = DT * frame_step 
    print('DT', DT)
    print('frame_step', frame_step)
    print('DT_prime', DT_prime)
    
    maxlag=int(float(maxtime)/float(DT_prime)) #i.e lag in terms of frames
    print('maxlag', maxlag)

        
    obs0 = v[0]
    obs1 = v[1]

    # build param list
    lag_list = np.arange(1,maxlag)
    #GLOBAL_COUNTER = maxlag
    lag_times = lag_list*DT_prime
    
    parameters_array = np.zeros((len(lag_list),3))
    parameters_array[:,0] = np.int32(lag_list)
    parameters_array[:,1] = k_te
    parameters_array[:,2] = start_frame
    parameters_array = np.int32(parameters_array)

    results = RunParallelTE(obs0,obs1,parameters_array)

    name01 = an[0] + '->' + an[1]
    name10 = an[1] + '->' + an[0]

    write2file(results, lag_times, csv_name, folder, name01, name10)
    plot_results(results, lag_times, img_name, folder, name01, name10)
    print('Results:\n', results)

    return True



def main(): 
    TE()
    
    
if __name__ == "__main__": 
    main()
