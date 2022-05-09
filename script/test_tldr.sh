export BASEPATH=/home/yuningm2/citesum
export TASK_NAME=scitldr
export RUN_NAME=test-$TASK_NAME-zeroshot
export WANDB_PROJECT=citesum
export WANDB_RUN_GROUP=test
export TOKENIZERS_PARALLELISM=false
export MODEL_PATH=CiteSum-ckpt


python $BASEPATH/run_seq2seq.py \
    --model_name_or_path $MODEL_PATH  \
    --do_predict \
    --task_name $TASK_NAME\
    --test_file $BASEPATH/data/$TASK_NAME/test.json \
    --output_dir $BASEPATH/output/scitldr/test/$RUN_NAME \
    --per_device_eval_batch_size=64 \
    --run_name $RUN_NAME \
    --report_to wandb \
    --predict_with_generate \
    --generation_min_length 10 \
    --generation_max_length 45 \
    --num_beams 1 \
    --use_prompt True