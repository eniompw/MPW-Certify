## MPW-Certify

A web application for verifying certificate authenticity by using QR codes that link to a central database. This application allows users to quickly validate the legitimacy of UFP (Universal Fraud Prevention) certificates by scanning a QR code or entering a certificate ID.

## Features

- Certificate lookup by ID
- Displays detailed certificate information
- Responsive web interface
- Excel-based database integration
- Vercel deployment ready

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: Excel (.xlsx)
- **Dependencies**: 
  - flask
  - pandas
  - openpyxl
  - python-dotenv
  - qrcode
  - pillow

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

## Vercel Deployment

This application is configured to work with Vercel deployment. When deployed on Vercel:

1. The Excel file will be stored in the `/tmp` directory, which is writable on Vercel
2. Any changes made to the data will persist for the duration of the serverless function execution
3. The `VERCEL` environment variable is set to identify when running in the Vercel environment

Note that since Vercel uses serverless functions with ephemeral file systems, data changes will not persist permanently between different function invocations. For a production environment, consider using a more persistent storage solution like a database.

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