export BASEPATH=/home/yuningm2/citesum
export TASK_NAME=scitldr
export RUN_NAME=scitldr_continuous_ThispaperREF
export WANDB_PROJECT=citesum
export WANDB_RUN_GROUP=fewshot
export TOKENIZERS_PARALLELISM=false
export MODEL_PATH=CiteSum-ckpt

python $BASEPATH/run_seq2seq.py \
    --model_name_or_path $MODEL_PATH  \
    --do_train \
    --do_eval \
    --do_predict \
    --task_name $TASK_NAME\
    --train_file $BASEPATH/data/$TASK_NAME/train_ThispaperREF.json \
    --validation_file $BASEPATH/data/$TASK_NAME/val.json \
    --test_file $BASEPATH/data/$TASK_NAME/test.json \
    --output_dir $BASEPATH/output/scitldr/$RUN_NAME \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=64 \
    --evaluation_strategy steps \
    --save_strategy steps \
    --save_total_limit 1 \
    --early_stopping_patience 5 \
    --metric_for_best_model rouge2 \
    --max_steps 1600 \
    --logging_steps 50 \
    --eval_steps 50 \
    --save_steps 1000 \
    --run_name $RUN_NAME \
    --overwrite_output_dir \
    --learning_rate 1e-5 \
    --report_to wandb \
    --load_best_model_at_end True \
    --predict_with_generate \
    --generation_max_length 45 \
    --generation_min_length 10 \
    --generation_num_beams 1 \
    --num_beams 1 \
    --max_train_samples 872
    # --gradient_accumulation_steps 2
    # --max_source_length 512 \