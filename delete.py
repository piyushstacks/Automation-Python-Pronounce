import os

def delete_files_except_target(folder_path, target_words):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Iterate through each file
    for file in files:
        file_path = os.path.join(folder_path, file)
        
        # Check if any of the target words are in the filename
        if any(word in file for word in target_words):
            print(f"Keeping file: {file}")
        else:
            # Delete the file if none of the target words are in the filename
            try:
                os.remove(file_path)
                print(f"Deleted file: {file}")
            except Exception as e:
                print(f"Error deleting file {file}: {e}")

# Example usage:
folder_path = 'D:\Content\YOUTUBE\Shorts\Learnthislang\Automation\pronunciations'  # Replace with your folder path
target_words = ['combined', '.csv']  # Replace with your specific target words
delete_files_except_target(folder_path, target_words)
