import os
from flask import Flask, request, render_template
import pytesseract
from PIL import Image

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有文件 part'
    
    file = request.files['file']
    
    if file.filename == '':
        return '没有选择文件'
    
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)

    # OCR 图片识别
    image = Image.open(save_path)
    text = pytesseract.image_to_string(image, lang='chi_sim+eng')  # 中英文都支持

    # 返回 index.html 并显示识别结果
    return render_template('index.html', ocr_text=text)

if __name__ == '__main__':
    app.run
