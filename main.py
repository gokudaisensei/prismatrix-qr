from PIL import Image, ImageDraw, ImageFont
import pyqrcode
from loguru import logger
import os
from concurrent.futures import ThreadPoolExecutor
import sys

# Configure Loguru logger
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# Output directories
qr_code_dir = './qr_codes'
id_card_dir = './id_cards'

# Create directories if they don't exist
for directory in [qr_code_dir, id_card_dir]:
    os.makedirs(directory, exist_ok=True)

# Function to process a single participant
def process_participant(participant_number):
    try:
        # Load the template and create ImageDraw object
        template_path = './Participants.png'
        template = Image.open(template_path)
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype('./fonts/JetBrainsMono-Bold.ttf', size=80)

        qr_number = f'PM-{participant_number:03d}'
        
        # Log the start of processing for the participant
        logger.info(f"Processing participant: {qr_number}")
        
        # Create QR code
        qrcode = pyqrcode.create(qr_number, version=2)

        # Save QR code image to a file
        qr_code_path = f'{qr_code_dir}/{qr_number}.png'
        qrcode.png(qr_code_path, scale=32)

        # Paste QR code onto the template
        qr_image = Image.open(qr_code_path)
        template.paste(qr_image, (1091, 2261))

        # Draw participant number on the template
        draw.text((1483, 3501), qr_number, font=font, fill='black', stroke_width=1, align='left')

        # Save the modified template as an ID card
        id_card_path = f'{id_card_dir}/{qr_number}.png'
        template.save(id_card_path)

        # Log the completion of processing for the participant
        logger.success(f"Participant {qr_number} processed successfully.")

    except Exception as e:
        logger.error(f"Error processing participant {qr_number}: {e}")

# Generate QR codes and ID cards using parallel processing with threads
with ThreadPoolExecutor() as executor:
    executor.map(process_participant, range(1, 301))

logger.info("Script execution complete.")

