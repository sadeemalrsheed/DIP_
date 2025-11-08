"""
🧪 اختبار المودل مباشرة - نفس الطريقة اللي درّبت فيها
"""

from tensorflow import keras # type: ignore
import numpy as np # type: ignore
from PIL import Image # type: ignore

# تحميل المودل
print("⏳ Loading model...")
model = keras.models.load_model('final_model_transfer_learning.keras')
print("✅ Model loaded!")

# معلومات المودل
print(f"\n📊 Model Info:")
print(f"Input shape: {model.input_shape}")
print(f"Output shape: {model.output_shape}")

# فحص الطبقة الأولى
print(f"\nFirst layer: {model.layers[0].name}")
print(f"Model expects: {model.input_shape}")

# اسماء الكلاسات (مختصرة)
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

print(f"\n🔢 Number of classes: {len(class_names)}")
print(f"Model output neurons: {model.output_shape[-1]}")

if len(class_names) != model.output_shape[-1]:
    print("⚠️ WARNING: Class names count doesn't match model output!")

# جرب صورة تجريبية
print("\n" + "="*60)
print("🧪 TEST: Random array (simulating an image)")
print("="*60)

# إنشاء مصفوفة عشوائية
test_array = np.random.rand(1, 224, 224, 3).astype(np.float32)

# اختبار 1: Raw values [0, 1]
print("\n1️⃣ Test with raw values [0, 1]:")
pred1 = model.predict(test_array, verbose=0)
top3_1 = np.argsort(pred1[0])[-3:][::-1]
for i, idx in enumerate(top3_1, 1):
    print(f"   {i}. {class_names[idx]}: {pred1[0][idx]*100:.2f}%")

# اختبار 2: Scaled to [-1, 1] (MobileNet style)
print("\n2️⃣ Test with scaled values [-1, 1]:")
test_array_scaled = (test_array - 0.5) * 2  # [0,1] -> [-1,1]
pred2 = model.predict(test_array_scaled, verbose=0)
top3_2 = np.argsort(pred2[0])[-3:][::-1]
for i, idx in enumerate(top3_2, 1):
    print(f"   {i}. {class_names[idx]}: {pred2[0][idx]*100:.2f}%")

# اختبار 3: معالجة MobileNet الرسمية
print("\n3️⃣ Test with MobileNetV2 preprocessing:")
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
test_array_mobilenet = preprocess_input(test_array.copy() * 255)  # Back to [0,255] then preprocess
pred3 = model.predict(test_array_mobilenet, verbose=0)
top3_3 = np.argsort(pred3[0])[-3:][::-1]
for i, idx in enumerate(top3_3, 1):
    print(f"   {i}. {class_names[idx]}: {pred3[0][idx]*100:.2f}%")

print("\n" + "="*60)
print("📝 Instructions:")
print("="*60)
print("1. Run this script: python test_model.py")
print("2. Check which preprocessing gives the MOST VARIED results")
print("3. That's the correct preprocessing for your model!")
print("\nIf all 3 tests give similar results (always Lettuce),")
print("then the model itself needs retraining.")
print("="*60)