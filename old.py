import subprocess, tkinter, tkinter.filedialog, asyncio

default = {
    "export_location": "output/",
    "visuals_filename": "output.mp4",
    "audio_filename": "output.aac",
}

async def extract():
    submit_button["state"] = tkinter.DISABLED
    status_text.set("Extracting")

    await asyncio.sleep(1)

    if using_default_export.get():
        clear_output_directory()

    target_video_path = filename.get().replace("\"", "\\\"")

    if visual_checked.get():
        print("Extracting visuals")

        await system_call("""ffmpeg -i "{}" -an -vcodec copy {}{} -y""".format(target_video_path, custom_export_location.get(), custom_visuals_filename.get()))

        print("Visuals complete")
        
    if audio_checked.get():
        print("Extracting audio")

        await system_call("""ffmpeg -i "{}" -vn -acodec copy {}{} -y""".format(target_video_path, custom_export_location.get(), custom_audio_filename.get()))

        print("Audio complete")

    submit_button["state"] = tkinter.NORMAL
    print("Extraction complete")
    status_text.set("Done")

async def system_call(command):
    return subprocess.call(command)

def get_export_location():
    return default["export_location"] if using_default_export else custom_export_location.get()


def toggle_custom_export_options():
    if using_default_export.get():
        for widget in custom_export_options:
            widget["state"] = tkinter.DISABLED

        custom_export_location.set(default["export_location"])
        custom_visuals_filename.set(default["visuals_filename"])
        custom_audio_filename.set(default["audio_filename"])
        
    else:
        for widget in custom_export_options:
            widget["state"] = tkinter.NORMAL

def clear_output_directory():
    import os, shutil

    for export_filename in [default["visuals_filename"], default["audio_filename"]]:
        path = os.path.join(default["export_location"], export_filename)
        if os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def browse_files(title, string_var):
    path = tkinter.filedialog.askopenfilename(title=title)
    if path:
        string_var.set(path)

def browse_directory(title, string_var):
    path = tkinter.filedialog.askdirectory(title=title)
    if path:
        string_var.set(path)

def verify_requirements():
    submit_button["state"] = tkinter.NORMAL if visual_checked.get() or audio_checked.get() else tkinter.DISABLED


# window
window = tkinter.Tk()
window.title("Ripvideo")
window.minsize(600, 300)

divs = [tkinter.Frame(bd=8) for i in range(6)]

# 0 — file path
filename_input_frame = tkinter.Frame(divs[0])

filename = tkinter.StringVar()

filename_input = tkinter.Entry(filename_input_frame, textvariable=filename, width=64)

tkinter.Label(divs[0], text="Target video").pack()
filename_input.pack(side=tkinter.LEFT)
tkinter.Button(filename_input_frame, text="Browse…",
        command=lambda: browse_files("Select target video", filename)).pack(side=tkinter.RIGHT)
filename_input_frame.pack()

# 1 — export type
tkinter.Label(divs[1], text="I want to extract the…").pack()

visual_checked = tkinter.BooleanVar()
audio_checked = tkinter.BooleanVar()

visual_checkbutton = tkinter.Checkbutton(divs[1], text="visuals",
        variable=visual_checked, onvalue=True, offvalue=False, command=verify_requirements)
audio_checkbutton = tkinter.Checkbutton(divs[1], text="audio",
        variable=audio_checked, onvalue=True, offvalue=False, command=verify_requirements)

audio_checkbutton.select()

visual_checkbutton.pack()
audio_checkbutton.pack()

# 2 — export location
using_default_export = tkinter.BooleanVar()
custom_export_location = tkinter.StringVar()
custom_visuals_filename = tkinter.StringVar()
custom_audio_filename = tkinter.StringVar()

default_export_checkbutton = tkinter.Checkbutton(divs[2], text="Use default location",
        variable=using_default_export, onvalue=True, offvalue=False, command=toggle_custom_export_options)
custom_export_location_input_frame = tkinter.Frame(divs[2])
custom_export_location_input = tkinter.Entry(custom_export_location_input_frame, textvariable=custom_export_location, width=64)
custom_export_location_button = tkinter.Button(custom_export_location_input_frame, text="Browse…",
        command=lambda: browse_directory("Select output destination", custom_export_location))
custom_visuals_filename_input = tkinter.Entry(divs[2], textvariable=custom_visuals_filename, width=16)
custom_audio_filename_input = tkinter.Entry(divs[2], textvariable=custom_audio_filename, width=16)

default_export_checkbutton.select()

tkinter.Label(divs[2], text="Export file location").pack()
default_export_checkbutton.pack()
custom_export_location_input.pack(side=tkinter.LEFT)
custom_export_location_button.pack(side=tkinter.RIGHT)
custom_export_location_input_frame.pack()
tkinter.Label(divs[2], text="Visuals filename").pack()
custom_visuals_filename_input.pack()
tkinter.Label(divs[2], text="Audio filename").pack()
custom_audio_filename_input.pack()

custom_export_options = [custom_export_location_input, custom_visuals_filename_input, custom_audio_filename_input, custom_export_location_button]
toggle_custom_export_options()

# 3 — trimming


# 4 — submit
submit_button = tkinter.Button(divs[4], text="Extract", command=lambda: asyncio.run(extract()))

submit_button.pack()

# 5 — status box
status_text = tkinter.StringVar()
status_text.set("…… status ……")

status_box = tkinter.Label(divs[5], textvariable=status_text, width=64)
status_box.pack()

for div in divs:
    div.pack()

window.mainloop()