import gpt_2_simple as gpt2
import os

checkpoint_dir="../krea_brain/checkpoint"
model_name = '355M'

if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(model_name=model_name)  # model is saved into current directory under /models/124M/

sess = gpt2.start_tf_sess()
# After 3 hours of debugging I have realised that you need to put also the checkpoint_dir under generate.

gpt2.load_gpt2(sess,
              # run_name=run_name,
              # checkpoint_dir=checkpoint_dir,
              model_name=model_name,
              model_dir='models',
              multi_gpu=True)

gpt2.generate(sess, model_name=model_name,
              #run_name=run_name, checkpoint_dir=checkpoint_dir,
              temperature=0.8, include_prefix=True, prefix='Hacker, news',
              truncate='<|endoftext|>', nsamples=10, batch_size=2, length=128
              )
