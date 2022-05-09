export BASEPATH=/home/yuningm2/citesum
export TASK_NAME=gigaword
export RUN_NAME=test-$TASK_NAME-cites-beam32
export WANDB_PROJECT=citesum
export WANDB_RUN_GROUP=test
export TOKENIZERS_PARALLELISM=false
export MODEL_PATH=CiteSum-ckpt


python $BASEPATH/run_seq2seq.py \
    --save_script test_gigaword.sh \
    --model_name_or_path $MODEL_PATH  \
    --do_predict \
    --task_name $TASK_NAME\
    --test_file $BASEPATH/data/$TASK_NAME/test.json \
    --output_dir $BASEPATH/output/gigaword/test/$RUN_NAME \
    --per_device_eval_batch_size=64 \
    --run_name $RUN_NAME \
    --report_to wandb \
    --predict_with_generate \
    --generation_min_length 4 \
    --generation_max_length 24 \
    --num_beams 32\
    --use_prompt False