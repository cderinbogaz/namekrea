import gpt_2_simple as gpt2
import os

model_name = "355M"
if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(model_name=model_name)  # model is saved into current directory under /models/124M/

file_name = "../scraper/data/meta_context.csv"

sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              file_name,
              model_name=model_name,
              multi_gpu=True,
              steps=1000, save_every=10)  # steps is max number of training steps

gpt2.generate(sess)