import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import webbrowser

# ============================================================
# CONFIGURATION
# ============================================================

# IMPORTANT: Configure the path to your vpype installation
# 
# Default path (Windows with Python from Microsoft Store):
# C:\Users\YourUsername\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.XX_xxxxx\LocalCache\local-packages\PythonXXX\Scripts\vpype.exe
#
# To find your vpype path:
# 1. Open Command Prompt or PowerShell
# 2. Type: where vpype
# 3. Copy the full path shown and paste it below
#
# Or if installed via pip, it might be in:
# - C:\Python3XX\Scripts\vpype.exe
# - C:\Users\YourUsername\AppData\Roaming\Python\PythonXXX\Scripts\vpype.exe
#
# Linux/Mac users: use the full path from 'which vpype' command
# Example for Linux: /usr/local/bin/vpype
# Example for Mac: /usr/local/bin/vpype or /opt/homebrew/bin/vpype

VPYPE_CMD = r"C:\Users\PC\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\vpype.exe"

# ============================================================
# GUI
# ============================================================

class PenplotterPaintGUI:
    def __init__(self, root):
        root.title("PENPLOTTER PAINT SPLITTER")
        root.geometry("700x1050")
        root.configure(bg='black')

        self.bucket_file = tk.StringVar()
        self.input_file = tk.StringVar()
        self.splitdist = tk.StringVar(value="100")  # mm

        self.build_ui(root)

    # --------------------------------------------------------

    def build_ui(self, root):
        # Title
        title_label = tk.Label(
            root, 
            text="PENPLOTTER PAINT SPLITTER",
            font=("Arial", 20, "bold"),
            bg='black',
            fg='white'
        )
        title_label.pack(pady=20)

        # STEP 1 - Install VPYPE
        self.create_step_section(
            root,
            "STEP 1",
            "Install VPYPE",
            has_link=True
        )

        # Separator
        tk.Frame(root, height=2, bg='#404040').pack(fill='x', padx=20, pady=10)

        # STEP 2 - Load Bucket Path
        self.create_step_section(
            root,
            "STEP 2",
            "LOAD BUCKET PATH SVG\n(Draw a single line in Inkscape where your first paint color is located.Vpype will duplicate it for each color layer)"
        )
        
        bucket_frame = tk.Frame(root, bg='black')
        bucket_frame.pack(padx=20, fill='x', pady=(0, 10))
        
        tk.Entry(
            bucket_frame, 
            textvariable=self.bucket_file, 
            width=55,
            bg='#2b2b2b',
            fg='white',
            insertbackground='white'
        ).pack(side='left', fill='x', expand=True)
        
        tk.Button(
            bucket_frame, 
            text="Browse", 
            command=self.browse_bucket,
            bg='#404040',
            fg='white',
            activebackground='#505050',
            activeforeground='white',
            width=10
        ).pack(side='left', padx=5)

        # Separator
        tk.Frame(root, height=2, bg='#404040').pack(fill='x', padx=20, pady=10)

        # STEP 3 - Load SVG Drawing
        self.create_step_section(
            root,
            "STEP 3",
            "LOAD YOUR DRAWING TO SPLIT\n(Multi-color SVG with each color on a separate layer. Must use same paper size and units as bucket path)"
        )
        
        input_frame = tk.Frame(root, bg='black')
        input_frame.pack(padx=20, fill='x', pady=(0, 10))
        
        tk.Entry(
            input_frame, 
            textvariable=self.input_file, 
            width=55,
            bg='#2b2b2b',
            fg='white',
            insertbackground='white'
        ).pack(side='left', fill='x', expand=True)
        
        tk.Button(
            input_frame, 
            text="Browse", 
            command=self.browse_input,
            bg='#404040',
            fg='white',
            activebackground='#505050',
            activeforeground='white',
            width=10
        ).pack(side='left', padx=5)

        # Separator
        tk.Frame(root, height=2, bg='#404040').pack(fill='x', padx=20, pady=10)

        # STEP 4 - Split Distance
        self.create_step_section(
            root,
            "STEP 4",
            "SET SPLIT DISTANCE\n(Distance in mm between each paint reload)"
        )
        
        split_frame = tk.Frame(root, bg='black')
        split_frame.pack(padx=20, fill='x', pady=(0, 10))
        
        tk.Entry(
            split_frame, 
            textvariable=self.splitdist, 
            width=15,
            bg='#2b2b2b',
            fg='white',
            insertbackground='white',
            font=("Arial", 12)
        ).pack(side='left')

        # Separator
        tk.Frame(root, height=2, bg='#404040').pack(fill='x', padx=20, pady=10)

        # STEP 5 - Split Button
        step5_label = tk.Label(
            root, 
            text="STEP 5",
            font=("Arial", 12, "bold"),
            bg='black',
            fg='white'
        )
        step5_label.pack(anchor="w", padx=20, pady=(10, 5))

        split_button = tk.Button(
            root, 
            text="SPLIT", 
            command=self.run_split,
            bg='#1a5f1a',
            fg='white',
            activebackground='#267326',
            activeforeground='white',
            font=("Arial", 14, "bold"),
            height=2,
            width=15
        )
        split_button.pack(anchor="w", padx=20, pady=10)

        # Separator
        tk.Frame(root, height=2, bg='#404040').pack(fill='x', padx=20, pady=10)

        # STEP 6 - Final instructions
        self.create_step_section(
            root,
            "STEP 6",
            "Open the result file in Inkscape.\nManually adjust the position of each group bucket path to match your palette layout"
        )

        # Separator
        tk.Frame(root, height=2, bg='#404040').pack(fill='x', padx=20, pady=20)

        # Help message at the bottom
        help_frame = tk.Frame(root, bg='#1a1a1a', relief='ridge', borderwidth=2)
        help_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(
            help_frame,
            text="⚠ TROUBLESHOOTING",
            font=("Arial", 10, "bold"),
            bg='#1a1a1a',
            fg='#ffcc00'
        ).pack(pady=(10, 5))
        
        tk.Label(
            help_frame,
            text="If the program doesn't work, you may need to configure the vpype path.\n"
                 "Open this Python file in a text editor and modify the VPYPE_CMD variable\n"
                 "at the top to match your vpype installation location.",
            font=("Arial", 11),
            bg='#1a1a1a',
            fg='#cccccc',
            justify='left'
        ).pack(padx=15, pady=(0, 10))
        
        tk.Label(
            help_frame,
            text="Example: VPYPE_CMD = r\"C:\\path\\to\\your\\vpype.exe\"",
            font=("Arial", 13, "bold"),
            bg='#1a1a1a',
            fg='#ffcc00'
        ).pack(pady=(10, 5))

    # --------------------------------------------------------

    def create_step_section(self, root, step_num, description, has_link=False):
        """Create a step section with title and description"""
        step_label = tk.Label(
            root, 
            text=step_num,
            font=("Arial", 12, "bold"),
            bg='black',
            fg='white'
        )
        step_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        desc_label = tk.Label(
            root, 
            text=description,
            font=("Arial", 10),
            bg='black',
            fg='white',
            justify='left'
        )
        desc_label.pack(anchor="w", padx=20, pady=(2, 0))
        
        if has_link:
            link_label = tk.Label(
                root,
                text="https://vpype.readthedocs.io/en/latest/install.html",
                font=("Arial", 9, "underline"),
                bg='black',
                fg='#4a9eff',
                cursor="hand2"
            )
            link_label.pack(anchor="w", padx=20, pady=(2, 0))
            link_label.bind("<Button-1>", lambda e: webbrowser.open("https://vpype.readthedocs.io/en/latest/install.html"))

    # --------------------------------------------------------

    def browse_bucket(self):
        f = filedialog.askopenfilename(
            title="Select Bucket Path SVG",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
        )
        if f:
            self.bucket_file.set(f)

    def browse_input(self):
        f = filedialog.askopenfilename(
            title="Select Drawing SVG to Split",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
        )
        if f:
            self.input_file.set(f)

    # --------------------------------------------------------

    def build_command(self, outfile):
        infile = self.input_file.get()
        bucketfile = self.bucket_file.get()

        if not infile or not bucketfile:
            return ""

        cmd = (
            f'"{VPYPE_CMD}" '
            f'eval "files_in=[\'{infile}\']" '
            f'read -a stroke "{infile}" '
            f'forlayer '
            f'splitdist {self.splitdist.get()}mm '
            f'forlayer '
            f'lmove %_lid% "%_lid*2%" '
            f'read -l "%_lid*2-1%" "{bucketfile}" '
            f'end '
            f'lmove all %_lid% '
            f'end '
            f'write "{outfile}"'
        )

        print("\n" + "="*60)
        print("VPYPE COMMAND:")
        print("="*60)
        print(cmd)
        print("="*60 + "\n")
        
        return cmd

    # --------------------------------------------------------

    def run_split(self):
        infile = self.input_file.get()
        bucketfile = self.bucket_file.get()
        
        # Validation
        if not infile:
            messagebox.showerror("Error", "Please select an SVG drawing to split (Step 3).")
            return
        
        if not bucketfile:
            messagebox.showerror("Error", "Please select a Bucket Path SVG (Step 2).")
            return

        if not os.path.exists(infile):
            messagebox.showerror("Error", f"Drawing file not found:\n{infile}")
            return

        if not os.path.exists(bucketfile):
            messagebox.showerror("Error", f"Bucket file not found:\n{bucketfile}")
            return

        try:
            splitdist = float(self.splitdist.get())
            if splitdist <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid split distance (positive number).")
            return

        # Ask user where to save the output file
        default_name = os.path.basename(infile).replace(".svg", "_PAINT.svg")
        initial_dir = os.path.dirname(infile)
        
        outfile = filedialog.asksaveasfilename(
            title="Save Split File As",
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")],
            initialfile=default_name,
            initialdir=initial_dir
        )
        
        if not outfile:
            # User cancelled
            return

        # Build and run command
        cmd = self.build_command(outfile)
        if not cmd:
            return
        
        try:
            # Run the command
            process = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            if process.returncode == 0:
                # Success message with green styling
                success_window = tk.Toplevel()
                success_window.title("Success")
                success_window.geometry("500x200")
                success_window.configure(bg='#1a5f1a')
                
                tk.Label(
                    success_window,
                    text="✓ SPLIT COMPLETED SUCCESSFULLY",
                    font=("Arial", 16, "bold"),
                    bg='#1a5f1a',
                    fg='white'
                ).pack(pady=20)
                
                tk.Label(
                    success_window,
                    text=f"Output saved to:\n{outfile}",
                    font=("Arial", 10),
                    bg='#1a5f1a',
                    fg='white',
                    wraplength=450
                ).pack(pady=10)
                
                tk.Button(
                    success_window,
                    text="OK",
                    command=success_window.destroy,
                    bg='white',
                    fg='#1a5f1a',
                    font=("Arial", 12, "bold"),
                    width=10
                ).pack(pady=10)
                
                # Auto close after 5 seconds
                success_window.after(5000, success_window.destroy)
                
            else:
                # Error from vpype
                error_msg = f"vpype command failed.\n\nError output:\n{process.stderr}"
                if process.stdout:
                    error_msg += f"\n\nStandard output:\n{process.stdout}"
                messagebox.showerror("vpype Error", error_msg)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run vpype:\n\n{str(e)}")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("PENPLOTTER PAINT SPLITTER - STARTED")
    print("="*60 + "\n")
    
    root = tk.Tk()
    app = PenplotterPaintGUI(root)
    root.mainloop()