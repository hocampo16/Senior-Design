def cleanup_old_photos(folder_path, max_files=30, extension=".jpg"):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(extension)]
    files.sort(key=os.path.getctime)  # Sort by creation time (oldest first)

    while len(files) > max_files:
        os.remove(files[0])
        files.pop(0)

# put like this after every saved function 
cleanup_old_photos("nir_photos", 30, ".jpg")
cleanup_old_photos("red_photos", 30, ".jpg")
cleanup_old_photos("NDVI_results", 30, ".jpg")
cleanup_old_photos(output_folder, 30, ".jpg")
