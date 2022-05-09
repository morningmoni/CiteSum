import gzip
import io
import json
import pickle
from multiprocessing import Pool
from tqdm import tqdm


def chunks(l, n):
    n = len(l) // n
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def multi_runs(f, para, f_combine=None, n=10):
    with Pool(n) as pool:
        res = pool.map(f, para)
        if f_combine is not None:
            res = f_combine(res)
        return res


def read_pdf_parse(para2):
    fname, valid_paper_id = para2
    data = []
    with gzip.open(fname, 'rb') as gz:
        f = io.BufferedReader(gz)
        for line in tqdm(f.readlines()):
            d = json.loads(line)
            if d['paper_id'] in valid_paper_id:
                data.append(d)
    return data


def read_pdf_parse_wt(fname):
    '''
    save papers with full text access
    :param fname:
    :return:
    '''
    id2abs = {}
    with gzip.open(fname, 'rb') as gz, gzip.open(fname + '.abs_body', 'wt') as o:
        f = io.BufferedReader(gz)
        for line in tqdm(f.readlines()):
            d = json.loads(line)
            if len(d['abstract']) > 0:
                id2abs[d['paper_id']] = d['abstract']
                if len(d['body_text']) > 0 and len(d['bib_entries']) > 0:
                    o.write(json.dumps(d) + '\n')
    pickle.dump(id2abs, open(fname + '.id2abs.pkl', 'wb'))
    return id2abs


def save_pdf_parse_R(fname):
    """
    save papers that contain related work section pdf data
    :param fname:
    """
    valid_papers = []
    # all inputs have abstract and body_text
    with gzip.open(fname + '.abs_body', 'rt') as f:
        for line in tqdm(f):
            d = json.loads(line)
            if any('related work' in para['section'].lower() for para in d['body_text']):
                valid_papers.append(d)
    print(f'len(valid_papers)={len(valid_papers)}')
    pickle.dump(valid_papers, open(fname + '.valid_papers.pkl', 'wb'))


def extract_IC(d):
    I = []
    C = []
    for para in d['body_text']:
        if 'introduction' == para['section'].lower():
            I.append(para['text'])
        elif 'conclusion' == para['section'].lower():
            C.append(para['text'])

    if len(I) == 0:
        for para in d['body_text']:
            if 'introduction' in para['section'].lower():
                I.append(para['text'])
    if len(C) == 0:
        for para in d['body_text']:
            if 'conclusion' in para['section'].lower():
                C.append(para['text'])

    return ' '.join(I), ' '.join(C)


def save_pdf_parse_IC(fname):
    """
    save papers that contain related work section pdf data
    :param fname:
    """
    id2AIC = {}
    # all inputs have abstract and body_text
    with gzip.open(fname + '.abs_body', 'rt') as f:
        n_I = n_C = n_IC = n_I_or_C = 0
        for line in tqdm(f):
            d = json.loads(line)
            I, C = extract_IC(d)
            id2AIC[d['paper_id']] = (I, C)
            if len(I) > 0:
                n_I += 1
            if len(C) > 0:
                n_C += 1
            if len(I) > 0 and len(C) > 0:
                n_IC += 1
            if len(I) > 0 or len(C) > 0:
                n_I_or_C += 1

    print(f'n_I, n_C, n_IC, n_I_or_C={n_I, n_C, n_IC, n_I_or_C}')
    pickle.dump(id2AIC, open(fname + '.id2IC.pkl', 'wb'))


def read_metadata_domain(fname):
    '''
    save id2domain, a dict that maps id to paper domain_related fields
    :param fname:
    :return:
    '''
    id2domain = {}
    with gzip.open(fname, 'rb') as gz:
        f = io.BufferedReader(gz)
        for line in tqdm(f.readlines()):
            d = json.loads(line)
            if d['has_pdf_parse'] and d['has_pdf_parsed_abstract'] and d['has_pdf_parsed_body_text'] and d[
                'has_pdf_parsed_bib_entries']:
                if d['mag_field_of_study']:
                    fields = {k: d[k] for k in ['venue', 'journal', 'mag_field_of_study']}
                    id2domain[d['paper_id']] = fields

    pickle.dump(id2domain, open(fname + '.id2domain.pkl', 'wb'))

def read_metadata_title(fname):
    '''
    save id2title
    :param fname:
    :return:
    '''
    id2title = {}
    with gzip.open(fname, 'rb') as gz:
        f = io.BufferedReader(gz)
        for line in tqdm(f.readlines()):
            d = json.loads(line)
            if d['has_pdf_parse'] and d['has_pdf_parsed_abstract'] and d['has_pdf_parsed_body_text'] and d[
                'has_pdf_parsed_bib_entries']:
                id2title[d['paper_id']] = d['title']

    pickle.dump(id2title, open(fname + '.id2title.pkl', 'wb'))


def combine_dict(res):
    res_total = {}
    for d in res:
        res_total.update(d)
    return res_total


if __name__ == '__main__':
    N = 25
    batches = [{'input_metadata_path': f"20200705v1/full/metadata/metadata_{idx}.jsonl.gz",
                'output_metadata_path': f"20200705v1/full/metadata/metadata_{idx}.filtered.jsonl",
                'input_pdf_parses_path': f"20200705v1/full/pdf_parses/pdf_parses_{idx}.jsonl.gz",
                'output_pdf_parses_path': f"20200705v1/full/pdf_parses/pdf_parses_{idx}.filtered.jsonl", }
               for idx in range(0, 100)]
    # id2abs = multi_runs(read_pdf_parse_wt, para=[b['input_pdf_parses_path'] for b in batches],
    #                     n=N)
    multi_runs(read_metadata_title, para=[b['input_metadata_path'] for b in batches], n=N)
    # multi_runs(save_pdf_parse_IC, para=[b['input_pdf_parses_path'] for b in batches], n=N)
