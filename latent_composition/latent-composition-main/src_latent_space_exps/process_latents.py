"""
Date: 13/01/2021
In this file, latent pre-processing functions are implemented. For each of the attribute in question only few layers
correspond to those variations, filtering out other layer variations can help make edit more disentagled and clear
"""

import numpy as np
import os 
import pickle 

"""
​​Expression (4 − 5), 
Yaw (0 − 3), 
Age (4 − 7), 
Add Glasses (0 − 5) | (0 - 9)
Hat (0 - 5) 
Baldness (0 − 5) 
Bangs (0 - 5)  
Facial hair (5 − 7 and 10).  
"""
# ['bang', 'eye_g', 'smile', 'bald', 'hat', 'pose', 'age_60_', 'beard', 'age']      
def filter_direction(latent, attr):
    #  print("attribute: ", attr)
    if (attr == 'bang'):
        latent[0,6:18,:] = np.zeros((12, 512)) 

    elif (attr == 'eye_g'):
        latent[0,9:18,:] = np.zeros((9, 512))  

    elif (attr == 'smile'):
        latent[0,0:4,:] = np.zeros((4, 512))
        latent[0,6:18,:] = np.zeros((12, 512))

    elif (attr == 'bald'):
        latent[0,6:18,:] = np.zeros((12, 512))

    elif (attr == 'hat'):
        latent[0,6:18,:] = np.zeros((12, 512))

    elif (attr == 'pose'):
        latent[0,4:18,:] = np.zeros((14, 512))

    elif (attr == 'age_60_'):
        latent[0,:4,:] = np.zeros((4, 512)) 
        latent[0,8:,:] = np.zeros((10, 512))

    elif (attr == 'age_70_'):
        latent[0,:4,:] = np.zeros((4, 512)) 
        latent[0,8:,:] = np.zeros((10, 512))

    elif (attr == 'age_80_'):
        latent[0,:4,:] = np.zeros((4, 512)) 
        latent[0,8:,:] = np.zeros((10, 512))

    elif (attr == 'beard'):
        latent[0,0:5,:] = np.zeros((5, 512))
        latent[0,8:10,:] = np.zeros((2, 512))
        latent[0,11:,:] = np.zeros((7,512))  

    elif (attr == 'eye_g_style'):
        latent[0,9:18,:] = np.zeros((9, 512))  

    elif (attr == 'hair_style'):
        latent[0,6:18,:] = np.zeros((12, 512))

    return latent 

# This function will take the bundle of latent codes along with the corresponding attribute and calls the filtering function to retain only important layers 
def process_latents(latents, attr):
    # Iterating over latents for any particular attribute 
    filtered_latents = []
    for id in range(0, latents.shape[0]):
        latent = latents[id] 
        filtered_latent = filter_direction(latent, attr)        
        filtered_latents.append(filtered_latent)    
    
    filtered_latents = np.array(filtered_latents)
    return filtered_latents

# This function will take the bundle of latent codes for any given attribute set and perform filteration of direction by zeroing out some components 
def process_style_latents(latent_db, attr):
    modified_dict = {}
    # Iterating over all the attribute styles and their corresponding pair of original and transformed images to process the latent attributes 
    for k, all_dirs in latent_db.items():
        # Normalizing all the pairwise distances to have unit length before averaging
        # print("Key for att: ", k, " length of transforms: ", len(all_dirs))
        # print("All direction shape: ", len(all_dirs)) 
        filtered_latents = [] 
        for id in range(len(all_dirs)):
            latent = all_dirs[id]
            filtered_latent = filter_direction(latent, attr) 
            filtered_latents.append(filtered_latent)

        # print("filtered direction shape: ", len(filtered_latents))
        filtered_latents = np.array(filtered_latents)
        modified_dict[k] = filtered_latents 

    return modified_dict


# This function will call other basic functions to process the latent codes based on the attribute in question 
def run_main():
    # Attributes for editing with a set of latent vectors
    """
    attr_list = ['bang', 'eye_g', 'smile', 'bald', 'hat', 'pose', 'age_60_', 'age_70_', 'age_80_', 'beard']  
    latent_paths_src = ['latent_db_dir_id_11_bang.npy', 'latent_db_dir_id_17_eye_g.npy', 'latent_db_dir_id_18_smile.npy', 'latent_db_dir_id_20_bald.npy',
                   'latent_db_dir_id_20_hat.npy', 'latent_db_dir_id_14_pose.npy', 'latent_db_dir_id_12_age_60.npy', 'latent_db_dir_id_12_age_70.npy',
                   'latent_db_dir_id_12_age_80.npy', 'latent_db_dir_id_8_beard.npy']
    """

    # Attribute Style editing with a set of latent vectors for variations of attribute styles 
    attr_list = ['eye_g_style', 'hair_style']
    latent_paths_src = ['latent_style_att_dir_db_eye_g_style.csv', 'latent_style_att_dir_db_hair_style.csv'] 

    dirs_files_root = '../../data_files/estimated_att_styles/'  
    dirs_files_root_fltd = '../../data_files/estimated_att_styles_filt/'  

    latent_paths = [os.path.join(dirs_files_root, lp) for lp in latent_paths_src]
    latent_paths_dst = [os.path.join(dirs_files_root_fltd, lp) for lp in latent_paths_src]  

    n_attr = 10
    for id in range(0, 2):
        # latent_db = np.load(latent_paths[id])
        load_file = open(latent_paths[id],'rb') 
        latent_db = pickle.load(load_file)     
        attr = attr_list[id]
        print("Processing attribute: ", attr, " from path: ", latent_paths[id]) 

        # processed_latent_db = process_latents(latent_db, attr)
        processed_latent_db = process_style_latents(latent_db, attr)  

        # print("Processed latent shape: ", processed_latent_db.shape)
        # print("Saving latent at: ", latent_paths_dst[id])

        # np.save(latent_paths_dst[id], processed_latent_db)
        
        print("Saving the processed latents at: ", latent_paths_dst[id])
        fhandle = open(latent_paths_dst[id], "wb")  
        pickle.dump(processed_latent_db, fhandle)


if __name__ == "__main__":
    run_main()
