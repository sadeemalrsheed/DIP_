import tensorflow as tf

try:
    import tensorflowjs as tfjs
    print("✅ tensorflowjs imported successfully")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nInstall using: pip install tensorflowjs")
    exit()

print("\nLoading model...")
model = tf.keras.models.load_model('final_model_transfer_learning.keras')
print("✅ Model loaded!")

print(f"\nInput shape: {model.input_shape}")
print(f"Output shape: {model.output_shape}")
print(f"Number of classes: {model.output_shape[-1]}")

print("\nConverting to TensorFlow.js...")
tfjs.converters.save_keras_model(model, 'model_tfjs')

print("✅ DONE! Check 'model_tfjs' folder")