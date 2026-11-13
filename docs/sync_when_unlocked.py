import shutil
import time

src = "docs/NewsScope_Presentation_CruxTemplate.pptx"
dst = "docs/NewsScope_Presentation.pptx"

def try_copy():
    try:
        shutil.copy2(src, dst)
        print("SUCCESS: Copied pristine CruxTemplate to NewsScope_Presentation.pptx!")
        return True
    except PermissionError:
        print("LOCKED: PowerPoint is currently holding NewsScope_Presentation.pptx open.")
        return False
    except Exception as e:
        print("ERROR:", e)
        return False

if __name__ == "__main__":
    try_copy()
