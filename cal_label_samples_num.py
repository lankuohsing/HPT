#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 16:00:28 2024

@author: guoxing.lan
"""

label_to_num={
    '''
	"Root": {
		"CS": 0,
		"Medical": 0,
		"Civil": 0,
		"ECE": 0,
		"biochemistry": 0,
		"MAE": 0,
		"Psychology": 0
	},'''
	"CS": {
		"Symbolic computation": 402,
		"Computer vision": 432,
		"Computer graphics": 412,
		"Operating systems": 380,
		"Machine learning": 398,
		"Data structures": 392,
		"network security": 445,
		"Image processing": 415,
		"Parallel computing": 443,
		"Distributed computing": 403,
		"Algorithm design": 379,
		"Computer programming": 425,
		"Relational databases": 377,
		"Software engineering": 416,
		"Bioinformatics": 365,
		"Cryptography": 387,
		"Structured Storage": 43
	},
	"Medical": {
		"Alzheimer\'s Disease": 368,
		"Parkinson\'s Disease": 298,
		"Sprains and Strains": 142,
		"Cancer": 359,
		"Sports Injuries": 365,
		"Senior Health": 118,
		"Multiple Sclerosis": 253,
		"Hepatitis C": 288,
		"Weight Loss": 327,
		"Low Testosterone": 305,
		"Fungal Infection": 372,
		"Diabetes": 353,
		"Parenting": 343,
		"Birth Control": 335,
		"Heart Disease": 291,
		"Allergies": 357,
		"Menopause": 371,
		"Emergency Contraception": 291,
		"Skin Care": 339,
		"Myelofibrosis": 198,
		"Hypothyroidism": 315,
		"Headache": 341,
		"Overactive Bladder": 340,
		"Irritable Bowel Syndrome": 336,
		"Polycythemia Vera": 148,
		"Atrial Fibrillation": 294,
		"Smoking Cessation": 257,
		"Lymphoma": 267,
		"Asthma": 317,
		"Bipolar Disorder": 260,
		"Crohn\'s Disease": 198,
		"Idiopathic Pulmonary Fibrosis": 246,
		"Mental Health": 222,
		"Dementia": 237,
		"Rheumatoid Arthritis": 188,
		"Osteoporosis": 320,
		"Medicare": 255,
		"Psoriatic Arthritis": 202,
		"Addiction": 309,
		"Atopic Dermatitis": 262,
		"Digestive Health": 95,
		"Healthy Sleep": 129,
		"Anxiety": 262,
		"Psoriasis": 128,
		"Ankylosing Spondylitis": 321,
		"Children\'s Health": 350,
		"Stress Management": 361,
		"HIV/AIDS": 358,
		"Depression": 130,
		"Migraine": 178,
		"Osteoarthritis": 305,
		"Hereditary Angioedema": 182,
		"Kidney Health": 90,
		"Autism": 309,
		"Schizophrenia": 38,
		"Outdoor Health": 2
	},
	"Civil": {
		"Green Building": 418,
		"Water Pollution": 446,
		"Smart Material": 363,
		"Ambient Intelligence": 410,
		"Construction Management": 412,
		"Suspension Bridge": 395,
		"Geotextile": 419,
		"Stealth Technology": 148,
		"Solar Energy": 384,
		"Remote Sensing": 384,
		"Rainwater Harvesting": 441,
		"Transparent Concrete": 3,
		"Highway Network System": 4,
		"Nano Concrete": 7,
		"Bamboo as a Building Material": 2,
		"Underwater Windmill": 1
	},
	"ECE": {
		"Electric motor": 372,
		"Satellite radio": 148,
		"Digital control": 426,
		"Microcontroller": 413,
		"Electrical network": 392,
		"Electrical generator": 240,
		"Electricity": 447,
		"Operational amplifier": 419,
		"Analog signal processing": 407,
		"State space representation": 344,
		"Signal-flow graph": 274,
		"Electrical circuits": 375,
		"Lorentz force law": 44,
		"System identification": 417,
		"PID controller": 429,
		"Voltage law": 54,
		"Control engineering": 276,
		"Single-phase electric power": 6
	},
	"biochemistry": {
		"Molecular biology": 746,
		"Enzymology": 576,
		"Southern blotting": 510,
		"Northern blotting": 699,
		"Human Metabolism": 622,
		"Polymerase chain reaction": 750,
		"Immunology": 652,
		"Genetics": 566,
		"Cell biology": 552,
		"DNA/RNA sequencing": 14
	},
	"MAE": {
		"Fluid mechanics": 386,
		"Hydraulics": 402,
		"computer-aided design": 371,
		"Manufacturing engineering": 346,
		"Machine design": 420,
		"Thermodynamics": 361,
		"Materials Engineering": 289,
		"Strength of materials": 335,
		"Internal combustion engine": 387
	},
	"Psychology": {
		"Prenatal development": 389,
		"Attention": 416,
		"Eating disorders": 387,
		"Borderline personality disorder": 376,
		"Prosocial behavior": 388,
		"False memories": 362,
		"Problem-solving": 360,
		"Prejudice": 389,
		"Antisocial personality disorder": 368,
		"Nonverbal communication": 394,
		"Leadership": 350,
		"Child abuse": 404,
		"Gender roles": 395,
		"Depression": 380,
		"Social cognition": 397,
		"Seasonal affective disorder": 365,
		"Person perception": 391,
		"Media violence": 296,
		"Schizophrenia": 335
	}
}


num_of_samples=0
list_second=[]
num_of_labels=0
for parent_label, children_labels in label_to_num.items():
    for child_label, num in children_labels.items():
        num_of_samples+=num
        num_of_labels+=1
        if child_label in list_second:
            print(child_label)
        list_second.append(child_label)
#list_second有145个，去重后143个
# In[]


# In[]
a=['Electric motor', 'Satellite radio', 'Single-phase electric power', 'Water Pollution', 'Bamboo as a Building Material', 'Underwater Windmill', 'Cell biology', 'DNA/RNA sequencing', 'Smart Material', 'Transparent Concrete', 'Nano Concrete', 'Electrical generator', 'Analog signal processing', 'Geotextile', 'Highway Network System', 'Atrial Fibrillation', 'Depression', 'Bipolar Disorder', 'Schizophrenia', 'Digestive Health', 'Outdoor Health']
print(len(a))
print(len(set(a)))



# In[]
#从Excel中获取的area列的label，去重后143个，去重前145个，Depression和Schizophrenia都同时存在于Medical和Psychology两个父标签下面
all_children_from_excel=["Symbolic computation","Alzheimer's Disease","Green Building","Electric motor","Parkinson's Disease","Computer vision","Molecular biology","Satellite radio","Fluid mechanics","Prenatal development","Sprains and Strains","Enzymology","Southern blotting","Cancer","Northern blotting","Sports Injuries","Senior Health","Computer graphics","Digital control","Human Metabolism","Polymerase chain reaction","Multiple Sclerosis","Operating systems","Microcontroller","Attention","Immunology","Genetics","Water Pollution","Hydraulics","Hepatitis C","Weight Loss","Machine learning","Low Testosterone","Fungal Infection","Diabetes","Data structures","Cell biology","Parenting","Birth Control","Smart Material","network security","Heart Disease","computer-aided design","Image processing","Parallel computing","Ambient Intelligence","Allergies","Menopause","Emergency Contraception","Electrical network","Construction Management","Distributed computing","Electrical generator","Electricity","Operational amplifier","Manufacturing engineering","Analog signal processing","Skin Care","Eating disorders","Myelofibrosis","Suspension Bridge","Machine design","Hypothyroidism","Headache","Overactive Bladder","Geotextile","Irritable Bowel Syndrome","Polycythemia Vera","Atrial Fibrillation","Smoking Cessation","Lymphoma","Thermodynamics","Asthma","State space representation","Bipolar Disorder","Materials Engineering","Stealth Technology","Solar Energy","Signal-flow graph","Crohn's Disease","Borderline personality disorder","Prosocial behavior","False memories","Idiopathic Pulmonary Fibrosis","Electrical circuits","Algorithm design","Strength of materials","Problem-solving","Internal combustion engine","Lorentz force law","Prejudice","Antisocial personality disorder","System identification","Computer programming","Nonverbal communication","Relational databases","PID controller","Voltage law","Leadership","Child abuse","Mental Health","Dementia","Rheumatoid Arthritis","Osteoporosis","Software engineering","Bioinformatics","Medicare","Control engineering","Psoriatic Arthritis","Addiction","Atopic Dermatitis","Digestive Health","Remote Sensing","Gender roles","Rainwater Harvesting","Healthy Sleep","Depression","Social cognition","Anxiety","Cryptography","Psoriasis","Ankylosing Spondylitis","Children's Health","Stress Management","Seasonal affective disorder","HIV/AIDS","Migraine","Person perception","Osteoarthritis","Hereditary Angioedema","Media violence","Schizophrenia","Kidney Health","Autism","Transparent Concrete","Highway Network System","DNA/RNA sequencing","Structured Storage","Nano Concrete","Outdoor Health","Single-phase electric power","Bamboo as a Building Material","Underwater Windmill"]
list_second=list(set(list_second))
set_child_label=['Fungal Infection', 'PID controller', 'State space representation', 'Digestive Health', 'Stealth Technology', 'Prosocial behavior', 'Kidney Health', 'Rheumatoid Arthritis', 'computer-aided design', 'Hypothyroidism', "Crohn's Disease", 'Headache', 'Construction Management', 'Materials Engineering', 'Prejudice', 'Digital control', 'Operating systems', 'Ambient Intelligence', 'Idiopathic Pulmonary Fibrosis', 'Lorentz force law', 'System identification', 'Eating disorders', 'Low Testosterone', 'Mental Health', 'Emergency Contraception', 'Weight Loss', 'Irritable Bowel Syndrome', 'Voltage law', 'Gender roles', 'Electric motor', 'Skin Care', 'Cancer', 'Polymerase chain reaction', 'Sprains and Strains', 'Menopause', 'Medicare', 'Northern blotting', 'Human Metabolism', 'Heart Disease', 'Senior Health', 'Borderline personality disorder', 'Analog signal processing', 'Migraine', 'Internal combustion engine', 'Microcontroller', 'Atopic Dermatitis', 'Immunology', 'Enzymology', 'Depression', 'Attention', 'Electricity', 'Person perception', 'Control engineering', 'Image processing', 'Signal-flow graph', 'Psoriasis', 'Suspension Bridge', 'Algorithm design', 'Green Building', 'Problem-solving', 'Anxiety', 'Cell biology', 'Computer vision', 'Symbolic computation', 'Media violence', 'Psoriatic Arthritis', 'Smoking Cessation', 'Diabetes', "Alzheimer's Disease", 'Structured Storage', 'Autism', 'Software engineering', 'Computer graphics', 'Stress Management', 'Osteoporosis', 'network security', 'Strength of materials', 'Child abuse', 'Healthy Sleep', 'Machine learning', 'Distributed computing', 'Nonverbal communication', "Children's Health", 'False memories', 'Manufacturing engineering', 'Bipolar Disorder', 'Myelofibrosis', 'Polycythemia Vera', 'Prenatal development', 'Seasonal affective disorder', 'Cryptography', 'Electrical generator', 'Southern blotting', 'Osteoarthritis', 'Smart Material', 'Allergies', 'Birth Control', 'Social cognition', 'Molecular biology', 'Rainwater Harvesting', 'Data structures', 'Leadership', 'Overactive Bladder', 'Schizophrenia', 'Remote Sensing', "Parkinson's Disease", 'Thermodynamics', 'Antisocial personality disorder', 'Relational databases', 'Sports Injuries', 'Electrical network', 'Machine design', 'Electrical circuits', 'Water Pollution', 'Parenting', 'Fluid mechanics', 'HIV/AIDS', 'Hepatitis C', 'Operational amplifier', 'Ankylosing Spondylitis', 'Bioinformatics', 'Atrial Fibrillation', 'Multiple Sclerosis', 'Computer programming', 'Genetics', 'Hereditary Angioedema', 'Geotextile', 'Dementia', 'Addiction', 'Lymphoma', 'Asthma', 'Solar Energy', 'Parallel computing', 'Hydraulics']
set(list_second).difference(set(set_child_label))

# In[]


all_children2=["Symbolic computation","Computer vision","Computer graphics","Operating systems","Machine learning","Data structures","network security","Image processing","Parallel computing","Distributed computing","Algorithm design","Computer programming","Relational databases","Software engineering","Bioinformatics","Cryptography","Structured Storage","Alzheimer's Disease","Parkinson's Disease","Sprains and Strains","Cancer","Sports Injuries","Senior Health","Multiple Sclerosis","Hepatitis C","Weight Loss","Low Testosterone","Fungal Infection","Diabetes","Parenting","Birth Control","Heart Disease","Allergies","Menopause","Emergency Contraception","Skin Care","Myelofibrosis","Hypothyroidism","Headache","Overactive Bladder","Irritable Bowel Syndrome","Polycythemia Vera","Atrial Fibrillation","Smoking Cessation","Lymphoma","Asthma","Bipolar Disorder","Crohn's Disease","Idiopathic Pulmonary Fibrosis","Mental Health","Dementia","Rheumatoid Arthritis","Osteoporosis","Medicare","Psoriatic Arthritis","Addiction","Atopic Dermatitis","Digestive Health","Healthy Sleep","Anxiety","Psoriasis","Ankylosing Spondylitis","Children's Health","Stress Management","HIV/AIDS","Migraine","Osteoarthritis","Hereditary Angioedema","Kidney Health","Autism","Green Building","Water Pollution","Smart Material","Ambient Intelligence","Construction Management","Suspension Bridge","Geotextile","Stealth Technology","Solar Energy","Remote Sensing","Rainwater Harvesting","Electric motor","Digital control","Microcontroller","Electrical network","Electrical generator","Electricity","Operational amplifier","Analog signal processing","State space representation","Signal-flow graph","Electrical circuits","Lorentz force law","System identification","PID controller","Voltage law","Control engineering","Molecular biology","Enzymology","Southern blotting","Northern blotting","Human Metabolism","Polymerase chain reaction","Immunology","Genetics","Cell biology","Fluid mechanics","Hydraulics","computer-aided design","Manufacturing engineering","Machine design","Thermodynamics","Materials Engineering","Strength of materials","Internal combustion engine","Prenatal development","Attention","Eating disorders","Borderline personality disorder","Prosocial behavior","False memories","Problem-solving","Prejudice","Antisocial personality disorder","Nonverbal communication","Leadership","Child abuse","Gender roles","Depression","Social cognition","Seasonal affective disorder","Person perception","Media violence","Schizophrenia"]



for label in all_children2:
    if label not in all_children_from_excel:
        print(label)


# In[]
redundant_labels=['Electric motor', 'Satellite radio', 'Single-phase electric power', 'Water Pollution', 'Bamboo as a Building Material', 'Underwater Windmill', 'Cell biology', 'DNA/RNA sequencing', 'Smart Material', 'Transparent Concrete', 'Nano Concrete', 'Electrical generator', 'Analog signal processing', 'Geotextile', 'Highway Network System', 'Atrial Fibrillation', 'Depression', 'Bipolar Disorder', 'Schizophrenia', 'Digestive Health', 'Outdoor Health']
for label in redundant_labels:
    if label not in all_children2:
        print(label)

# In[]
#从代码中获取的redundant_labels信息
redundant_labels2=['Transparent Concrete', 'Electrical generator', 'Single-phase electric power', 'Schizophrenia', 'Bamboo as a Building Material', 'Satellite radio', 'Depression', 'Nano Concrete', 'Underwater Windmill', 'Highway Network System', 'Outdoor Health', 'DNA/RNA sequencing']
for label in redundant_labels2:
    if label  in set_child_label:
        print(label)


# In[]
from collections import defaultdict


y1_to_y2=defaultdict(set)
y2_to_y1=defaultdict(set)
y1y2_to_y=defaultdict(set)
y_to_y1y2=defaultdict(set)
y1y2_to_parent_child=defaultdict(set)
y1_to_parent=defaultdict(set)
y2_to_children=defaultdict(set)
y_to_child=defaultdict(set)
child_to_y=defaultdict(set)
with open("/Users/guoxing.lan/projects/github/wo_en/HPT/data/WebOfScience/Meta-data/Data.txt",'r',encoding="UTF-8") as rf:
    for line in rf:
        split_list=line.strip().split("\t")
        assert len(split_list)==7
        y1=split_list[0]
        y2=split_list[1]
        Y=split_list[2]
        parent_label=split_list[3]
        child_label=split_list[4]
        y1_to_y2[y1].add(y2)
        y2_to_y1[y2].add(y1)
        y1y2_to_y[y1+"-"+y2].add(Y)
        y_to_y1y2[Y].add(y1+"-"+y2)
        y1y2_to_parent_child[y1+"-"+y2].add(parent_label+"-"+child_label)
        y2_to_children[y2].add(child_label)
        y_to_child[Y].add(child_label)
        child_to_y[child_label].add(Y)

# In[]
for y2,y1_set in y2_to_y1.items():
    if len(y1_set)>1:
        print(y2,y1_set)

# In[]
for y1y2,y_set in y1y2_to_y.items():
    if len(y_set)>1:
        print(y1y2,y_set)
# In[]
for y,y1y2_set in y_to_y1y2.items():
    if len(y1y2_set)>1:
        print(y,y1y2_set)

# In[]
for child,y_set in child_to_y.items():
    if len(y_set)>1:
        print(child,y_set)
# In[]
for y,child_set in y_to_child.items():
    if len(child_set)>1:
        print(f'''{y}: {child_set}''')
# In[]
import json
dict_redundant_id_to_label=defaultdict(list)
for y1y2, parent_child_set in y1y2_to_parent_child.items():
    if(len(parent_child_set))>1:
        dict_redundant_id_to_label[y1y2]=list(parent_child_set)

print(json.dumps(dict_redundant_id_to_label))
# In[]
a={1,2,3}
type(a)


for i in a:
    print(i)
