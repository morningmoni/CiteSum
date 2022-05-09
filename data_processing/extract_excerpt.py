import pickle
from collections import defaultdict

from tqdm import tqdm, trange

import spacy

from data_processing.read_data import multi_runs

nlp = spacy.load("en_core_sci_sm")


def view_related_work_simple(data):
    related_work_subsec = []
    status = 'not_yet'
    for idx, para in enumerate(data['body_text']):
        if 'related work' in para['section'].lower():
            related_work_subsec.append(para)
            status = 'ongoing'
        elif status == 'ongoing':
            status = 'passed'
            break
    return related_work_subsec


def paras2str(paras):
    return ' '.join(para['text'] for para in paras)


def extract_excerpt(pdf_data_source_fname, add_IC=True,
                    add_cur_paper_as_input=True, add_cite_num=True, display=False, min_abs_char=100):
    pdf_data_source = pickle.load(open(pdf_data_source_fname + '.valid_papers.pkl', 'rb'))
    id_source = range(len(pdf_data_source))

    id2data = {}  # input paper, output related work sent
    id2r = {}  # paper -> its related work section
    id2c = defaultdict(list)  # paper -> where it is cited
    n_examples = 0
    for cur_id in tqdm(list(id_source)[:]):
        if display:
            print(f'cur_id={cur_id}')

        cur_abs = paras2str(pdf_data_source[cur_id]['abstract'])
        bib_entries = pdf_data_source[cur_id]['bib_entries']
        if bib_entries is None:
            continue
        input_l = []
        output_l = []

        data = pdf_data_source[cur_id]
        related_work_subsec = view_related_work_simple(data)
        #         related_work_subsec = view_related_work(data, display, debug=False)
        id2r[cur_id] = related_work_subsec
        for ct, para in enumerate(related_work_subsec):
            if len(para['cite_spans']) > 0:
                cite_idx = 0
                doc = nlp(para['text'])
                for sent in doc.sents:
                    input_l.append([])
                    if add_cur_paper_as_input:
                        input_l[-1].append(cur_abs)
                    has_cite = []
                    if display:
                        print(sent.text)
                    while cite_idx < len(para['cite_spans']) and sent.start_char <= para['cite_spans'][cite_idx][
                        'start'] and \
                            para['cite_spans'][cite_idx]['end'] <= sent.end_char:
                        if display:
                            print(para['cite_spans'][cite_idx])
                        ref_id = para['cite_spans'][cite_idx]['ref_id']
                        if ref_id in bib_entries:
                            cited_paper = bib_entries[ref_id]
                            cited_paper_id = cited_paper['link']
                            if cited_paper_id in id2abs and len(paras2str(id2abs[cited_paper_id])) > min_abs_char:
                                has_cite.append(True)
                                if add_cite_num:
                                    input_l[-1].append(para['cite_spans'][cite_idx]['text'])
                                input_l[-1].append(paras2str(id2abs[cited_paper_id]))

                                id2c[cited_paper_id].append(
                                    {'paper_id': cur_id, 'cite_span': para['cite_spans'][cite_idx], 'text': sent.text})
                                if display:
                                    print(cited_paper_id, paras2str(id2abs[cited_paper_id]))
                                    print()
                            else:
                                has_cite.append(False)
                        cite_idx += 1
                    # only save the example if all cited papers have abs
                    if len(has_cite) > 0 and all(has_cite):
                        output_l.append(sent.text)
                    else:
                        input_l.pop()
                    if display:
                        # TODO the cited sent could be about "Our work" but we ignore them for now
                        print(colored(f"our/we in sent={'our' in sent.text.lower() or 'we ' in sent.text.lower()}",
                                      'red'))
                        print()
            if display:
                print('=' * 20, 'new para', '=' * 20)

        assert len(input_l) == len(output_l)
        if len(input_l) > 0:
            id2data[cur_id] = (input_l, output_l)
            n_examples += len(input_l)
    print(f'#abs-excerpt examples={n_examples}  #cited papers={len(id2c)}')
    pickle.dump((id2data, id2r, id2c), open(pdf_data_source_fname + '.excerpt.pkl', 'wb'))
    return id2data, id2r, id2c


if __name__ == '__main__':
    N = 2
    batches = [{'input_metadata_path': f"20200705v1/full/metadata/metadata_{idx}.jsonl.gz",
                'output_metadata_path': f"20200705v1/full/metadata/metadata_{idx}.filtered.jsonl",
                'input_pdf_parses_path': f"20200705v1/full/pdf_parses/pdf_parses_{idx}.jsonl.gz",
                'output_pdf_parses_path': f"20200705v1/full/pdf_parses/pdf_parses_{idx}.filtered.jsonl", }
               for idx in range(0, 2)]

    id2abs = {}
    for i in trange(100):
        d = pickle.load(open(f"20200705v1/full/pdf_parses/pdf_parses_{i}.jsonl.gz.id2abs.pkl", 'rb'))
        id2abs.update(d)
    multi_runs(extract_excerpt, para=[b['input_pdf_parses_path'] for b in batches],
               n=N)
