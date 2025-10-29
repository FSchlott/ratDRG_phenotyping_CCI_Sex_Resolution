import matplotlib.pyplot as plt
from skimage import measure
from tqdm.auto import tqdm
import os


class ImageData : 
    def __init__ (self, subdir):
        nfmask_paths = os.path.join(subdir, 'nf_pred/masks')
        ib4mask_paths = os.path.join(subdir, 'ib4_pred/masks')
        atf3mask_paths = os.path.join(subdir, 'atf3_pred/masks')

        self.nf_anz_L = []
        self.ib4_anz_L = []
        self.atf3_anz_L = []
        self.overlap_atf3_nf_anz_L = []
        self.overlap_atf3_ib4_anz_L = []
        self.overlap_nf_ib4_anz_L = []
        self.nf_sizes_L = []
        self.ib4_sizes_L = []
        self.atf3_sizes_L = []
        self.atf3_per_nf_L = []
        self.atf3_per_ib4_L = []
        self.ib4_per_nf_L = []
        self.ib4_per_atf3_L = []


        for nfM_filename , ib4M_filename , atf3M_filename in tqdm(zip(os.listdir(nfmask_paths), os.listdir(ib4mask_paths),
                                         os.listdir(atf3mask_paths))):
            nfM = plt.imread (os.path.join (nfmask_paths, nfM_filename))
            ib4M = plt.imread (os.path.join (ib4mask_paths, ib4M_filename))
            atf3M = plt.imread (os.path.join (atf3mask_paths, atf3M_filename))

            #get mask for the overlap of neuron labels
            overlapM_atf3_nf = self.get_overlapM (nfM, atf3M)
            overlapM_atf3_ib4 = self.get_overlapM (ib4M, atf3M)
            overlapM_nf_ib4 = self.get_overlapM (nfM, ib4M)

            #get labels numbers and sizes for each celltype and overlaps
            ib4_anz , ib4_sizes = self.get_cellnum_sizes (ib4M)
            atf3_anz , atf3_sizes = self.get_cellnum_sizes (atf3M)
            nf_anz , nf_sizes  = self.get_cellnum_sizes (nfM ) 
            overlap_atf3_nf_anz , overlap_atf3_nf_sizes  = self.get_cellnum_sizes (overlapM_atf3_nf)
            overlap_atf3_ib4_anz , overlap_atf3_ib4_sizes = self.get_cellnum_sizes (overlapM_atf3_ib4)
            overlap_nf_ib4_anz , overlap_nf_ib4_sizes = self.get_cellnum_sizes (overlapM_nf_ib4)
            atf3_per_ib4 , atf3_per_nf, ib4_per_nf, ib4_per_atf3 = self.get_percentages (nf_anz, ib4_anz, atf3_anz, overlap_atf3_ib4_anz, overlap_atf3_nf_anz, overlap_nf_ib4_anz)
           
            #append lists
            self.nf_anz_L.append (float (nf_anz))
            self.ib4_anz_L.append (float (ib4_anz))
            self.atf3_anz_L.append (float (atf3_anz))
            self.overlap_atf3_nf_anz_L.append (float (overlap_atf3_nf_anz))
            self.overlap_atf3_ib4_anz_L.append (float (overlap_atf3_ib4_anz))
            self.overlap_nf_ib4_anz_L.append (float (overlap_nf_ib4_anz))
            self.nf_sizes_L.append (nf_sizes)
            self.ib4_sizes_L.append (ib4_sizes)
            self.atf3_sizes_L.append (atf3_sizes)
            self.atf3_per_nf_L.append (atf3_per_nf)            
            self.atf3_per_ib4_L.append (atf3_per_ib4)
            self.ib4_per_nf_L.append (ib4_per_nf) 
            if ib4_per_nf > 0:
                self.ib4_per_atf3_L.append (ib4_per_atf3) 
                       
    #generates a mask for the overlap of two segmentations
    def get_overlapM (self, mask1 , mask2):
        addM = (mask1 + mask2)
        overlapM = (addM ==2)*1
        return overlapM

    def get_cellnum_sizes (self, mask):
        #get labels for neurons
        areas = []
        labels , anz = measure.label (mask , return_num = True)
        props = measure.regionprops (labels)
        #measure area in px per label  
        for i in range (anz): 
            areas.append (float(props[i].area)) 
        #remove values below small neuron size
        thr = 150 #threshold based on smallest annotated ib4+ cell 
        cell_L = [num for num in areas if num > thr] #new list with only cells above thr
        c_num = len (cell_L)
        return c_num , cell_L

    def get_percentages (self, nf_anz, ib4_anz, atf3_anz, overlap_atf3_ib4_anz, overlap_atf3_nf_anz, overlap_nf_ib4_anz):
        if nf_anz > 0: 
            atf3_per_ib4 = (overlap_atf3_ib4_anz / ib4_anz)*100
            atf3_per_nf = (overlap_atf3_nf_anz / nf_anz)*100
            ib4_per_nf = (overlap_nf_ib4_anz / nf_anz)*100
            if atf3_anz > 0:
                ib4_per_atf3 = (overlap_atf3_ib4_anz / atf3_anz)*100
            else: 
                ib4_per_atf3 = 0.0
        return atf3_per_ib4 , atf3_per_nf, ib4_per_nf, ib4_per_atf3

