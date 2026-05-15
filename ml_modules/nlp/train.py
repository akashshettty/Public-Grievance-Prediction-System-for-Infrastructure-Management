"""
Training Script for Complaint Classification
Fine-tunes DistilBERT on Bengaluru Grievance Data.
"""

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComplaintDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def train_model(data_path, output_dir="models/nlp_classifier"):
    # 1. Load Data
    logger.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)
    
    # We use 'issue_type' as the text and 'category' as label
    # or combined text
    df['text_combined'] = df['issue_type'] + " " + df['sub_category'].fillna('')
    df = df[['text_combined', 'category']].dropna()
    
    # Encode Labels
    le = LabelEncoder()
    df['label_idx'] = le.fit_transform(df['category'])
    num_labels = len(le.classes_)
    
    # Save label encoder for inference
    import pickle
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)
        
    # 2. Split Data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['text_combined'].tolist(), 
        df['label_idx'].tolist(), 
        test_size=0.2,
        random_state=42
    )

    # 3. Tokenization
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

    # 4. Create Datasets
    train_dataset = ComplaintDataset(train_encodings, train_labels)
    val_dataset = ComplaintDataset(val_encodings, val_labels)

    # 5. Initialize Model
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=num_labels)

    # 6. Training Arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True
    )

    # 7. Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    # 8. Train
    logger.info("Starting training...")
    trainer.train()
    
    # 9. Save Best Model
    logger.info(f"Saving model to {output_dir}")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    return model, tokenizer

if __name__ == "__main__":
    # Path to the processed data
    DATA_PATH = "data/processed/grievances_cleaned.csv"
    if os.path.exists(DATA_PATH):
        # We limit the training data for demonstration or if resources are low
        # In real scenario, use the full dataset
        train_model(DATA_PATH)
    else:
        logger.error(f"Data file not found at {DATA_PATH}")
