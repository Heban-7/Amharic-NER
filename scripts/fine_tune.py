import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer
from datasets import Dataset
from seqeval.metrics import classification_report
import numpy as np

# Define model names

# Step Load and preprocess the dataset
def load_conll_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    sentences, labels = [], []
    current_sentence, current_labels = [], []
    for line in lines:
        if line.strip() == "":
            if current_sentence:
                sentences.append(current_sentence)
                labels.append(current_labels)
                current_sentence, current_labels = [], []
        else:
            parts = line.strip().split()
            if len(parts) == 2:
                current_sentence.append(parts[0])
                current_labels.append(parts[1])
    if current_sentence:
        sentences.append(current_sentence)
        labels.append(current_labels)
    return sentences, labels

# Convert data into Hugging Face dataset
def prepare_dataset(sentences, labels):
    dataset_dict = {"tokens": sentences, "ner_tags": labels}
    return Dataset.from_dict(dataset_dict)

# Tokenize and align labels
def tokenize_and_align_labels(example, tokenizer, label_to_id):
    tokenized_inputs = tokenizer(example["tokens"], truncation=True, is_split_into_words=True)
    word_ids = tokenized_inputs.word_ids()
    
    previous_word_idx = None
    aligned_labels = []
    for word_idx in word_ids:
        if word_idx is None:
            aligned_labels.append(-100)
        elif word_idx != previous_word_idx:
            aligned_labels.append(label_to_id[example["ner_tags"][word_idx]])
        else:
            aligned_labels.append(-100)
        previous_word_idx = word_idx
    tokenized_inputs["labels"] = aligned_labels
    return tokenized_inputs

# Train and evaluate model
def train_and_evaluate(model_name, train_dataset, val_dataset, id_to_label):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=len(id_to_label))
    
    training_args = TrainingArguments(
        output_dir=f"./results_{model_name}",
        evaluation_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        save_strategy="epoch",
        logging_dir=f"./logs_{model_name}",
        load_best_model_at_end=True,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer
    )
    trainer.train()
    predictions, labels, _ = trainer.predict(val_dataset)
    predictions = np.argmax(predictions, axis=2)
    true_labels = [[id_to_label[l] for l in label if l != -100] for label in labels]
    pred_labels = [[id_to_label[p] for p, l in zip(pred, label) if l != -100] for pred, label in zip(predictions, labels)]
    print(f"Evaluation for {model_name}")
    print(classification_report(true_labels, pred_labels))
    return trainer


