import os
from PIL import Image

def degrade_image(img_path, output_path, quality=30):
    """
    Applies JPEG compression to simulate degradation.
    """
    with Image.open(img_path) as img:
        img = img.convert('RGB')
        img.save(output_path, 'JPEG', quality=quality)
        
def create_degraded_dataset(manifest_path, output_dir, degrade_quality=30):
    import csv
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    out_manifest = os.path.join(output_dir, 'manifest.csv')
    base_dir = os.path.dirname(manifest_path)
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        with open(out_manifest, 'w', encoding='utf-8', newline='') as out_f:
            writer = csv.DictWriter(out_f, fieldnames=['image_path', 'label'])
            writer.writeheader()
            
            for row in reader:
                img_rel = row.get('image_path')
                label = row.get('label')
                
                src = os.path.join(base_dir, img_rel)
                if not os.path.exists(src):
                    continue
                    
                dst_name = f"degraded_{os.path.basename(src)}"
                dst_rel = dst_name
                dst_full = os.path.join(output_dir, dst_name)
                
                degrade_image(src, dst_full, degrade_quality)
                
                writer.writerow({
                    'image_path': dst_rel,
                    'label': label
                })

if __name__ == '__main__':
    print("Use this module to generate degraded versions of test datasets.")
