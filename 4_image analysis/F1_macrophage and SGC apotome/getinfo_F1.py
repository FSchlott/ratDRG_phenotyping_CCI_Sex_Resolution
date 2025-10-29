import matplotlib.pyplot as plt
import numpy as np
from skimage import measure
from skimage.morphology import disk
from skimage.morphology import binary_dilation
from tqdm.auto import tqdm
import os

class ImageData : 
    def __init__ (self, subdir): 
        nfmask_paths = os.path.join(subdir, 'nf_pred/masks')
        gfapmask_paths = os.path.join(subdir, 'gfap_pred/masks')
        iba1mask_paths = os.path.join(subdir, 'iba1_pred/masks')  
        
        #empty lists to append results 
        self.iba1_per_nra_L = []
        self.gfap_per_nra_L = []
        self.iba1_anz_L = []
        self.gfap_anz_L = []

        self.neuronarea_um_L = []
        self.iba1_um_L = []
        self.gfap_um_L = []


        #for each file in the respective subfolders
        for nfM_filename , gfapM_filename , iba1M_filename in tqdm(zip(os.listdir(nfmask_paths), os.listdir(gfapmask_paths),
                                         [fn for fn in os.listdir(iba1mask_paths) if fn.endswith ("png")])):
        
                                     
            nfM = plt.imread (os.path.join (nfmask_paths, nfM_filename))
            gfapM = plt.imread (os.path.join (gfapmask_paths, gfapM_filename))
            iba1M = plt.imread (os.path.join (iba1mask_paths, iba1M_filename))

            #extract data
            neuronarea_um, iba1_per_nra, iba1_anz, iba1_um, gfap_per_nra, gfap_anz, gfap_um = self.quantify_per_neuronarea (nfM , iba1M , gfapM)
        
            #append lists
            self.iba1_per_nra_L.append (float(iba1_per_nra))
            self.gfap_per_nra_L.append (float(gfap_per_nra))
            self.iba1_anz_L.append (float (iba1_anz))
            self.gfap_anz_L.append (float (gfap_anz))
            self.neuronarea_um_L.append (float (neuronarea_um))
            self.iba1_um_L.append (float (iba1_um))
            self.gfap_um_L.append (float (gfap_um))
    

    def get_ov_numbers (self, neuronarea, qM) :
        addM = qM + neuronarea
        overlap = (addM == 2)*1
        #gets label numbers and area
        labels , anz = measure.label (overlap , return_num = True )  
        qsum = np.sum (overlap)
        sum_um = qsum * 0.184 #from px to mm2
        per_nra = (qsum/np.sum (neuronarea))*100 #area per neuronarea
        return per_nra , anz , sum_um

    def quantify_per_neuronarea (self, nfM, iba1M, gfapM) :
        shape = disk (20) #for dilation of neurons
        neuronarea = binary_dilation (nfM, shape)
        neuronarea_um2 = (np.sum (neuronarea)) * 0.184 #from px to mm2
        # get numbers per neuronarea
        iba1_per_nra , iba1_anz, iba1_um = self.get_ov_numbers (neuronarea, iba1M)
        gfap_per_nra , gfap_anz, gfap_um = self.get_ov_numbers (neuronarea, gfapM)

        return neuronarea_um2 , iba1_per_nra, iba1_anz , iba1_um, gfap_per_nra , gfap_anz , gfap_um
