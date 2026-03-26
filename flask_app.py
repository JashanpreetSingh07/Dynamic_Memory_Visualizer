from flask import Flask, render_template, jsonify, request
from backend.memory_management import PagingSimulator, SegmentationSimulator
import json

app = Flask(__name__)

# Global simulators
paging_simulator = None
segmentation_simulator = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/paging/initialize', methods=['POST'])
def initialize_paging():
    global paging_simulator
    data = request.json
    num_frames = data.get('num_frames')
    replacement_algo = data.get('replacement_algo')
    
    paging_simulator = PagingSimulator(num_frames, replacement_algo)
    return jsonify({
        'status': 'success',
        'message': 'Paging simulator initialized'
    })

@app.route('/api/paging/process', methods=['POST'])
def process_pages():
    global paging_simulator
    if not paging_simulator:
        return jsonify({
            'status': 'error',
            'message': 'Paging simulator not initialized'
        }), 400
    
    data = request.json
    pages = data.get('pages', [])
    results = []
    
    for page in pages:
        fault = paging_simulator.access_page(page)
        results.append({
            'page': page,
            'fault': fault,
            'frames': paging_simulator.frames.copy(),
            'total_faults': paging_simulator.page_faults,
            'total_hits': paging_simulator.total_hits
        })
    
    return jsonify({
        'status': 'success',
        'results': results
    })

@app.route('/api/paging/reset', methods=['POST'])
def reset_paging():
    global paging_simulator
    if paging_simulator:
        paging_simulator.reset()
    return jsonify({
        'status': 'success',
        'message': 'Paging simulator reset'
    })

@app.route('/api/segmentation/initialize', methods=['POST'])
def initialize_segmentation():
    global segmentation_simulator
    data = request.json
    total_memory = data.get('total_memory')
    
    segmentation_simulator = SegmentationSimulator(total_memory)
    return jsonify({
        'status': 'success',
        'message': 'Segmentation simulator initialized'
    })

@app.route('/api/segmentation/allocate', methods=['POST'])
def allocate_segment():
    global segmentation_simulator
    if not segmentation_simulator:
        return jsonify({
            'status': 'error',
            'message': 'Segmentation simulator not initialized'
        }), 400
    
    data = request.json
    size = data.get('size')
    label = data.get('label')
    
    success = segmentation_simulator.allocate_segment(size, label)
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Segment allocated' if success else 'Not enough memory',
        'segments': segmentation_simulator.segments,
        'free_memory': segmentation_simulator.free_memory
    })

@app.route('/api/segmentation/free', methods=['POST'])
def free_segment():
    global segmentation_simulator
    if not segmentation_simulator:
        return jsonify({
            'status': 'error',
            'message': 'Segmentation simulator not initialized'
        }), 400
    
    data = request.json
    label = data.get('label')
    
    success = segmentation_simulator.free_segment(label)
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Segment freed' if success else 'Segment not found',
        'segments': segmentation_simulator.segments,
        'free_memory': segmentation_simulator.free_memory
    })

@app.route('/api/segmentation/reset', methods=['POST'])
def reset_segmentation():
    global segmentation_simulator
    if segmentation_simulator:
        segmentation_simulator.reset()
    return jsonify({
        'status': 'success',
        'message': 'Segmentation simulator reset'
    })

if __name__ == '__main__':
    app.run(debug=True) 