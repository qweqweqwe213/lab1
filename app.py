from flask import Flask, render_template, request
from PIL import Image
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    result_image = None

    if request.method == "POST":

        file = request.files["image"]

        if file:

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            img = Image.open(filepath)

            # график RGB

            img_rgb = img.convert("RGB")

            r = []
            g = []
            b = []

            for pixel in img_rgb.getdata():
                r.append(pixel[0])
                g.append(pixel[1])
                b.append(pixel[2])

            plt.figure(figsize=(8, 4))

            plt.hist(r, bins=256, color='red', alpha=0.5)
            plt.hist(g, bins=256, color='green', alpha=0.5)
            plt.hist(b, bins=256, color='blue', alpha=0.5)

            graph_path = os.path.join(app.config['RESULT_FOLDER'], 'graph.png')

            plt.savefig(graph_path)
            plt.close()

            w, h = img.size

            # части картинки
            A = img.crop((0, 0, w // 2, h // 2))
            B = img.crop((w // 2, 0, w, h // 2))
            C = img.crop((0, h // 2, w // 2, h))
            D = img.crop((w // 2, h // 2, w, h))

            # новая картинка
            new_img = Image.new("RGB", (w, h))

            # сдвиг по часовой стрелке
            new_img.paste(C, (0, 0))
            new_img.paste(A, (w // 2, 0))
            new_img.paste(D, (0, h // 2))
            new_img.paste(B, (w // 2, h // 2))

            result_path = os.path.join(app.config['RESULT_FOLDER'], 'result.jpg')

            new_img.save(result_path)

            result_image = 'results/result.jpg'

    return render_template(
        "index.html",
        result_image=result_image,
        graph_image='results/graph.png'
    )


app.run(debug=True)