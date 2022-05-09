export BASEPATH=/home/yuningm2/citesum
export TASK_NAME=xsum
export RUN_NAME=test-$TASK_NAME-zeroshot-pegasus
export WANDB_PROJECT=citesum
export WANDB_RUN_GROUP=test
export TOKENIZERS_PARALLELISM=false
export MODEL_PATH=CiteSum-ckpt


python $BASEPATH/run_seq2seq.py \
    --save_script test_xsum.sh \
    --model_name_or_path $MODEL_PATH  \
    --do_predict \
    --task_name $TASK_NAME\
    --dataset_name $TASK_NAME \
    --output_dir $BASEPATH/output/xsum/test/$RUN_NAME \
    --per_device_eval_batch_size=16 \
    --run_name $RUN_NAME \
    --report_to wandb \
    --predict_with_generate \
    --generation_max_length 62 \
    --generation_min_length 11 \
    --num_beams 4 \
    --use_prompt False
