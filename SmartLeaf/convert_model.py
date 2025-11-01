
import os
import sys
import argparse
import tensorflow as tf

try:
    from tensorflowjs.converters import save_keras_model
except Exception as e:
    print("❌ Could not import tensorflowjs converter.\n"
          "   Make sure you installed:\n"
          "     pip install --no-deps tensorflowjs==4.21.0\n"
          "     pip install tf-keras==2.15.0\n"
          f"   Details: {e}")
    sys.exit(1)

BAR = "═" * 72

def _shape(obj):
    try:
        return tuple(obj) if isinstance(obj, (list, tuple)) else tuple(obj.shape)
    except Exception:
        try:
            return tuple(obj.as_list())
        except Exception:
            return obj

def get_io_shapes(model):
    try:
        in_shape = model.input_shape
    except Exception:
        in_shape = [_shape(t) for t in model.inputs]
    try:
        out_shape = model.output_shape
    except Exception:
        out_shape = [_shape(t) for t in model.outputs]
    return in_shape, out_shape

def guess_num_classes(out_shape):
    try:
        s = out_shape[0] if isinstance(out_shape, list) else out_shape
        last = s[-1]
        if isinstance(last, int) and last > 1:
            return last
    except Exception:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Convert Keras model to TensorFlow.js (model.json + shards)."
    )
    parser.add_argument("-m", "--model", default="final_model_transfer_learning.keras",
                        help="Path to .keras/.h5 file or SavedModel directory.")
    parser.add_argument("-o", "--out", default="model_tfjs",
                        help="Output directory (default: model_tfjs).")
    args = parser.parse_args()

    model_path = args.model
    out_dir = args.out

    print(BAR)
    print("CONVERTING KERAS MODEL TO TENSORFLOW.JS")
    print(BAR)
    print(f"🧩 TensorFlow version : {tf.__version__}")
    print(f"📄 Model path         : {os.path.abspath(model_path)}")
    print(f"📁 Output directory   : {os.path.abspath(out_dir)}")

    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        sys.exit(1)

    # 1) Load model
    print("\n📦 Loading model...")
    try:
        model = tf.keras.models.load_model(model_path)
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        sys.exit(1)

    # 2) Info
    in_shape, out_shape = get_io_shapes(model)
    n_classes = guess_num_classes(out_shape)
    print("\n📊 Model Information:")
    print(f"   Input shape : {in_shape}")
    print(f"   Output shape: {out_shape}")
    print(f"   Num classes : {n_classes if n_classes else 'N/A'}")

    print("\n🧱 Model Summary:")
    try:
        model.summary()
    except Exception:
        print("   (summary not available)")

    # 3) Convert
    print("\n🔁 Converting to TFJS...")
    os.makedirs(out_dir, exist_ok=True)
    try:
        save_keras_model(model, out_dir)
        print(f"✅ Converted. Saved to: {os.path.abspath(out_dir)}")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        sys.exit(1)

    # 4) List output
    print("\n📂 Generated files:")
    for name in sorted(os.listdir(out_dir)):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"   - {name} ({size_mb:.2f} MB)")

    print("\n" + BAR)
    print("🎉 CONVERSION COMPLETE")
    print(BAR)
    print("\nNext steps:")
    print(f"1) Move '{out_dir}' beside your index.html (or adjust the path).")
    print(f"2) In JS: const model = await tf.loadLayersModel('{out_dir}/model.json');")
    print( "3) Ensure your image preprocessing matches the model input size (H×W×C).")

if __name__ == "__main__":
    main()

