import matplotlib.pyplot as plt
from skimage import measure
from tqdm.auto import tqdm
import os
import tifffile as tiff
import numpy as np


class ImageData : 
    def __init__ (self, subdir):
        nfmask_paths = os.path.join(subdir, 'nf_pred/masks')
        ib4mask_paths = os.path.join(subdir, 'ib4_pred/masks')
        nfcellpose_paths = os.path.join(subdir, 'nf_cellpose/cellpose_masks')
        ib4cellpose_paths = os.path.join(subdir, 'ib4_cellpose/cellpose_masks')

        self.nf_anz_L = []
        self.ib4_anz_L = []
        self.overlap_nf_ib4_anz_L = []
        self.nf_sizes_L = []
        self.ib4_sizes_L = []
        self.ib4_per_nf_L = []
        self.ib4oL_per_nf_L = []

        for nfM_filename , nfcp_filename, ib4M_filename, ib4cp_filename in tqdm(zip(os.listdir(nfmask_paths), 
                                                                            os.listdir(nfcellpose_paths), 
                                                                            os.listdir(ib4mask_paths), 
                                                                            os.listdir(ib4cellpose_paths), )):
            nfM = plt.imread (os.path.join (nfmask_paths, nfM_filename))
            ib4M = plt.imread (os.path.join (ib4mask_paths, ib4M_filename))
            nf_cp_labels = tiff.imread (os.path.join (nfcellpose_paths, nfcp_filename))
            ib4_cp_labels = tiff.imread (os.path.join (ib4cellpose_paths, ib4cp_filename))

            #get overlap and masks 
            overlapM_nf_ib4 = self.get_overlapM (nfM, ib4M)

            #execute functions: get label numbers and sizes 
            ib4_anz , ib4_sizes = self.get_cellnum_sizes (ib4_cp_labels)
            nf_anz , nf_sizes  = self.get_cellnum_sizes_cellpose (nf_cp_labels ) 
            overlap_nf_ib4_anz , overlap_nf_ib4_sizes = self.get_cellnum_sizes (overlapM_nf_ib4)
            ib4oL_per_nf, ib4_per_nf = self.get_percentages_2 (nf_anz, ib4_anz, overlap_nf_ib4_anz)
            
            #append lists
            self.nf_anz_L.append (float (nf_anz))
            self.ib4_anz_L.append (float (ib4_anz))
            self.overlap_nf_ib4_anz_L.append (float (overlap_nf_ib4_anz))
            self.nf_sizes_L.append (nf_sizes)
            self.ib4_sizes_L.append (ib4_sizes)
            self.ib4_per_nf_L.append (ib4_per_nf)
            self.ib4oL_per_nf_L.append (ib4oL_per_nf) 
                       
    
    def get_overlapM (self, mask1 , mask2):
        addM = (mask1 + mask2)
        overlapM = (addM ==2)*1
        return overlapM
    
    #gets number and size of cells per image
    def get_cellnum_sizes_cellpose (self, cellpose):
        sizes = []
        filtered_label = np.zeros([cellpose.shape[0], cellpose.shape[1]])
        count = 1
        for i in range(cellpose.max()+1):
            if i > 0:
                cell = cellpose==i
                if cell.sum() > 150:
                    filtered_label[cell] = int(count)
                    count +=1
                    sizes.append (float (cell.sum()))
        return count, sizes

    #version without cellpose
    def get_cellnum_sizes (self, mask):
        #get labels for neurons
        areas = []
        labels , anz = measure.label (mask , return_num = True)
        props = measure.regionprops (labels)
        #measure area in px per label  
        for i in range (anz): 
            areas.append (float(props[i].area)) 
        #remove values below small neuron siez
        thr = 150 #threshold based on smallest annotated ib4+ cell 
        cell_L = [num for num in areas if num > thr] #new list with only cells above thr
        c_num = len (cell_L)
        return c_num , cell_L 
        
    
    def get_percentages_2 (self, nf_anz, ib4_anz, overlap_nf_ib4_anz):
        if nf_anz > 0: 
            ib4oL_per_nf = (overlap_nf_ib4_anz / nf_anz)*100
            ib4_per_nf = (ib4_anz / nf_anz)*100
        return ib4oL_per_nf, ib4_per_nf