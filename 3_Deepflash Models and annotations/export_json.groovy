def imageData = QPEx.getCurrentImageData()
def server = imageData.getServer()

def export_dir = "C:/Work/Annotations/marker/mask_export/annotator_json" 
def fname = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())

def annotations = getAnnotationObjects()
boolean prettyPrint = true
def gson = GsonTools.getInstance(prettyPrint)
//println gson.toJson(annotations)

def name = String.format("%s/%s.json", export_dir, fname)
File file = new File(name)
file.withWriter('UTF-8') {
    gson.toJson(annotations, it)
}