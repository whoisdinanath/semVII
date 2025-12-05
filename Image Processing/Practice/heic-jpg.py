import os
from PIL import Image
from pillow_heif import register_heif_opener


# set quality argument as needed, input folder will be current directory if left blank, output folder will be 'converted_images' in current directory if left blank
def convert_heic_to_jpeg(input_folder, output_folder, quality=95):
    # register heif opener to handle heic files
    register_heif_opener()
    
    # validate input folder
    if not os.path.exists(input_folder):
        print(f"error: input folder '{input_folder}' does not exist")
        return
    
    # create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # get all heic files from input folder
    heic_extensions = ['.heic', '.heif']
    heic_files = [f for f in os.listdir(input_folder) 
                  if any(f.lower().endswith(ext) for ext in heic_extensions)]
    
    if not heic_files:
        print("no heic/heif files found")
        return
    
    converted_count = 0
    for heic_file in heic_files:
        try:
            # open heic image
            heic_path = os.path.join(input_folder, heic_file)
            with Image.open(heic_path) as image:
                # convert to rgb if needed
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # create output filename with .jpg extension
                jpeg_filename = os.path.splitext(heic_file)[0] + '.jpg'
                jpeg_path = os.path.join(output_folder, jpeg_filename)
                
                # save as jpeg
                image.save(jpeg_path, 'JPEG', quality=quality, optimize=True)
                converted_count += 1
                
        except Exception as e:
            print(f"error converting {heic_file}: {str(e)}")
    
    print(f"converted {converted_count}/{len(heic_files)} files")

def main():
    input_folder = input("input folder path (or press enter for current directory): ").strip()
    if not input_folder:
        input_folder = os.getcwd()
    
    output_folder = input("output folder path (or press enter for 'converted_images'): ").strip()
    if not output_folder:
        output_folder = os.path.join(os.getcwd(), "converted_images")
    
    quality = input("jpeg quality (1-100, or press enter for 95): ").strip()
    if quality:
        try:
            quality = int(quality)
            if not 1 <= quality <= 100:
                quality = 95
        except ValueError:
            quality = 95
    else:
        quality = 95
    
    convert_heic_to_jpeg(input_folder, output_folder, quality)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\noperation cancelled")
    except Exception as e:
        print(f"error: {str(e)}")
