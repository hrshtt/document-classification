import requests
from collections import namedtuple
from math import *

Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
API_URL = ''

# filepath = '/home/hrshtt/Documents/Data/doc_class_dataset/all_invoices/Hide-Shipping-Charge-DHL-Shipping-Label-Commercial-Invoice-With-Rate.png' 
filepath = '/home/hrshtt/Documents/Data/doc_class_dataset/all_invoices/9636.PDF' 


def mean_var_sigma(a):
    N = len(a)
    mean = sum(a)/N
    var = sum(map(lambda x:(x-mean)**2, a))/N
    sig = sqrt(var)
    return mean, var, sig

def percentage_area_overlap(a, b, arg=0): # returns None if rectangles don't intersect
    area_a = (a.xmax - a.xmin) * (a.ymax - a.ymin)
    area_b = (b.xmax - b.xmin) * (b.ymax - b.ymin)
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if dx>=0 and dy>=0:
        if arg == 0:
            return dx*dy/max(area_a, area_b)
        elif arg == 3:
            return dx*dy/min(area_a, area_b)
        elif arg == 1:
            return dx*dy/area_a
        return dx*dy/area_b
    else:
        return(0)

def calc_font_size( vision_text_seeds, table=None):
    seeds_height = []
    thead_seeds = []
    # seed_val
    # area_overlap, mean_word_height, _, sd
    if table:
        ra = Rectangle(table['bbox'][0], table['bbox'][1], table['bbox'][2], table['bbox'][3])
        for seed_val in vision_text_seeds:
            rb = Rectangle(seed_val[0][0], seed_val[0][1], seed_val[0][2], seed_val[0][3])
            area_overlap = percentage_area_overlap(ra, rb, 2)
            if area_overlap is not None and area_overlap > 0.70:
                seeds_height.append(seed_val[0][3]-seed_val[0][1])
                thead_seeds.append(seed_val)
    #     print(thead_seeds)
        print(seeds_height)
        mean_word_height, _, sd = mean_var_sigma(seeds_height)
        print(mean_word_height)
        return mean_word_height, thead_seeds, sd
        
    else:
        for seed_val in vision_text_seeds:
            seeds_height.append(seed_val[0][3]-seed_val[0][1])
        mean_word_height, _, sd = mean_var_sigma(seeds_height)
        return mean_word_height, sd

def smoothen_vision_seeds(sorted_vision_seeds):
    #print(f"sorted_vision_seeds = {sorted_vision_seeds}")
    font_size, _ = calc_font_size(sorted_vision_seeds)
    threshold = ceil(font_size/2) if ceil(font_size/2) > 4 else 4 # if it fails, try  adding sigma value to font_size
    for idx in range(1,len(sorted_vision_seeds)):
        if abs((sorted_vision_seeds[idx][0][1] + sorted_vision_seeds[idx][0][3])/2 - (sorted_vision_seeds[idx-1][0][1] + sorted_vision_seeds[idx-1][0][3])/2) <= threshold:
            sorted_vision_seeds[idx][0][1] = sorted_vision_seeds[idx-1][0][1]
            sorted_vision_seeds[idx][0][3] = sorted_vision_seeds[idx-1][0][3]
    return sorted(sorted_vision_seeds, key= lambda x: (x[0][1], x[0][0]))

with open(filepath, 'rb')as f:
    file_ = f.read()
    print("Sending request")
    ocr_result = requests.post(API_URL, files={"file" : file_})
    if ocr_result.status_code==200:
        print("success")
        output = []
        ocr_result = ocr_result.json()['ocr']
        if filepath.lower().endswith('.pdf'):
            output = ocr_result
        else:
            output.append(ocr_result)
        for page in output:
            page.sort(key= lambda x: (x[0][1], x[0][0]))
            doc_text = ' '.join(i[1] for i in page)
            print(f"doc_text : {doc_text}")
    else:
        print('ocr down')