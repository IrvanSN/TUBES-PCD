import os
import time
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__, static_folder='uploads')

app.secret_key = '2030234082342'
app.config['SESSION_TYPE'] = 'filesystem'

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_proccessing(image_path):
  # Buka gambar
  im = Image.open(image_path)
  width, height = im.size
  print(width)

  # Ubah menjadi grayscale
  im = im.convert('L')

  # Ubah setiap pixel menjadi simbol sesuai dengan ketentuan
  pixels = np.array(im)
  pixels = pixels.astype(str)
  for x in range(min(width, pixels.shape[0])):
    for y in range(min(height, pixels.shape[1])):
      pixel = pixels[x, y]
      if int(pixel) >= 0 and int(pixel) <= 22:
          pixels[x, y] = '@ '
      elif int(pixel) >= 23 and int(pixel) <= 45:
          pixels[x, y] = '$ '
      elif int(pixel) >= 46 and int(pixel) <= 68:
          pixels[x, y] = '# '
      elif int(pixel) >= 69 and int(pixel) <= 89:
          pixels[x, y] = '* '
      elif int(pixel) >= 90 and int(pixel) <= 112:
          pixels[x, y] = '! '
      elif int(pixel) >= 113 and int(pixel) <= 135:
          pixels[x, y] = '= '
      elif int(pixel) >= 136 and int(pixel) <= 158:
          pixels[x, y] = '; '
      elif int(pixel) >= 159 and int(pixel) <= 181:
          pixels[x, y] = ': '
      elif int(pixel) >= 182 and int(pixel) <= 204:
          pixels[x, y] = '~ '
      elif int(pixel) >= 205 and int(pixel) <= 227:
          pixels[x, y] = '- '
      else:
          pixels[x, y] = '. '
  file = open(image_path + '.rtf',"w")

  # Cetak teks simbol
  for x in range(min(width, pixels.shape[0])):
    for y in range(min(height, pixels.shape[1])):
        file.write(pixels[x, y])
    file.write('\n')

  file.close

@app.route('/')
def home():
  return render_template('home.html')
    
@app.route('/upload-image', methods = ['POST'])
def upload_image():
  if request.method == 'POST':
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url) 
    if file and allowed_file(file.filename):
      epoch_time = int(time.time())
      filename = secure_filename(str(epoch_time) + '-' + file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      image_proccessing('uploads/' + filename)
      return redirect(url_for('result', name=filename + '.rtf'))

@app.route('/result', methods = ['POST', 'GET'])
def result():
    args = request.args
    with open('uploads/' + args.get("name"), 'r') as f: 
      return render_template('result.html', text=f.read())

if __name__ == "__main__":
    app.run(host="0.0.0.0")