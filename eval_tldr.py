import os

'''
Evaluate SciTLDR by its original script (which takes max of multiple references)
'''

def eval_res(pred_file, ref_file):
    cmd = f'python "scitldr/scripts/cal-rouge.py" {pred_file} {ref_file} --workers 40 > tldr_results.txt'
    os.system(cmd)

def post_process_zeroshot_REF(fname):
    with open(fname + '.postprocessed', 'w') as o:
        for line in open(fname):
            line = line.replace('In REF,', '')
            if line.startswith('REF'):
                line = line.replace('REF', 'this paper')
            else:
                line = line.replace('REF', '')
            line = line.replace('REF', '')
            o.write(line.strip() + '\n')

pred_file = "output/scitldr/test/test-scitldr-zeroshot/generated_predictions.txt"
post_process_zeroshot_REF(pred_file)
pred_file = pred_file + '.postprocessed'
ref_file = "scitldr/SciTLDR-Data/SciTLDR-A/test.jsonl"
eval_res(pred_file, ref_file)
with open('tldr_results.txt') as f:
    for line in f:
        if '||multi-max' in line:
            print(line.strip())
print()