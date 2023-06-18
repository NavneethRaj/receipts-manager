# Receipt Organizer

Receipt Organizer is a web application that allows you to upload and organize your receipts. It uses Flask as the backend framework and integrates Tesseract OCR for extracting text from uploaded receipt images.

## Prerequisites

Make sure you have the following prerequisites installed on your system:

- Python 3.x: [Download Python](https://www.python.org/downloads/)
- Tesseract OCR: [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/receipt-organizer.git
   ```
   
2. Change into the project directory:

    ```
    cd receipt-organizer
    ```

3. Create a virtual environment (optional but recommended):

    ```shell
    python3 -m venv venv

4. Activate the virtual environment:

    On Windows:
    ```shell
    venv\Scripts\activate
    
    On macOS and Linux:
    ```shell
    source venv/bin/activate

4. Install the project dependencies:

    ```shell
    pip install -r requirements.txt
    ```

5. Configuration
    Open the app.py file and set a secret key for session management. Modify the following line:

    app.secret_key = 'your_secret_key'

6. Usage
    1. Start the Flask development server:

        ```shell
        python app.py
    2. Open your web browser and go to http://localhost:5000.
    3. You should see the homepage of the Receipt Organizer web application.

Contributing
Contributions to the project are welcome! If you find any issues or have any suggestions, please create a new issue or submit a pull request.

License
This project is licensed under the MIT License.

Please replace `your-username` in the URLs with your actual GitHub username when creating the repository.