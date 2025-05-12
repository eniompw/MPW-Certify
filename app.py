from flask import Flask, render_template, jsonify, request, send_file
import pandas as pd
import os
import qrcode
from io import BytesIO
import shutil

app = Flask(__name__)

def get_excel_path():
    """Get the path to the Excel file, ensuring it exists in /tmp for Vercel"""
    # On Vercel, use /tmp directory which is writable
    if os.environ.get('VERCEL', '0') == '1':
        excel_dir = '/tmp'
    else:
        # In local development, use the current directory
        excel_dir = os.path.dirname(__file__)
    
    excel_path = os.path.join(excel_dir, 'UFP Certificates.xlsx')
    
    # If we're on Vercel and the file doesn't exist in /tmp yet, copy it there
    if os.environ.get('VERCEL', '0') == '1' and not os.path.exists(excel_path):
        # Copy the file from the source directory to /tmp
        source_path = os.path.join(os.path.dirname(__file__), 'UFP Certificates.xlsx')
        shutil.copy2(source_path, excel_path)
    
    return excel_path

def extract_excel_data():
    """Extract data from the Excel file and return as a dictionary"""
    try:
        excel_path = get_excel_path()
        # Read the Excel file
        df = pd.read_excel(excel_path)
        
        # Convert DataFrame to a list of dictionaries (records)
        data = df.to_dict(orient='records')
        
        return {'status': 'success', 'data': data, 'columns': df.columns.tolist()}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def save_excel_data(data):
    """Save data to the Excel file"""
    try:
        excel_path = get_excel_path()
        df = pd.DataFrame(data)
        df.to_excel(excel_path, index=False)
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def generate_id(year, candidate_num):
    """Generate ID by concatenating year and 4-digit candidate number"""
    # Convert candidate_num to 4-digit string with leading zeros
    candidate_str = str(candidate_num).zfill(4)
    # Concatenate year and candidate number
    return f"{year}{candidate_str}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/lookup', methods=['GET'])
def lookup_by_id():
    """Look up a specific row by ID from the query parameter"""
    try:
        # Get query parameter 'q'
        query_id = request.args.get('q')
        
        if not query_id:
            return jsonify({'status': 'error', 'message': 'No ID provided. Use ?q=ID in your query.'})
        
        # Load Excel data
        excel_path = get_excel_path()
        df = pd.read_excel(excel_path)
        
        # Convert ID to same type for comparison (handle string/int cases)
        # Try as integer first
        try:
            query_id = int(query_id)
            result = df[df['ID'] == query_id]
        except ValueError:
            # If ID is not an integer, try as string
            result = df[df['ID'].astype(str) == query_id]
        
        if result.empty:
            return jsonify({'status': 'not_found', 'message': f'No record found with ID: {query_id}'})
        
        # Return the record
        record = result.to_dict(orient='records')[0]
        record['Teacher'] = result['Teacher'].values[0] if 'Teacher' in result.columns else 'Unknown'
        return jsonify({'status': 'success', 'data': record})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/records', methods=['GET'])
def get_all_records():
    """Get all records from the Excel file"""
    result = extract_excel_data()
    return jsonify(result)

@app.route('/api/records', methods=['POST'])
def add_record():
    """Add a new record to the Excel file"""
    try:
        # Get data from request
        new_record = request.json
        
        # Load current data
        result = extract_excel_data()
        if result['status'] == 'error':
            return jsonify(result)
        
        data = result['data']
        
        # Check if Year and Candidate fields are provided
        if 'Year' not in new_record or 'Candidate' not in new_record:
            return jsonify({'status': 'error', 'message': 'Year and Candidate fields are required'})
        
        # Generate ID from Year and Candidate
        year = new_record['Year']
        candidate = int(new_record['Candidate'])  # Ensure it's an integer
        generated_id = generate_id(year, candidate)
        
        # Set the ID in the new record
        new_record['ID'] = generated_id
        
        # Check if ID already exists
        for record in data:
            if str(record['ID']) == str(generated_id):
                return jsonify({'status': 'error', 'message': f"Record with ID {generated_id} already exists"})
        
        # Add new record
        data.append(new_record)
        
        # Save data
        save_result = save_excel_data(data)
        if save_result['status'] == 'error':
            return jsonify(save_result)
        
        return jsonify({'status': 'success', 'message': 'Record added successfully', 'id': generated_id})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/records/<record_id>', methods=['PUT'])
def update_record(record_id):
    """Update a record in the Excel file"""
    try:
        # Get data from request
        updated_record = request.json
        
        # Load current data
        result = extract_excel_data()
        if result['status'] == 'error':
            return jsonify(result)
        
        data = result['data']
        
        # If Year and Candidate are being updated, regenerate the ID
        if 'Year' in updated_record and 'Candidate' in updated_record:
            year = updated_record['Year']
            candidate = int(updated_record['Candidate'])
            updated_record['ID'] = generate_id(year, candidate)
        
        # Find and update record
        record_found = False
        for i, record in enumerate(data):
            if str(record['ID']) == str(record_id):
                data[i] = updated_record
                record_found = True
                break
        
        if not record_found:
            return jsonify({'status': 'error', 'message': f"Record with ID {record_id} not found"})
        
        # Save data
        save_result = save_excel_data(data)
        if save_result['status'] == 'error':
            return jsonify(save_result)
        
        return jsonify({'status': 'success', 'message': 'Record updated successfully', 'id': updated_record['ID']})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete a record from the Excel file"""
    try:
        # Load current data
        result = extract_excel_data()
        if result['status'] == 'error':
            return jsonify(result)
        
        data = result['data']
        
        # Find and remove record
        record_found = False
        for i, record in enumerate(data):
            if str(record['ID']) == str(record_id):
                data.pop(i)
                record_found = True
                break
        
        if not record_found:
            return jsonify({'status': 'error', 'message': f"Record with ID {record_id} not found"})
        
        # Save data
        save_result = save_excel_data(data)
        if save_result['status'] == 'error':
            return jsonify(save_result)
        
        return jsonify({'status': 'success', 'message': 'Record deleted successfully'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/qrcode/<record_id>', methods=['GET'])
def generate_qr_code(record_id):
    """Generate a QR code for a certificate record"""
    try:
        # Create the URL for the certificate lookup
        base_url = request.host_url.rstrip('/')
        certificate_url = f"{base_url}/?q={record_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(certificate_url)
        qr.make(fit=True)
        
        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code to BytesIO object
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Return the image as a file response
        return send_file(img_io, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
