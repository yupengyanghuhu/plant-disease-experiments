import os
import numpy as np
from keras.models import load_model
from PIL import Image
from keras.preprocessing import image
import subprocess
from keras.applications.inception_v3 import preprocess_input
import argparse
import sys

parser = argparse.ArgumentParser()

SPECIES = ['Apple','Bean','Blueberry','Cherry','Corn','Grape','Grapefruit','Orange','Peach','Pepper','Potato','Raspberry','Sorghum','Soybean','Squash','Strawberry','Sugarcane','Tomato']


APPLE = ['Apple___Apple_scab','Apple___Black_rot','Apple___Cedar_apple_rust','Apple___healthy']
CHERRY = ['Cherry_(including_sour)___Powdery_mildew','Cherry_(including_sour)___healthy']
CORN = ['Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot','Corn_(maize)___Common_rust_','Corn_(maize)___Northern_Leaf_Blight','Corn_(maize)___healthy']
GRAPE = ['Grape___Black_rot','Grape___Esca_(Black_Measles)','Grape___Leaf_blight_(Isariopsis_Leaf_Spot)','Grape___healthy']
PEACH = ['Peach___Bacterial_spot', 'Peach___healthy']
PEPPER = ['Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy']
POTATO = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
STRAWBERRY = ['Strawberry___Leaf_scorch', 'Strawberry___healthy']
SUGERCANE = ['Sugarcane leaf spot', 'Sugarcane aphid', 'Sugarcane coal fouling']
TOMATO = ['Tomato___Bacterial_spot','Tomato___Early_blight','Tomato___Late_blight','Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot','Tomato___Spider_mites Two-spotted_spider_mite',
        'Tomato___Target_Spot','Tomato___Tomato_Yellow_Leaf_Curl_Virus','Tomato___Tomato_mosaic_virus','Tomato___healthy']



target_size_disease = (64, 64)
target_size_specious = (100, 100)


def predict(img_path,do_print=True,model='VGG'):
    """
        given image path segment the image and predict specious on that image
    
    """
    image_name,extension=os.path.splitext(img_path)
    new_image = image_name+"_marked"+extension
    result = subprocess.check_output(['python', "leaf-image-segmentation/segment.py", "-s", img_path])
    model_path = os.path.join('Plant_Disease_Detection_Benchmark_models/Models', get_species_model())
    model = load_model(model_path)
    img = Image.open(new_image)
    if img.size != target_size_specious:
        img = img.resize(target_size_specious)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x).flatten()
    value_ = preds.argsort()
    value = value_[::-1]

    if do_print:
        print("Plant Species ")
        for i in value:
            print("\t - "+str(SPECIES[i])+" : \t"+str(preds[i]))

    return str(SPECIES[value[0]]),new_image


def predict_species(img_path,do_print=True,model='VGG'):
    """
        given the image predict the class on the raw image
    """
    model_path = os.path.join('Plant_Disease_Detection_Benchmark_models/Models', get_species_model())
    model = load_model(model_path)
    img = Image.open(img_path)
    if img.size != target_size_specious:
        img = img.resize(target_size_specious)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x).flatten()
    value_ = preds.argsort()
    value = value_[::-1]

    if do_print:
        print("Plant Species ")
        for i in value:
            print("\t - "+str(SPECIES[i])+" : \t"+str(preds[i]))

    return str(SPECIES[value[0]])
    

def predict_disease(img_path,species,do_print=True,model='VGG'):
    """
       given image do disease prediction on that image 
    """
    try:
        CLASS_ARRAY = get_class(species)
        model_path = os.path.join('Plant_Disease_Detection_Benchmark_models/Models', get_disease_model(species))
    except:
        print ('NO Disease Found For This Species')
        return 0

    model = load_model(model_path)
    img = Image.open(img_path)
    if img.size != target_size_disease:
        img = img.resize(target_size_disease)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x).flatten()
    value_ = preds.argsort()
    value = value_[::-1]

    if do_print:
        print("Plant Disease : ")
        for i in value:
            print("\t-"+str(CLASS_ARRAY[i])+" : \t"+str(preds[i]))

    return str(CLASS_ARRAY[value[0]])


def get_disease_model(x,model='VGG'):
    '''
         x : species name
         model : which trained model VGG or Inception_V3
    '''

    if model == 'VGG':
        return {
            'Apple':'Apple_0.9395_VGG.h5',
            'Cherry':'Cherry_0.9873_VGG.h5',
            'Corn':'Corn_0.8926_VGG.h5',
            'Grape':'Grape_0.9293_VGG.h5',
            'Peach':'Peach_97_VGG.h5',
            'Tomato':'Tomato_0.8675_VGG.h5',
            'Pepper':'pepper_95.90.h5',
            'Potato':'potato_90.62.h5',
            'Strawberry':'starwberry_99.h5',
            'Sugarcane':'Sugarcane_0.8356_VGG.h5'
            }[x]
    elif model == 'Inception_v3':
        return {
            'Apple':'InceptionV3-scratch_segApple.h5 ',
            'Cherry':'InceptionV3-scratch_segCherry.h5',
            'Corn':'InceptionV3-scratch_segCorn.h5 ',
            'Grape':'InceptionV3-scratch_segGrape.h5 ',
            'Peach':'InceptionV3-scratch_segPeach.h5 ',
            'Tomato':'InceptionV3-scratch_segTomato.h5 ',
            'Pepper':'InceptionV3-scratch_segPepper.h5 ',
            'Potato':'InceptionV3-scratch_segPotato.h5 ',
            'Strawberry':'InceptionV3-scratch_segStrawberry.h5 ',
            'Sugarcane':'InceptionV3-scratch_segSugarcane.h5 '
            }[x]


def get_species_model(model='VGG'):
    '''
         x : species name
         model : which trained model VGG or Inception_V3
    '''

    if model == 'VGG':
        return 'VGG_all_100p_94.h5'
    elif model == 'Inception_v3':
        target_size_disease = (64, 64)
        return 'InceptionV3-scratch_segspecies.h5'



def get_class(x):
    return{
        'Apple' : APPLE,
        'Cherry' : CHERRY,
        'Corn' : CORN,
        'Grape' : GRAPE,
        'Peach' : PEACH,
        'Pepper' : PEPPER,
        'Potato' : POTATO,
        'Strawberry' : STRAWBERRY,
        'Sugarcane' : SUGERCANE,
        'Tomato' : TOMATO,
        }[x]




if __name__ == "__main__":
    parser.add_argument("--image",type=str,help='image path')
    parser.add_argument("--segment",type=bool,default=False,help='add segmentation')
    parser.add_argument("--species",type=str,default='',help='Specious Name if Known')
    parser.add_argument('--model',default='VGG',choices=['VGG','Inception_v3'],help='choose  VGG or Inception_v3')

    args = parser.parse_args()

    # Checking input and printing help 
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
        


    # if not segment and species is not known
    if False ==args.segment and args.species == '':
        species = predict_species(args.image,args.model)
        predict_disease(args.image,species,args.model)

    # if segment and species is not known     
    elif True == args.segment and args.species == '':
        species,image_name = predict(args.image,args.model)
        predict_disease(image_name,species)

    #if segment and species is given
    elif True == args.segment and args.species != '' :
        species,image_name = predict(args.image,False,args.model)
        predict_disease(image_name,species,args.model)

    #if not segment and species is given
    elif False == args.segment and args.species != '' :
        predict_disease(args.image,args.species,args.model)

    # should not enter here
    else:
        Print("Make Sure Your Command is Correct")


    



