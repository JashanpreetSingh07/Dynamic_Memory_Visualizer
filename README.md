Dynamic Memory Management Visualizer

A web-based Operating System simulation tool that visually demonstrates dynamic memory management techniques such as paging, segmentation, and page replacement algorithms. The project provides an interactive interface to help students understand how memory is allocated, managed, and replaced in modern operating systems.

Live Demo:  
https://dynamic-memory-visualizer.onrender.com

GitHub Repository: 
https://github.com/JashanpreetSingh07/Dynamic_Memory_Visualizer

---

Project Overview

Memory management is a core component of operating systems responsible for allocating and managing memory resources efficiently. Techniques such as paging, segmentation, and page replacement are used to optimize memory usage and reduce fragmentation.

This project provides a visual learning platform where users can simulate these techniques and observe how memory behaves in different scenarios.

The goal of the project is to:

- Help students understand **memory allocation and replacement algorithms**
- Provide **visual representations of memory usage**
- Simulate **page faults and memory allocation**
- Improve understanding of **Operating System concepts**

---

# Features

## Memory Management Simulation
- Paging simulation
- Segmentation simulation
- Virtual memory representation

## Page Replacement Algorithms
- FIFO (First-In First-Out)
- LRU (Least Recently Used)
- Random

## Visualization
- Dynamic graphical representation of memory blocks
- Visualization of allocated and free memory
- Page fault display

## Interactive Inputs
Users can input:
- Number of frames
- Page reference string
- Memory sizes
- Segment details

## Web Interface
- Simple and interactive UI
- Real-time output
- Easy-to-use controls

---

# System Architecture

The project follows a **Flask-based architecture**.

```
Dynamic_Memory_Visualizer/
│
├── backend/
│   ├── algorithm.py
│   ├── paging.py
│   └── segmentation.py
│
├── frontend/
│   ├── main_ui.py
│   └── visualizer.py
│
├── templates/
│
├── static/
│
├── app.py
│
└── requirements.txt
```

### Backend
Handles the core memory management logic:

- Memory allocation
- Page replacement algorithms
- Page fault calculation

### Frontend
Responsible for:

- User interface
- Visualization
- Displaying results

### Flask Application
Acts as a bridge between frontend and backend.

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web framework |
| HTML | Frontend structure |
| CSS | Styling |
| JavaScript | Interactive UI |
| Render | Deployment platform |

---

# Installation Guide

### 1 Clone the repository

```bash
git clone https://github.com/JashanpreetSingh07/Dynamic_Memory_Visualizer.git
```

### 2 Navigate to the project directory

```bash
cd Dynamic_Memory_Visualizer
```

### 3 Install dependencies

```bash
pip install -r requirements.txt
```

### 4 Run the Flask application

```bash
Web (Flask UI — runs locally at http://127.0.0.1:5000/):
python app.py --web
Or run Flask app directly:
python flask_app.py
```

### 5 Open in browser

```
http://127.0.0.1:5000
```

---

# How It Works

1. The user enters memory parameters through the UI.
2. Flask sends the data to the backend algorithms.
3. The algorithm processes memory allocation.
4. Results are returned to the frontend.
5. The UI visualizes memory allocation and page replacement steps.

---

# Example Use Case

Example input:

```
Frames: 3
Reference String: 7 0 1 2 0 3 0 4
Algorithm: FIFO
```

Output:

```
Page Faults: 6
Memory Frames Visualization
```

The visualizer displays step-by-step memory changes.

---

# Screenshots

(Add screenshots here)

Example:

```
/screenshots/home.png
/screenshots/paging.png
/screenshots/segmentation.png
```

---

# Deployment

The project is deployed using **Render**.

Live Application:  
https://dynamic-memory-visualizer.onrender.com

---

# Learning Outcomes

This project helps understand:

- Dynamic memory allocation
- Paging
- Segmentation
- Page replacement algorithms
- Memory fragmentation
- Operating system memory management concepts

---

# Future Improvements

Possible improvements:

- Add more page replacement algorithms (Optimal, LFU)
- Add real-time animated visualizations
- Improve UI/UX
- Add performance comparison between algorithms
- Convert project to full **React + Flask architecture**

---

# Contributing

Contributions are welcome.

Steps:

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Push to your branch  
5. Create a Pull Request  

---

# Author

**Jashanpreet Singh**

B.Tech Computer Science Engineering

GitHub:  
https://github.com/JashanpreetSingh07

---

# License

This project is developed for **educational purposes**.
