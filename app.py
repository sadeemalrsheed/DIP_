"""
🌿 SmartLeaf - Simple Python API
No conversion needed! Use your Keras model directly.
"""

from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
from tensorflow import keras # type: ignore
import numpy as np # type: ignore
from PIL import Image # type: ignore
import io
import os

app = Flask(__name__)
CORS(app)  # للسماح بالاتصال من المتصفح

# تحميل المودل عند بداية التطبيق
print("⏳ Loading model...")

# البحث عن ملف المودل
model_file = None
possible_names = [
    'final_model_transfer_learning.keras',
    'final_model_transfer_learning.h5',
    'final*.keras',
    'final*.h5'
]

for name in possible_names:
    if '*' in name:
        import glob
        files = glob.glob(name)
        if files:
            model_file = files[0]
            break
    elif os.path.exists(name):
        model_file = name
        break

if not model_file:
    raise FileNotFoundError("❌ Model file not found! Please add: final_model_transfer_learning.keras")

model = keras.models.load_model(model_file)
print(f"✅ Model loaded: {model_file}")
print(f"📊 Classes: {model.output_shape[-1]}")

# قائمة الكلاسات (نفس الترتيب في script.js)
class_names = [
    "Apple_Apple_scab", "Apple_Black_rot", "Apple_Cedar_apple_rust", "Apple_healthy",
    "Blueberry_healthy", "Cherry_Powdery_mildew", "Cherry_healthy",
    "Corn_Cercospora_leaf_spot Gray_leaf_spot", "Corn_Common_rust_",
    "Corn_Northern_Leaf_Blight", "Corn_healthy", "Cucumber ـBacterialـWilt",
    "Cucumber_Gummy_Stem_Blight", "Cucumber_Pythium_Fruit_Rot",
    "CucumberـAnthracnose", "CucumberـBelly Rot", "CucumberـDownyـMildew",
    "Cucumberـhealthy", "Downy_mildew_on_lettuce", "Grape_Black_rot",
    "Grape_Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape_healthy", "Lemon_Anthracnose", "Lemon_Black_Spot", "Lemon_Citrus_Canker",
    "Lemon_Citrus_Leaf_Miner", "Lemon_Curl_Leaf", "Lemon_Dry_leaf", "Lemon_Greening",
    "Lemon_Healthy", "Lemon_Melanose", "Lettuce_Bacterial", "LettuceـHealthy",
    "LettuceـShepherd_purse_weeds", "Orange_Haunglongbing_(Citrus_greening)",
    "Peach_Bacterial_spot", "Peach_healthy", "Pepper_bell_Bacterial_spot",
    "Pepper_bell_healthy", "Potato_Early_blight", "Potato_Late_blight",
    "Potato_healthy", "Powdery_mildew_on_lettuce", "Septoria_blight_on_lettuce",
    "Soybean___healthy", "Squash_Powdery_mildew", "Strawberry_Leaf_scorch",
    "Strawberry_healthy", "Tomato_Bacterial_spot", "Tomato_Early_blight",
    "Tomato_Late_blight", "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato_Target_Spot",
    "Tomato_Yellow_Leaf_Curl_Virus", "Tomato_healthy", "Tomato_mosaic_virus",
    "Watermelon_Downy_Mildew", "Watermelon_Healthy", "Watermelon_Mosaic_Virus",
    "Wilt_and_leaf_blight_on_lettuce", "banana_Cordana_leaf_spot", "banana_healthy",
    "banana_pestalotiopsis", "banana_sigatoka", "bean_angular_leaf_spot",
    "bean_healthy", "bean_rust", "chili_Bacterial_Spot", "chili_Cercospora_Leaf_Spot",
    "chili_Curl_Virus", "chili_Healthy", "chili_Nutrition_Deficiency",
    "chili_White_spot", "olive_Healthy", "olive_aculus_olearius", "olive_peacock_spot",
    "plam_Black_Scorch", "plam_Fusarium_Wilt", "plam_Healthy", "plam_Leaf_Spots",
    "plam_Magnesium_Deficiency", "plam_Manganese_Deficiency", "plam_Parlatoria_Blanchardi",
    "plam_Potassium_Deficiency", "plam_Rachis_Blight", "plam_infected_by_Bug",
    "plam_infected_by_Dubas", "rice_Bacterial_leaf_blight", "rice_Brown_spot",
    "rice_Leaf_smut", "wheat_leaf_brown_rust", "wheat_stem_black_rust",
    "wheat_strip_yellowrust"
]

def preprocess_image(image_file):
    """معالجة الصورة للمودل"""
    img = Image.open(io.BytesIO(image_file.read())).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def home():
    return """
    <html>
    <head>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; background: #f0f7f4; }
            h1 { color: #457b67; }
            .status { background: #8BC3AE; color: white; padding: 20px; border-radius: 10px; }
        </style>
    </head>
    <body>
        <h1>🌿 SmartLeaf API is Running!</h1>
        <div class="status">
            <p>✅ Server is Ready</p>
            <p>📊 Model: {}</p>
            <p>🔢 Classes: {}</p>
            <p>📝 Use POST /predict to analyze plant images</p>
        </div>
    </body>
    </html>
    """.format(model_file, len(class_names))

@app.route('/predict', methods=['POST'])
def predict():
    """استقبال الصورة والتنبؤ"""
    try:
        # التحقق من وجود صورة
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        
        # معالجة الصورة
        img_array = preprocess_image(image_file)
        
        # التنبؤ
        predictions = model.predict(img_array, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx]) * 100
        
        # النتيجة
        predicted_class = class_names[predicted_class_idx]
        
        return jsonify({
            'success': True,
            'predicted_class': predicted_class,
            'confidence': f"{confidence:.1f}%"
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("✅ SmartLeaf Server is Ready!")
    print("🌐 Open: http://localhost:5000")
    print("📝 Use POST /predict with 'image' file")
    print("="*50 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')