import os
import re
import json
import sys
import hashlib
from verify_integrity import get_skeleton_hash, verify_integrity

REGISTRY_PATH = "seo-engine/REGISTRY.json"

def reinforce(slug, region_id, new_content):
    """
    Surgically injects new content into a specific region of a page.
    """
    if not os.path.exists(REGISTRY_PATH):
        print("❌ Error: Registry not found.")
        return False

    with open(REGISTRY_PATH, 'r') as f:
        registry = json.load(f)

    page = next((p for p in registry['pages'] if p['slug'] == slug), None)
    if not page:
        print(f"❌ Error: Slug '{slug}' not found in registry.")
        return False

    file_path = page['url'].lstrip('/') + 'index.html'
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found.")
        return False

    # 1. Load current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. Verify pre-injection integrity
    print(f"🔍 Verifying pre-injection integrity for {slug}...")
    if not verify_integrity(file_path, page['skeleton_hash']):
        print("❌ ABORTING: Pre-injection integrity check failed.")
        return False

    # 3. Perform surgical replacement
    # Regex targets: <!-- START:REGION:ID -->...<!-- END:REGION:ID -->
    pattern = rf'(<!-- START:REGION:{region_id} -->)(.*?)(<!-- END:REGION:{region_id} -->)'
    match = re.search(pattern, content, flags=re.DOTALL)
    
    if not match:
        print(f"❌ Error: Region '{region_id}' not found in {file_path}")
        return False

    header = match.group(1)
    current_inner = match.group(2)
    footer = match.group(3)

    # 4. Determine Substitution Strategy
    if region_id in ['BODY', 'FAQ']:
        # APPEND MODE: Additive growth
        print(f"➕ Mode: APPEND for {region_id}")
        # If it's FAQ, we might need to inject inside a wrapper if it exists
        if region_id == 'FAQ' and 'class="faq-section"' in current_inner:
            # Injecting before the closing div of the section
            new_inner = re.sub(r'(</div>\s*)$', f'\n{new_content}\n\\1', current_inner, flags=re.DOTALL)
        else:
            new_inner = current_inner.rstrip() + "\n\n" + new_content + "\n"
    elif region_id == 'HEAD':
        # SURGICAL HEAD: Replace title/meta but protect canonical/schema
        print(f"🎯 Mode: SURGICAL UPDATE for {region_id}")
        new_inner = "\n    " + new_content.strip() + "\n"
    elif region_id == 'INTENT':
        # SURGICAL INTENT: Replace H1/Intro
        print(f"🎯 Mode: SURGICAL UPDATE for {region_id}")
        new_inner = "\n    " + new_content.strip() + "\n"
    else:
        # Default: Replace wholesale (if unexpected ID)
        print(f"⚠️ Mode: DEFAULT REPLACE for {region_id}")
        new_inner = "\n" + new_content + "\n"

    new_html = content[:match.start()] + header + new_inner + footer + content[match.end():]

    # 5. Verify post-injection hash (in-memory)
    # We calculate the hash of the NEW html to ensure the skeleton is still exactly the same
    temp_skeleton = re.sub(r'<!-- START:REGION:.*? -->.*?<!-- END:REGION:.*? -->', '[REGION]', new_html, flags=re.DOTALL)
    new_hash = hashlib.sha256(temp_skeleton.encode('utf-8')).hexdigest()

    if new_hash != page['skeleton_hash']:
        print("❌ CRITICAL ERROR: Post-injection skeleton hash drift detected!")
        print(f"Expected: {page['skeleton_hash']}")
        print(f"Got:      {new_hash}")
        return False

    # 6. Write to disk
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"✅ SUCCESS: Surgically reinforced {region_id} region in {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python surgical_reinforce.py <slug> <region_id> <content_file_or_string>")
        sys.exit(1)

    slug = sys.argv[1]
    region_id = sys.argv[2]
    content_input = sys.argv[3]

    if os.path.exists(content_input):
        with open(content_input, 'r') as f:
            new_content = f.read().strip()
    else:
        new_content = content_input.strip()

    if reinforce(slug, region_id, new_content):
        sys.exit(0)
    else:
        sys.exit(1)
