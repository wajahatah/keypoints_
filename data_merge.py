import json
import os

def load_coco_json(json_path):
    """Load a single COCO dataset from a JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)

def update_ids(dataset, image_offset, annotation_offset):
    """Update image and annotation IDs in a dataset to avoid conflicts."""
    for image in dataset['images']:
        image['id'] += image_offset

    for annotation in dataset['annotations']:
        annotation['id'] += annotation_offset
        annotation['image_id'] += image_offset

def merge_datasets(base_dataset, new_dataset):
    """Merge a new dataset into the base dataset, ensuring ID uniqueness."""
    # Calculate the offset for image and annotation IDs
    image_offset = max([img['id'] for img in base_dataset['images']]) + 1
    annotation_offset = max([ann['id'] for ann in base_dataset['annotations']]) + 1

    # Update IDs in the new dataset
    update_ids(new_dataset, image_offset, annotation_offset)

    # Append images and annotations
    base_dataset['images'].extend(new_dataset['images'])
    base_dataset['annotations'].extend(new_dataset['annotations'])

    # Merge categories: Ensure categories are consistent
    category_mapping = {}
    max_cat_id = max(cat['id'] for cat in base_dataset['categories'])
    
    for new_cat in new_dataset['categories']:
        # Check if the category exists in the base dataset
        existing_cat = next((cat for cat in base_dataset['categories'] if cat['name'] == new_cat['name']), None)
        if existing_cat:
            category_mapping[new_cat['id']] = existing_cat['id']
        else:
            max_cat_id += 1
            new_cat['id'] = max_cat_id
            category_mapping[new_cat['id']] = max_cat_id
            base_dataset['categories'].append(new_cat)

    # Update category IDs in annotations
    for ann in new_dataset['annotations']:
        ann['category_id'] = category_mapping[ann['category_id']]

def save_coco_json(output_path, dataset):
    """Save the merged dataset to a JSON file."""
    with open(output_path, 'w') as f:
        json.dump(dataset, f)

# Paths to your 7-8 COCO dataset JSON files
json_files = [
    "C:/Users/LAMBDA THETA/Downloads/b5_1/annotations/person_keypoints_default.json",
    "C:/Users/LAMBDA THETA/Downloads/b5_7/annotations/person_keypoints_default.json",
    "C:/Users/LAMBDA THETA/Downloads/b5_6/annotations/person_keypoints_default.json",
    "C:/Users/LAMBDA THETA/Downloads/b5_5/annotations/person_keypoints_default.json",
    "C:/Users/LAMBDA THETA/Downloads/b5_4/annotations/person_keypoints_default.json",
    "C:/Users/LAMBDA THETA/Downloads/b5_2/annotations/person_keypoints_default.json"
    # Add all paths
]

# Load the first dataset as the base
merged_dataset = load_coco_json(json_files[0])

# Iteratively merge other datasets
for json_path in json_files[1:]:
    new_dataset = load_coco_json(json_path)
    merge_datasets(merged_dataset, new_dataset)

# Save the merged dataset
save_coco_json("C:/Users/LAMBDA THETA/Downloads/merged1_data.json", merged_dataset)
