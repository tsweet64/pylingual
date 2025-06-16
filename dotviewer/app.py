import os
import glob
from flask import Flask, redirect, render_template, jsonify, abort
import argparse

app = Flask(__name__)

# Global variables
DOT_FILES_INFO = [] # List of dicts: {'path', 'basename', 'group', 'num_idx', 'overall_index'}
GROUPED_FILES_LUT = {} # Dict: {'group_name': list_of_file_info_dicts}
SORTED_GROUP_NAMES = [] # List of actual group names, sorted
DOT_FILES = [] # Flat list of paths, globally sorted (for get_graph endpoint)
BASE_DIR = ""

def parse_filename_for_group(filename_basename):
    """
    Parses filename like 'groupname_idx.dot' into ('groupname', idx).
    If no '_', group is filename without .dot, idx is 0.
    If last part after '_' is not numeric, group is filename without .dot, idx is 0.
    """
    name_part_no_ext = filename_basename
    if filename_basename.lower().endswith('.dot'):
        name_part_no_ext = filename_basename[:-4]

    parts = name_part_no_ext.rsplit('_', 1)
    if len(parts) == 2:
        return parts[0], list(map(int, parts[1].split('-')))
    else:
        return name_part_no_ext, 0


@app.route('/')
def index():
    if not DOT_FILES_INFO:
        return "No .dot files found. Please restart with a valid directory."
    
    # Pass all group names (including "All" conceptually handled by JS)
    # and the name of the first group to load initially.
    initial_group_to_load = "All" # Default to "All"
    
    return render_template('index.html', 
                           all_group_names=SORTED_GROUP_NAMES,
                           initial_group_name=initial_group_to_load)


@app.route('/get_group_details/<group_name>')
def get_group_details(group_name):
    files_to_return = []
    
    if group_name == "All":
        for item in DOT_FILES_INFO:
            files_to_return.append({'filename': item['basename'], 'overall_index': item['overall_index']})
        return jsonify({'name': 'All', 'files': files_to_return, 'total_in_group': len(files_to_return)})
    
    elif group_name in GROUPED_FILES_LUT:
        for item in GROUPED_FILES_LUT[group_name]:
            files_to_return.append({'filename': item['basename'], 'overall_index': item['overall_index']})
        return jsonify({'name': group_name, 'files': files_to_return, 'total_in_group': len(files_to_return)})
    else:
        abort(404, description=f"Group '{group_name}' not found.")


@app.route('/get_graph/<int:overall_index>')
def get_graph(overall_index):
    if not 0 <= overall_index < len(DOT_FILES):
        abort(404, description="Graph overall_index out of bounds.")
    
    filepath = DOT_FILES[overall_index] 
    # We can also get basename from DOT_FILES_INFO if needed, but path is enough here
    filename = os.path.basename(filepath) 
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            dot_content = f.read()
        # The 'index' here is the overall_index, frontend will manage group-specific index
        return jsonify({'dot_content': dot_content, 'filename': filename, 'index': overall_index})
    except Exception as e:
        app.logger.error(f"Error reading file {filepath}: {e}")
        abort(500, description=f"Could not read graph file: {filename}")

def scan_dot_files(directory):
    global DOT_FILES_INFO, GROUPED_FILES_LUT, SORTED_GROUP_NAMES, DOT_FILES, BASE_DIR
    
    BASE_DIR = os.path.abspath(directory)
    pattern = os.path.join(BASE_DIR, "*.dot")
    raw_files_paths = glob.glob(pattern)

    if not raw_files_paths:
        print(f"Warning: No .dot files found in {BASE_DIR}")
        return

    parsed_files_data = []
    for f_path in raw_files_paths:
        basename = os.path.basename(f_path)
        group, num_idx = parse_filename_for_group(basename)
        parsed_files_data.append({'group': group, 'num_idx': num_idx, 'path': f_path, 'basename': basename})

    # Sort primarily by group name, then by numeric index, then by basename (for stability)
    parsed_files_data.sort(key=lambda x: (x['group'], x['num_idx'], x['basename']))

    # Assign overall_index and populate global structures
    DOT_FILES_INFO.clear()
    GROUPED_FILES_LUT.clear()
    
    temp_grouped_files = {} # Temporary dict to build GROUPED_FILES_LUT

    for overall_idx, item_data in enumerate(parsed_files_data):
        file_info = {
            'path': item_data['path'],
            'basename': item_data['basename'],
            'group': item_data['group'],
            'num_idx': item_data['num_idx'],
            'overall_index': overall_idx
        }
        DOT_FILES_INFO.append(file_info)
        
        if item_data['group'] not in temp_grouped_files:
            temp_grouped_files[item_data['group']] = []
        temp_grouped_files[item_data['group']].append(file_info)

    DOT_FILES = [item['path'] for item in DOT_FILES_INFO] # Update flat list of paths
    SORTED_GROUP_NAMES = sorted(temp_grouped_files.keys())
    
    for group_name in SORTED_GROUP_NAMES:
        GROUPED_FILES_LUT[group_name] = temp_grouped_files[group_name]

    print(f"Found {len(DOT_FILES_INFO)} .dot files in {BASE_DIR}, organized into {len(SORTED_GROUP_NAMES)} groups.")
    # For debugging, you can print groups:
    # for group_name in SORTED_GROUP_NAMES:
    # print(f"  Group '{group_name}': {[item['basename'] for item in GROUPED_FILES_LUT[group_name]]}")


@app.route('/reload')
def reload():
    global DOT_FILES_INFO, GROUPED_FILES_LUT, SORTED_GROUP_NAMES, DOT_FILES, BASE_DIR
    DOT_FILES_INFO = [] # List of dicts: {'path', 'basename', 'group', 'num_idx', 'overall_index'}
    GROUPED_FILES_LUT = {} # Dict: {'group_name': list_of_file_info_dicts}
    SORTED_GROUP_NAMES = [] # List of actual group names, sorted
    DOT_FILES = [] # Flat list of paths, globally sorted (for get_graph endpoint)
    BASE_DIR = ""
    scan_dot_files(args.directory)
    return redirect('/')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Web viewer for .dot files using Viz.js.")
    parser.add_argument('directory', type=str, help='Directory containing .dot files.', default='/tmp/cflow_test/graph', nargs='?')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the web server on.')
    args = parser.parse_args()

    scan_dot_files(args.directory)

    if not DOT_FILES_INFO:
        print("Exiting as no .dot files were found.")
    else:
        print(f"\nNavigate to http://127.0.0.1:{args.port}/ in your browser.")
        print("Use Dropdown to select group. Use Left/Right arrow keys to switch graphs within the selected group.")
        app.run(debug=True, port=args.port)
