import numpy as np

def direction_correlation(data): 
    
    fish0 = data[['x0', 'y0']].values
    fish1 = data[['y1', 'y1']].values
    time = data['time'].values
    
    N = len(fish0)
    
    front = np.zeros(N)
    
    #normalized0 = np.zeros((N, 2))
    #normalized1 = np.zeros((N, 2))

    center_position = 0.5* fish0 + fish1
    center_velocity = np.diff(center_position, axis = 0).T / np.diff(time, axis = 0)
    center_speed = np.linalg.norm(center_velocity, axis = 0)
    
    fish0_shifted = fish0 - center_position
    fish1_shifted = fish1 - center_position
    
    alphas0 = np.arctan(-fish0_shifted[:, 1] / fish0_shifted[:, 0])
    alphas1 = np.arctan(-fish1_shifted[:, 1] / fish1_shifted[:, 0])

    for i in range(N): 

        rot_mat0 = np.array([[np.cos(alphas0[i]), np.sin(alphas0[i])], [-np.sin(alphas0[i]), np.cos(alphas0[i])]])
        rot_point0 = np.dot(rot_mat0.T, fish0_shifted[i,:])
        
        rot_mat1 = np.array([[np.cos(alphas1[i]), np.sin(alphas1[i])], [-np.sin(alphas1[i]), np.cos(alphas1[i])]])
        rot_point1 = np.dot(rot_mat1.T, fish1_shifted[i,:])
        
        if rot_point0[0] > rot_point1[0]: 
            front[i] = 0
        else: 
            front[i] = 1
        
        #normalized0[i, :] = rot_point0
        #normalized1[i, :] = rot_point1
    

    
    return front, center_speed

