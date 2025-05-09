# MPW-Certify

A web application for verifying certificate authenticity by using QR codes that link to a central database. This application allows users to quickly validate the legitimacy of UFP (Universal Fraud Prevention) certificates by scanning a QR code or entering a certificate ID.

## Features

- Certificate lookup by ID
- Displays detailed certificate information
- Responsive web interface
- Excel-based database integration

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: Excel (.xlsx)
- **Dependencies**: 
  - flask
  - pandas
  - openpyxl
  - python-dotenv

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mpw-certify.git
   cd mpw-certify
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure you have the `UFP Certificates.xlsx` file in the root directory of the project.

### Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage

1. Enter a certificate ID in the search box
2. Click the "Search" button or press Enter
3. View the certificate details if it exists in the database

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── UFP Certificates.xlsx  # Certificate database
├── vercel.json            # Vercel deployment configuration
└── templates/
    ├── admin.html         # Admin interface
    └── index.html         # Web interface
```

## License

This project is licensed under the terms of the license file included in the repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.