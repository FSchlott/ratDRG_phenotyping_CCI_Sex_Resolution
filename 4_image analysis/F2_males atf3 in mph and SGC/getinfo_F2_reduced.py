import numpy as np
import matplotlib.pyplot as plt
import os
from skimage import measure
from skimage import segmentation
from scipy import ndimage
from tqdm.auto import tqdm
from skimage.morphology import binary_dilation, disk
import tifffile as tiff

class ImageData : 
    def __init__ (self, subdir): #subdirs from pipeline, per rat
        
        neuronsmask_paths = os.path.join(subdir, 'atf3_all_pred/masks')
        neuronscellpose_paths = os.path.join(subdir, 'aft3_all_cellpose/instance_labels')
        atf3mask_paths = os.path.join(subdir, 'atf3_pred/masks')
        iba1mask_paths = os.path.join(subdir, 'iba1_pred/masks')  
        gsmask_paths = os.path.join(subdir, 'gs_pred/masks')

        
        #empty lists to append results
        self.n_anz_L = []
        self.atf3_anz_L = []
        self.atf3_neg_anz_L = []

        self.n_sizes_L = []
        self.atf3_sizes_L = []
        self.atf3_neg_sizes_L = []

        self.iba1_borders_n_L = []
        self.gs_borders_n_L = []
        self.iba1_borders_atf3_L = []
        self.gs_borders_atf3_L = []
        self.iba1_borders_atf3_neg_L = []
        self.gs_borders_atf3_neg_L = []

        self.gs_iba1_proximity_L = []

        #for each file in the respective subfolders
        for nM_filename ,atf3M_filename, gsM_filename , iba1M_filename, n_cellpose_filename in tqdm(zip(os.listdir(neuronsmask_paths),os.listdir(atf3mask_paths), os.listdir(gsmask_paths),
                                         [fn for fn in os.listdir(iba1mask_paths) if fn.endswith ("png")], os.listdir(neuronscellpose_paths))):
                                     
            nM = plt.imread (os.path.join (neuronsmask_paths, nM_filename))
            gsM = plt.imread (os.path.join (gsmask_paths, gsM_filename))
            iba1M = plt.imread (os.path.join (iba1mask_paths, iba1M_filename))
            atf3M = plt.imread(os.path.join (atf3mask_paths , atf3M_filename))
            n_cellpose = tiff.imread (os.path.join (neuronscellpose_paths, n_cellpose_filename))
            atf3_negM = (nM - atf3M == 1) 

            #get neuronnumbers and labels
            n_labels, n_sizes, n_anz = self.get_cellnum_sizes_cellpose (n_cellpose)
            atf3_labels, atf3_sizes, atf3_anz = self.get_cellnum_sizes_atf3 (atf3M)
            atf3_neg_labels, atf3_neg_sizes, atf3_neg_anz = self.get_cellnum_sizes_atf3 (atf3_negM)

            iba1_borders_n = self.get_rings (n_labels , iba1M)
            iba1_borders_atf3 = self.get_rings (atf3_labels , iba1M)
            iba1_borders_atf3_neg = self.get_rings (atf3_neg_labels , iba1M)
            gs_borders_n = self.get_rings (n_labels , gsM)
            gs_borders_atf3 = self.get_rings (atf3_labels , gsM)
            gs_borders_atf3_neg = self.get_rings (atf3_neg_labels , gsM)

            gs_iba1_proximity = self.get_proximity (iba1M, gsM)
            
            #append lists
            self.n_anz_L.append (float(n_anz))
            self.atf3_anz_L.append (float (atf3_anz))
            self.atf3_neg_anz_L.append (float(atf3_neg_anz))
            self.n_sizes_L.append (n_sizes)
            self.atf3_sizes_L.append (atf3_sizes)
            self.atf3_neg_sizes_L.append (atf3_neg_sizes)

            self.iba1_borders_n_L.append (iba1_borders_n)
            self.iba1_borders_atf3_L.append (iba1_borders_atf3)
            self.iba1_borders_atf3_neg_L.append (iba1_borders_atf3_neg)
            self.gs_borders_n_L.append (gs_borders_n)
            self.gs_borders_atf3_L.append (gs_borders_atf3)
            self.gs_borders_atf3_neg_L.append (gs_borders_atf3_neg)

            self.gs_iba1_proximity_L.append (gs_iba1_proximity) 
    

    def get_proximity (self, iba1M, gsM):
        iba1_dilated = binary_dilation (iba1M, disk (2)) #dilates iba1 label by a px to get direct proximity as touch
        addM = iba1_dilated + gsM
        overlap = (addM == 2)*1
        gs_proximity = np.sum (overlap) / np.sum (gsM)
        return gs_proximity

    #version to include labels from cellpose to have distinct cell labels
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
        return np.uint16 (filtered_label), sizes, count


    def get_cellnum_sizes_atf3 (self, mask):
        sizes = [] 
        label = measure.label (mask) #get labels for cells
        unique, counts = np.unique (label, return_counts = True) #unique are the counted labels, counts the respective sizes
        filter = unique [counts > 150][1:] #filters the unique list to values above 150 (smalles manually annotated neuron during model training)
        filteredM = np.isin(label, filter)
        filtered_label, num = measure.label (filteredM , return_num = True)

        props = measure.regionprops (filtered_label)  
        for i in range (num): 
            sizes.append (float(props[i].area)) #area in px
        return filtered_label , sizes, num


    def get_rings(self, n_label, ringmask): 
        #dilate image frame by 5 pixels on borders
        ringmask_framedil = np.zeros([ringmask.shape[0]+20, ringmask.shape[1]+20])
        ringmask_framedil[10:-10, 10:-10] = ringmask
        
        n_label_framedil = np.zeros([n_label.shape[0]+20, n_label.shape[1]+20])
        n_label_framedil [10:-10, 10:-10] = n_label

        #dilate mask for iba or gs by 1px
        ringmask_dilated = ndimage.binary_dilation(ringmask_framedil)*1

        rings= []
        
        for i in range(1, n_label.max()+1):
            #get single neuron        
            n_object = (n_label_framedil==i)*1
            #dilate neuron by one pixel
            cell_dil = ndimage.binary_dilation(n_object)

            # cut neuron and ring image by 5 pixels around the neuron
            cellbounds = np.where(n_label_framedil==i)
            x_min = cellbounds[0].min()-5
            x_max = cellbounds[0].max()+5
            y_min = cellbounds[1].min()-5
            y_max = cellbounds[1].max()+5
            single_cell = cell_dil[x_min:x_max,y_min:y_max]

            ring = ringmask_dilated [x_min:x_max,y_min:y_max] 
                
            # find edges of neuron and overlap ring
            edges = segmentation.find_boundaries(single_cell, mode = "inner")
            n_border_px = edges.sum()
            overlap = (edges*1 + ring) == 2
            overlap_px = overlap.sum ()
                
            ring_touched = overlap_px/n_border_px

            rings.append(float (ring_touched))
        return rings
     
