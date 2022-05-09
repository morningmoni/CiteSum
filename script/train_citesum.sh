export BASEPATH=/home/yuningm2/citesum
export TASK_NAME=citesum
export RUN_NAME=$TASK_NAME-bart
export WANDB_PROJECT=citesum
export WANDB_RUN_GROUP=train-large
export TOKENIZERS_PARALLELISM=false


python $BASEPATH/run_seq2seq.py \
    --model_name_or_path facebook/bart-large \
    --do_train \
    --do_eval \
    --do_predict \
    --task_name $TASK_NAME\
    --train_file $BASEPATH/data/$TASK_NAME/train.json \
    --validation_file $BASEPATH/data/$TASK_NAME/val.json \
    --test_file $BASEPATH/data/$TASK_NAME/test.json \
    --output_dir $BASEPATH/output/$RUN_NAME \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --evaluation_strategy steps \
    --max_steps 200000 \
    --save_strategy steps \
    --save_total_limit 3 \
    --early_stopping_patience 5 \
    --metric_for_best_model rouge2 \
    --logging_steps 500 \
    --eval_steps 5000 \
    --save_steps 5000 \
    --run_name $RUN_NAME \
    --overwrite_output_dir \
    --learning_rate 2e-5 \
    --report_to wandb \
    --load_best_model_at_end True \
    --predict_with_generate \
    --generation_max_length 100 \
    --generation_min_length 10 \
    --generation_num_beams 1 \
    --num_beams 1 \
    --gradient_accumulation_steps 1 \
    --fp16 True \
