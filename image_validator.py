from PIL import Image
import pytesseract

class ImageValidator:
    @staticmethod
    def is_not_receipt(image_file):
        try:
            # Use pytesseract to extract text from the image
            extracted_text = pytesseract.image_to_string(Image.open(image_file))

            # Check if the extracted text contains any receipt-related information
            date_found = "date" in extracted_text.lower()
            amount_found = "amount" in extracted_text.lower()
            vendor_name_found = "vendor name" in extracted_text.lower()

            # If none of the receipt-related information is found, return True (not a receipt)
            return not (date_found or amount_found or vendor_name_found)

        except Exception as e:
            # Handle any exceptions that might occur during image processing
            print(f"Error while processing the image: {e}")
            return False