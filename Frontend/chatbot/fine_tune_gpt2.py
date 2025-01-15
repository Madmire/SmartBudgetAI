##################################################
# 1) Imports et définitions utiles
##################################################
from transformers import (
    GPTNeoForCausalLM,
    GPT2TokenizerFast,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
    EarlyStoppingCallback
)
from datasets import load_dataset
import logging

# Configurer la journalisation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

##################################################
# 2) Main : chargement du modèle, des données, fine-tuning
##################################################
def main():
    # 2.1 Charger le modèle EleutherAI/gpt-neo-125M et le tokenizer
    model_name = "EleutherAI/gpt-neo-125M"  # Variante GPT-Neo 125M
    tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
    
    # Ajouter des tokens spéciaux pour structurer les échanges
    special_tokens = {"additional_special_tokens": ["[INSTRUCTION]", "[USER]", "[BOT]"]}
    tokenizer.add_special_tokens(special_tokens)
    
    # Charger le modèle pré-entraîné
    model = GPTNeoForCausalLM.from_pretrained(model_name)
    # Redimensionner les embeddings pour inclure les nouveaux tokens
    model.resize_token_embeddings(len(tokenizer))
    
    # Utiliser le token EOS comme token de padding
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id

    # 2.2 Charger le dataset JSON (train.json et valid.json)
    dataset = load_dataset(
        'json',
        data_files={
            'train': 'train.json',
            'validation': 'valid.json'
        }
    )
    
    ##############################################################
    # 2.3 Prétraitement des données
    ##############################################################
    def preprocess_function(examples):
        """
        Concaténer l'instruction, la question et la réponse en utilisant les tokens spéciaux.
        """
        inputs = []
        for instruction, user_text, bot_text in zip(examples["instruction"], examples["user"], examples["bot"]):
            combined_text = f"[INSTRUCTION] {instruction}\n[USER]: {user_text}\n[BOT]: {bot_text}"
            inputs.append(combined_text)
        return tokenizer(
            inputs,
            truncation=True,
            max_length=512,
            padding="max_length"
        )
    
    # Appliquer le prétraitement au dataset
    tokenized_dataset = dataset.map(
        preprocess_function,
        batched=True,
        num_proc=4,  # Ajustez le nombre de processus selon vos cœurs disponibles
        remove_columns=["instruction", "user", "bot"]
    )
    
    ###################################################
    # 2.4 Configuration du data collator
    ###################################################
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # GPT-Neo n'utilise pas le masquage (Masked Language Modeling)
    )
    
    ###################################################
    # 2.5 Configuration du Trainer et lancement du fine-tuning
    ###################################################
    training_args = TrainingArguments(
        output_dir="./results",
        overwrite_output_dir=True,
        num_train_epochs=4,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,  # Simule un batch de plus grande taille
        per_device_eval_batch_size=2,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_steps=100,
        learning_rate=5e-5,
        warmup_steps=100,
        load_best_model_at_end=True  # Pour utiliser EarlyStoppingCallback
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        data_collator=data_collator,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )
    
    logger.info("---------- Début du fine-tuning ----------")
    trainer.train()
    logger.info("---------- Fine-tuning terminé ----------")
    
    # Sauvegarder le modèle et le tokenizer finetunés
    model.save_pretrained("./EleutherAI-gpt-neo-125M-finetuned")
    tokenizer.save_pretrained("./EleutherAI-gpt-neo-125M-finetuned")
    logger.info(">>> Modèle et tokenizer sauvegardés dans './EleutherAI-gpt-neo-125M-finetuned'")

##################################################
# 3) Bloc indispensable sous Windows
##################################################
if __name__ == '__main__':
    main()
