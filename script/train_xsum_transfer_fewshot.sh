export BASEPATH=/home/yuningm2/citesum
export TASK_NAME=xsum
export RUN_NAME=$TASK_NAME-train1000_bart
export WANDB_PROJECT=citesum
export WANDB_RUN_GROUP=fewshot
export TOKENIZERS_PARALLELISM=false
export MODEL_PATH=CiteSum-ckpt

python $BASEPATH/run_seq2seq.py \
    --save_script train_xsum_transfer_fewshot.sh \
    --data_seed 420 \
    --model_name_or_path $MODEL_PATH \
    --do_train \
    --do_eval \
    --do_predict \
    --task_name $TASK_NAME\
    --dataset_name $TASK_NAME \
    --output_dir $BASEPATH/output/xsum/$RUN_NAME \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --evaluation_strategy steps \
    --save_strategy steps \
    --save_total_limit 1 \
    --early_stopping_patience 3 \
    --metric_for_best_model rouge2 \
    --max_steps 1200 \
    --logging_steps 120 \
    --eval_steps 240 \
    --save_steps 240 \
    --run_name $RUN_NAME \
    --overwrite_output_dir \
    --learning_rate 5e-5 \
    --report_to wandb \
    --load_best_model_at_end True \
    --predict_with_generate \
    --generation_max_length 62 \
    --generation_min_length 11 \
    --generation_num_beams 1 \
    --num_beams 6 \
    --max_train_samples 1000 \
    --max_eval_samples 1000 \
    --fp16 True \
