import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox
from PIL import Image
import os

def combine_3ds_screens(primary_image_path):
    try:
        # Determine if the input is a top or bottom screen file
        base_name, ext = os.path.splitext(os.path.basename(primary_image_path))
        if "_top" in base_name:
            other_image_path = primary_image_path.replace("_top", "_bot")
        elif "_bot" in base_name:
            other_image_path = primary_image_path.replace("_bot", "_top")
        else:
            messagebox.showerror("Error", "File must contain '_top' or '_bot' in the name.")
            return
        
        # Check if the other screen file exists
        if not os.path.exists(other_image_path):
            messagebox.showerror("Error", f"Matching file not found: {other_image_path}")
            return

        # Load the primary and other images
        primary_image = Image.open(primary_image_path)
        other_image = Image.open(other_image_path)
        
        # Determine which is top and bottom based on the filenames
        if "_top" in base_name:
            top_image, bottom_image = primary_image, other_image
        else:
            top_image, bottom_image = other_image, primary_image

        # Define dimensions for the combined image
        combined_width = max(top_image.width, bottom_image.width)
        combined_height = top_image.height + bottom_image.height

        # Create a new image with RGBA mode (to support transparency)
        combined_image = Image.new("RGBA", (combined_width, combined_height), (0, 0, 0, 0))

        # Paste the top screen at the top
        combined_image.paste(top_image, (0, 0))

        # Calculate x position to center the bottom screen
        bottom_x = (combined_width - bottom_image.width) // 2
        combined_image.paste(bottom_image, (bottom_x, top_image.height))

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)

        # Generate output file path
        timestamp = base_name.replace("_top", "").replace("_bot", "")
        output_path = os.path.join(output_dir, f"combined_{timestamp}.png")

        # Save the result as a PNG
        combined_image.save(output_path, "PNG")
        messagebox.showinfo("Success", f"Combined image saved as {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def combine_from_entry():
    primary_path = input_entry.get()
    if not primary_path:
        messagebox.showerror("Error", "Please provide a top or bottom screen file path.")
        return
    combine_3ds_screens(primary_path)

def show_credits():
    credits_window = tk.Toplevel(root)
    credits_window.title("Credits")
    credits_window.geometry("300x200")
    credits_window.config(bg="#9dffb0")  # Minty green background

    # Title Label
    title_label = tk.Label(credits_window, text="Credits", font=("Arial", 16, "bold"), bg="#b3e6b3")
    title_label.pack(pady=10)

    # Credits Text
    text = tk.Text(credits_window, wrap=tk.WORD, height=6, width=40, font=("Arial", 12), bg="#b3e6b3", bd=0, padx=10, pady=10)
    text.pack(pady=10)

    url = "https://dreamykiley.carrd.co/"
    additional_text = "\n"

    text.insert(tk.END, "3DS Image Combiner\n\nCredit: Kiley W.\nVisit: ")
    text.insert(tk.END, url, ('url',))
    text.tag_config('url', foreground='blue', underline=True)
    text.bind("<Button-1>", lambda e: webbrowser.open(url))

    text.insert(tk.END, f"\n\n{additional_text}")

    text.config(state=tk.DISABLED)

    # Close Button
    close_button = tk.Button(credits_window, text="Close", command=credits_window.destroy, font=("Arial", 12), bg="#4CAF50", fg="white")
    close_button.pack(pady=10)

def create_gui():
    global root, input_entry

    root = tk.Tk()
    root.title("3DS Image Combiner")
    root.geometry("400x300")
    root.config(bg="#9dffb0")

    # Title Label
    title_label = tk.Label(root, text="3DS Image Combiner", font=("Arial", 16, "bold"), bg="#b3e6b3")
    title_label.pack(pady=10)

    # Input file entry and button
    tk.Label(root, text="Top or Bottom:", font=("Arial", 12), bg="#9dffb0").pack(pady=5)
    input_entry = tk.Entry(root, width=50, font=("Arial", 12))
    input_entry.pack(pady=5, padx=10)
    tk.Button(root, text="Browse...", command=browse_file, font=("Arial", 12), bg="#007bff", fg="white").pack(pady=5)

    # Combine button
    tk.Button(root, text="Combine Images", command=combine_from_entry, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=15)

    # Credits button
    credits_button = tk.Button(root, text="Credits", command=show_credits, font=("Arial", 12), bg="#4CAF50", fg="white")
    credits_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
