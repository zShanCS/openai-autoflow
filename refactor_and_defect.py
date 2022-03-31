'''
Code refactoring in Java and defect detection in C/C++
'''
import torch
from transformers import RobertaTokenizer, T5ForConditionalGeneration

device = torch.device(
    'cuda') if torch.cuda.is_available() else torch.device('cpu')

tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base')

defect_det = T5ForConditionalGeneration.from_pretrained('models/defect').to(device)
refiner = T5ForConditionalGeneration.from_pretrained('models/refine').to(device)


def refine(code):
    input_ids = tokenizer(code, return_tensors="pt").input_ids.to(device)
    # simply generate a single sequence
    generated_ids = refiner.generate(input_ids,
                                     max_length=int(input_ids.shape[1] * 1.5))
    out = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return out


def detect_defect(code):
    input_ids = tokenizer(code, return_tensors="pt").input_ids.to(device)
    generated_ids = defect_det.generate(
        input_ids, max_length=input_ids.shape[1])
    has_defect = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return has_defect
