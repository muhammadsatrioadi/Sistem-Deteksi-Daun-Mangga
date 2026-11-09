import os
from flask import Flask, render_template, request
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ================= CONFIG =================
UPLOAD_FOLDER = "static/uploads"
CONF_THRESHOLD = 0.4

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= LOAD MODEL =================
model = YOLO("best.pt")

print("Model berhasil dimuat")
print("Class model:", model.names)


# ================= DATA REKOMENDASI =================
def get_recommendation(label):

    data = {

        "Anthracnoce": {
            "nama": "Antraknosa",
            "deskripsi": "Antraknosa adalah penyakit pada tanaman mangga yang disebabkan oleh jamur Colletotrichum gloeosporioides. Penyakit ini umumnya menyerang daun, bunga, dan buah, dengan gejala berupa bercak hitam atau coklat yang dapat meluas dan menyebabkan jaringan membusuk. Berikut merupakan rekomendasi penanganan yang dapat dilakukan untuk mengatasi penyakit tersebut.",
            "penanganan": [
                "Penyemprotan fungisida seperti mancozeb, carbendazim, atau azoxystrobin.",
                "Pengendalian biologis menggunakan agen hayati seperti Candida tropicalis atau Aureobasidium pullulans.",
                "Perlakuan panas pascapanen dengan merendam buah dalam air panas untuk menghambat pertumbuhan jamur.",
                "Sanitasi tanaman dengan membuang bagian yang terinfeksi untuk mencegah penyebaran."
            ]
        },

        "Bacterial Canker": {
            "nama": "Bacterial Canker",
            "deskripsi": "Bacterial canker merupakan penyakit yang disebabkan oleh bakteri Xanthomonas campestris yang menyerang daun, batang, dan buah mangga, dengan gejala berupa bercak hitam yang dikelilingi warna kuning serta dapat menyebabkan daun berlubang dan mengering. Berikut merupakan rekomendasi penanganan yang dapat dilakukan untuk mengatasi penyakit tersebut.",
            "penanganan": [
                "Pemangkasan bagian tanaman yang terinfeksi seperti daun dan ranting.",
                "Sanitasi kebun dengan mengumpulkan dan memusnahkan daun yang terinfeksi.",
                "Penggunaan bakterisida seperti streptomycin atau copper oxychloride secara berkala.",
                "Pengendalian biologis menggunakan mikroorganisme seperti Bacillus atau Pseudomonas."
            ]
        },

        "Powdery Mildew": {
            "nama": "Powdery Mildew",
            "deskripsi": "Powdery mildew adalah penyakit yang disebabkan oleh jamur Oidium mangiferae yang ditandai dengan lapisan putih seperti tepung pada permukaan daun dan dapat menghambat pertumbuhan tanaman. Berikut merupakan rekomendasi penanganan yang dapat dilakukan untuk mengatasi penyakit tersebut.",
            "penanganan": [
                "Penyemprotan fungisida berbahan sulfur atau kalium bikarbonat.",
                "Mengurangi kelembapan lingkungan tanaman.",
                "Memastikan tanaman mendapatkan sinar matahari yang cukup.",
                "Sanitasi dengan membuang bagian tanaman yang terinfeksi."
            ]
        }

    }

    return data.get(label)

# ================= HALAMAN UTAMA =================
@app.route("/")
def index():
    return render_template("index.html")


# ================= DETEKSI =================
@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return "Tidak ada file yang diupload"

    file = request.files["image"]

    if file.filename == "":
        return "File belum dipilih"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    label = "Tidak Terdeteksi"
    confidence = 0

    try:

        results = model.predict(
            source=filepath,
            conf=0.4
        )

        boxes = results[0].boxes

        if boxes is not None and len(boxes) > 0:

            confs = boxes.conf.cpu().numpy()
            classes = boxes.cls.cpu().numpy()

            best_index = confs.argmax()
            best_conf = confs[best_index]

            if best_conf >= CONF_THRESHOLD:

                label_index = int(classes[best_index])
                label = model.names[label_index]
                confidence = float(best_conf)

        print("Hasil Deteksi:", label, confidence)

    except Exception as e:
        return f"Terjadi error saat prediksi: {e}"

    disease = get_recommendation(label)

    return render_template(
        "result.html",
        image=filename,
        disease=disease,
        label=label,
        confidence=round(confidence * 100, 2)
    )


# ================= RUN APP =================
if __name__ == "__main__":
    app.run(debug=True)