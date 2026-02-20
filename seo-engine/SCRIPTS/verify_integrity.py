import re
import hashlib
import sys
import os

def get_skeleton_hash(file_path):
    """
    Extracts all content OUTSIDE of REGION tags and returns its SHA-256 hash.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find all text between START and END regions inclusive
    # We remove the content to leave the "skeleton"
    skeleton = re.sub(r'<!-- START:REGION:.*? -->.*?<!-- END:REGION:.*? -->', '[REGION]', content, flags=re.DOTALL)
    
    # Return hash of the skeleton
    return hashlib.sha256(skeleton.encode('utf-8')).hexdigest()

def verify_integrity(file_path, original_hash):
    """
    Verifies that the current skeleton hash matches the original hash.
    """
    current_hash = get_skeleton_hash(file_path)
    if current_hash == original_hash:
        print(f"✅ Integrity Verified: {file_path}")
        return True
    else:
        print(f"❌ INTEGRITY FAILURE: Skeleton of {file_path} has drifted!")
        print(f"Expected: {original_hash}")
        print(f"Actual:   {current_hash}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python verify_integrity.py <file_path> <original_hash>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    original_hash = sys.argv[2]
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
        
    if verify_integrity(file_path, original_hash):
        sys.exit(0)
    else:
        sys.exit(1)
