import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend.memory_management import PagingSimulator, SegmentationSimulator
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

def setup_styles():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#1A1A2E")
    style.configure("TLabel", background="#1A1A2E", foreground="white", font=("Montserrat", 12))
    style.configure("TEntry", foreground="white", fieldbackground="#16213E", background="#16213E")
    style.configure("TButton", background="#16213E", foreground="white", font=("Montserrat", 12), borderwidth=0)
    style.map("TButton", background=[("active", "#E94560")])
    style.configure("TCombobox", font=("Montserrat", 12), background="#16213E", foreground="white")
    style.map("TCombobox", fieldbackground=[("readonly", "#16213E")])

class DynamicMemoryVisualizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Dynamic Memory Management Visualizer")
        master.state("zoomed")
        master.configure(background="#1A1A2E")
        setup_styles()

        # Create a scrollable container for main content
        self.container = ttk.Frame(master)
        self.container.grid(row=0, column=0, sticky="nsew")
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        
        # Set up Canvas and Scrollbar for scrolling
        self.canvas = tk.Canvas(self.container, background="#1A1A2E", highlightthickness=0)
        self.v_scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create a frame inside the canvas
        self.content_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="center")
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        
        # Top frame for simulation type selection
        self.top_frame = ttk.Frame(self.content_frame)
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.top_frame.columnconfigure(1, weight=1)
        ttk.Label(self.top_frame, text="Select Simulation Type:", font=("Montserrat", 16, "bold")).grid(row=0, column=0, sticky="w")
        self.simulation_type = tk.StringVar(value="Paging")
        self.sim_type_combo = ttk.Combobox(
            self.top_frame, textvariable=self.simulation_type,
            values=["Paging", "Segmentation"],
            state="readonly", font=("Montserrat", 14)
        )
        self.sim_type_combo.grid(row=0, column=1, sticky="ew", padx=10)
        self.sim_type_combo.bind("<<ComboboxSelected>>", self.on_simulation_change)

        # Main content frame for simulation-specific UI
        self.sim_frame = ttk.Frame(self.content_frame)
        self.sim_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.columnconfigure(0, weight=1)
        
        # Create simulation-specific frames
        self.create_paging_frame()
        self.create_segmentation_frame()
        self.show_frame("Paging")
        
        # Variables for paging graph visualization
        self.paging_faults = []
        self.paging_access_numbers = []
        self.paging_access_count = 0
        
        # Variables for segmentation graph visualization (free memory %)
        self.seg_free_memory = []
        self.seg_update_numbers = []
        self.seg_update_count = 0

    def on_frame_configure(self, event):
        # Update scrollable region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Center the content frame horizontally
        self.canvas.itemconfigure(1, anchor="n")

    def on_simulation_change(self, event):
        sim_type = self.simulation_type.get()
        self.show_frame(sim_type)
    
    def show_frame(self, sim_type):
        self.paging_frame.grid_forget()
        self.segmentation_frame.grid_forget()
        if sim_type == "Paging":
            self.paging_frame.grid(row=0, column=0, sticky="nsew")
        elif sim_type == "Segmentation":
            self.segmentation_frame.grid(row=0, column=0, sticky="nsew")
    
    # ----------------- Paging Simulation UI -----------------
    def create_paging_frame(self):
        self.paging_frame = ttk.Frame(self.sim_frame)
        for i in range(10):
            self.paging_frame.rowconfigure(i, pad=10)
        self.paging_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.paging_frame, text="Number of Frames:", font=("Montserrat", 12)).grid(row=0, column=0, sticky="e")
        self.frames_entry = ttk.Entry(self.paging_frame)
        self.frames_entry.grid(row=0, column=1, sticky="ew")
        self.frames_entry.insert(0, "4")
        
        ttk.Label(self.paging_frame, text="Replacement Algorithm:", font=("Montserrat", 12)).grid(row=1, column=0, sticky="e")
        self.algo_var = tk.StringVar(value="FIFO")
        self.algo_combo = ttk.Combobox(self.paging_frame, textvariable=self.algo_var,
                                       values=["FIFO", "LRU", "Random"], state="readonly")
        self.algo_combo.grid(row=1, column=1, sticky="ew")
        
        ttk.Label(self.paging_frame, text="Pages to Access (comma-separated):", font=("Montserrat", 12)).grid(row=2, column=0, sticky="e")
        self.page_entry = ttk.Entry(self.paging_frame)
        self.page_entry.grid(row=2, column=1, sticky="ew")
        
        # Process pages & file upload buttons
        self.access_button = ttk.Button(self.paging_frame, text="Process Pages", command=self.process_page_batch)
        self.access_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.upload_button = ttk.Button(self.paging_frame, text="Upload File", command=self.upload_page_file)
        self.upload_button.grid(row=4, column=0, columnspan=2, pady=5)
        self.reset_paging_button = ttk.Button(self.paging_frame, text="Reset Paging", command=self.reset_paging)
        self.reset_paging_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        self.paging_status = ttk.Label(self.paging_frame, text="Status: ", font=("Montserrat", 12))
        self.paging_status.grid(row=6, column=0, columnspan=2)
        self.frames_display = ttk.Label(self.paging_frame, text="Frames: []", font=("Montserrat", 12))
        self.frames_display.grid(row=7, column=0, columnspan=2)
        
        # Canvas for paging visualization
        self.paging_canvas = tk.Canvas(self.paging_frame, width=400, height=100, bg="white")
        self.paging_canvas.grid(row=8, column=0, columnspan=2, pady=10)
        
        # Matplotlib graph for page faults over time
        self.fig_paging = Figure(figsize=(4,2), dpi=100)
        self.ax_paging = self.fig_paging.add_subplot(111)
        self.ax_paging.set_title("Page Faults Over Time")
        self.ax_paging.set_xlabel("Access Number")
        self.ax_paging.set_ylabel("Page Faults")
        self.graph_canvas_paging = FigureCanvasTkAgg(self.fig_paging, master=self.paging_frame)
        self.graph_canvas_paging.get_tk_widget().grid(row=9, column=0, columnspan=2, pady=10)
        
        self.paging_simulator = None

    def update_paging_canvas(self):
        self.paging_canvas.delete("all")
        if not self.paging_simulator:
            return
        frames = self.paging_simulator.frames
        num_frames = len(frames)
        canvas_width = 400
        rect_width = canvas_width // num_frames if num_frames > 0 else 400
        for i, page in enumerate(frames):
            x0 = i * rect_width + 5
            y0 = 20
            x1 = (i+1) * rect_width - 5
            y1 = 80
            self.paging_canvas.create_rectangle(x0, y0, x1, y1, fill="#E94560", outline="black")
            display_text = str(page) if page is not None else ""
            self.paging_canvas.create_text((x0+x1)/2, (y0+y1)/2, text=display_text, font=("Montserrat", 14))
    
    def update_paging_graph(self):
        self.ax_paging.clear()
        self.ax_paging.set_title("Page Faults Over Time")
        self.ax_paging.set_xlabel("Access Number")
        self.ax_paging.set_ylabel("Page Faults")
        self.ax_paging.plot(self.paging_access_numbers, self.paging_faults, marker="o", linestyle="-", color="#E94560")
        self.graph_canvas_paging.draw()
    
    def process_page_batch(self):
        try:
            num_frames = int(self.frames_entry.get())
            algo = self.algo_var.get()
            if (self.paging_simulator is None or 
                self.paging_simulator.num_frames != num_frames or 
                self.paging_simulator.replacement_algo != algo):
                self.paging_simulator = PagingSimulator(num_frames, algo)
                self.paging_access_count = 0
                self.paging_faults = []
                self.paging_access_numbers = []
            pages_str = self.page_entry.get()
            pages = [int(x.strip()) for x in pages_str.split(",") if x.strip().isdigit()]
            for page in pages:
                fault = self.paging_simulator.access_page(page)
                self.paging_access_count += 1
                self.paging_access_numbers.append(self.paging_access_count)
                self.paging_faults.append(self.paging_simulator.page_faults)
            status = f"Processed pages: {pages}. Total faults: {self.paging_simulator.page_faults}."
            self.paging_status.config(text="Status: " + status)
            self.frames_display.config(text="Frames: " + str(self.paging_simulator.frames))
            self.update_paging_canvas()
            self.update_paging_graph()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def upload_page_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, "r") as f:
                    data = f.read()
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, data.strip())
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def reset_paging(self):
        if self.paging_simulator:
            self.paging_simulator.reset()
            self.paging_status.config(text="Status: Reset done.")
            self.frames_display.config(text="Frames: " + str(self.paging_simulator.frames))
            self.update_paging_canvas()
            self.paging_access_count = 0
            self.paging_faults = []
            self.paging_access_numbers = []
            self.update_paging_graph()
    
    # ----------------- Segmentation Simulation UI -----------------
    def create_segmentation_frame(self):
        self.segmentation_frame = ttk.Frame(self.sim_frame)
        for i in range(10):
            self.segmentation_frame.rowconfigure(i, pad=10)
        self.segmentation_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.segmentation_frame, text="Total Memory Size:", font=("Montserrat", 12)).grid(row=0, column=0, sticky="e")
        self.total_memory_entry = ttk.Entry(self.segmentation_frame)
        self.total_memory_entry.grid(row=0, column=1, sticky="ew")
        self.total_memory_entry.insert(0, "100")
        
        ttk.Label(self.segmentation_frame, text="Segment Size:", font=("Montserrat", 12)).grid(row=1, column=0, sticky="e")
        self.segment_size_entry = ttk.Entry(self.segmentation_frame)
        self.segment_size_entry.grid(row=1, column=1, sticky="ew")
        
        ttk.Label(self.segmentation_frame, text="Segment Label:", font=("Montserrat", 12)).grid(row=2, column=0, sticky="e")
        self.segment_label_entry = ttk.Entry(self.segmentation_frame)
        self.segment_label_entry.grid(row=2, column=1, sticky="ew")
        
        self.allocate_segment_button = ttk.Button(self.segmentation_frame, text="Allocate Segment", command=self.allocate_segment)
        self.allocate_segment_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.free_segment_button = ttk.Button(self.segmentation_frame, text="Free Segment", command=self.free_segment)
        self.free_segment_button.grid(row=4, column=0, columnspan=2, pady=5)
        # New Reset button to free all segments
        self.reset_seg_button = ttk.Button(self.segmentation_frame, text="Reset Segments", command=self.reset_segmentation)
        self.reset_seg_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        self.segmentation_status = ttk.Label(self.segmentation_frame, text="Status: ", font=("Montserrat", 12))
        self.segmentation_status.grid(row=6, column=0, columnspan=2)
        self.segments_display = ttk.Label(self.segmentation_frame, text="Segments: []", font=("Montserrat", 12))
        self.segments_display.grid(row=7, column=0, columnspan=2)
        
        # Canvas for segmentation visualization
        self.seg_canvas = tk.Canvas(self.segmentation_frame, width=400, height=100, bg="white")
        self.seg_canvas.grid(row=8, column=0, columnspan=2, pady=10)
        
        # Matplotlib graph for free memory percentage over time
        self.fig_seg = Figure(figsize=(4,2), dpi=100)
        self.ax_seg = self.fig_seg.add_subplot(111)
        self.ax_seg.set_title("Free Memory (%) Over Time")
        self.ax_seg.set_xlabel("Update Number")
        self.ax_seg.set_ylabel("Free Memory (%)")
        self.graph_canvas_seg = FigureCanvasTkAgg(self.fig_seg, master=self.segmentation_frame)
        self.graph_canvas_seg.get_tk_widget().grid(row=9, column=0, columnspan=2, pady=10)
        
        self.segmentation_simulator = None
    
    def update_segmentation_canvas(self):
        self.seg_canvas.delete("all")
        if self.segmentation_simulator is None:
            return
        total_memory = self.segmentation_simulator.total_memory
        canvas_width = 400
        canvas_height = 100
        self.seg_canvas.create_rectangle(5, 20, canvas_width-5, canvas_height-20, outline="black", fill="#16213E")
        segments = sorted(self.segmentation_simulator.segments, key=lambda x: x[0])
        for seg in segments:
            start, size, label = seg
            x0 = 5 + (start / total_memory) * (canvas_width - 10)
            x1 = 5 + ((start + size) / total_memory) * (canvas_width - 10)
            self.seg_canvas.create_rectangle(x0, 20, x1, canvas_height-20, fill="#E94560", outline="black")
            self.seg_canvas.create_text((x0+x1)/2, canvas_height/2, text=label, font=("Montserrat", 12, "bold"), fill="white")
    
    def update_segmentation_graph(self):
        self.ax_seg.clear()
        self.ax_seg.set_title("Free Memory (%) Over Time")
        self.ax_seg.set_xlabel("Update Number")
        self.ax_seg.set_ylabel("Free Memory (%)")
        self.ax_seg.plot(self.seg_update_numbers, self.seg_free_memory, marker="s", linestyle="-", color="#E94560")
        self.graph_canvas_seg.draw()
    
    def allocate_segment(self):
        try:
            total_memory = int(self.total_memory_entry.get())
            if self.segmentation_simulator is None or self.segmentation_simulator.total_memory != total_memory:
                self.segmentation_simulator = SegmentationSimulator(total_memory)
                self.seg_update_count = 0
                self.seg_free_memory = []
                self.seg_update_numbers = []
            size = int(self.segment_size_entry.get())
            label = self.segment_label_entry.get()
            success = self.segmentation_simulator.allocate_segment(size, label)
            status = f"Segment '{label}' allocated." if success else "Allocation failed. Not enough memory."
            self.segmentation_status.config(text="Status: " + status)
            self.segments_display.config(text="Segments: " + str(self.segmentation_simulator.segments))
            self.seg_update_count += 1
            self.seg_update_numbers.append(self.seg_update_count)
            free_pct = (self.segmentation_simulator.free_memory / self.segmentation_simulator.total_memory) * 100
            self.seg_free_memory.append(free_pct)
            self.update_segmentation_canvas()
            self.update_segmentation_graph()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def free_segment(self):
        try:
            label = self.segment_label_entry.get()
            if self.segmentation_simulator is None:
                messagebox.showerror("Error", "No segments allocated yet.")
                return
            success = self.segmentation_simulator.free_segment(label)
            status = f"Segment '{label}' freed." if success else "Segment not found."
            self.segmentation_status.config(text="Status: " + status)
            self.segments_display.config(text="Segments: " + str(self.segmentation_simulator.segments))
            self.seg_update_count += 1
            self.seg_update_numbers.append(self.seg_update_count)
            free_pct = (self.segmentation_simulator.free_memory / self.segmentation_simulator.total_memory) * 100
            self.seg_free_memory.append(free_pct)
            self.update_segmentation_canvas()
            self.update_segmentation_graph()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def reset_segmentation(self):
        # Reset segmentation simulator completely
        if self.segmentation_simulator:
            self.segmentation_simulator.reset()
            self.segmentation_status.config(text="Status: All segments reset.")
            self.segments_display.config(text="Segments: []")
            self.update_segmentation_canvas()
            self.seg_update_count = 0
            self.seg_free_memory = []
            self.seg_update_numbers = []
            self.update_segmentation_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = DynamicMemoryVisualizerApp(root)
    root.mainloop()
