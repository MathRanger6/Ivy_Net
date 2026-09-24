import os
import sys
import time
import shutil
import subprocess
from pptx import Presentation
from pptx.util import Inches
from pdf2image import convert_from_path

def flatten_presentation(input_path):
    # Resolve the incoming file path safely
    abs_input_path = os.path.abspath(os.path.expanduser(input_path))
    if not os.path.exists(abs_input_path):
        print(f"❌ Error: File not found at '{abs_input_path}'")
        return

    filename = os.path.basename(abs_input_path)
    name_no_ext, ext = os.path.splitext(filename)
    
    # Save a temporary working file to your local Desktop
    desktop_dir = os.path.expanduser("~/Desktop")
    temp_output_path = os.path.join(desktop_dir, f"{name_no_ext}_FLATTENED_UNSAVED{ext}")

    # Build a strictly local sandbox directory right on your Desktop
    desktop_temp_dir = os.path.join(desktop_dir, f"temp_flatten_{int(time.time())}")
    os.makedirs(desktop_temp_dir, exist_ok=True)
    
    local_pptx = os.path.join(desktop_temp_dir, filename)
    pdf_path = os.path.join(desktop_temp_dir, f"{name_no_ext}.pdf")

    print("📋 Copying presentation to local Desktop temporary directory...")
    shutil.copy2(abs_input_path, local_pptx)

    # Note: Because we are skipping automated saving, we'll try a native 
    # Python-based format mapping block if available, or fall back to an open request.
    print("🍏 Step 1: Reading presentation layout mapping...")
    orig_prs = Presentation(local_pptx)
    width = orig_prs.slide_width if orig_prs.slide_width else Inches(13.333)
    height = orig_prs.slide_height if orig_prs.slide_height else Inches(7.5)

    print("🚀 Step 2: Launching file visualization layout...")
    # Open the file up normally so the user can interactively print or save a copy to PDF
    subprocess.run(["open", "-a", "Microsoft PowerPoint", local_pptx], check=True)
    
    print("\n💡 MANUAL ACTION REQUIRED:")
    print("   1. PowerPoint has just opened your presentation.")
    print("   2. In PowerPoint, click: File -> Save As...")
    print("   3. Change the File Format dropdown to 'PDF'.")
    print(f"   4. Name it exactly: {name_no_ext}.pdf")
    print(f"   5. Save it into this temporary folder: {desktop_temp_dir}")
    print("\n⏳ Script is waiting for you to save that PDF... (Press Enter in this terminal window when done)")
    
    input() # Wait for user to manually create the file inside the desktop temp sandbox

    if not os.path.exists(pdf_path):
        print(f"❌ Error: Could not find the manually saved PDF at: {pdf_path}")
        print("Please ensure the filename and temporary folder location match exactly.")
        shutil.rmtree(desktop_temp_dir, ignore_errors=True)
        return

    print("📸 Step 3: Breaking PDF apart into static slide images...")
    images = convert_from_path(pdf_path, dpi=150)

    print("🐍 Step 4: Generating clean flattened presentation file...")
    new_prs = Presentation()
    new_prs.slide_width = width
    new_prs.slide_height = height
    blank_layout = new_prs.slide_layouts

    for i, img in enumerate(images):
        print(f"  🖼️  Locking down slide {i+1}...")
        img_path = os.path.join(desktop_temp_dir, f"slide_{i}.png")
        img.save(img_path, "PNG")
        
        slide = new_prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(img_path, 0, 0, width=new_prs.slide_width, height=new_prs.slide_height)

    new_prs.save(temp_output_path)
    
    # Clean up local temporary folder assets entirely
    shutil.rmtree(desktop_temp_dir, ignore_errors=True)

    print(f"\n🎉 Step 5: Opening your newly flattened presentation file!")
    print("➡️  Make sure to manually press Command+S (Save) inside PowerPoint to keep it permanently.")
    subprocess.run(["open", "-a", "Microsoft PowerPoint", temp_output_path])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python flatten.py <path_to_presentation.pptx>")
        sys.exit(1)
        
    flatten_presentation(sys.argv[1])