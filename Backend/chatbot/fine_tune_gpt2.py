##################################################
# 1) Imports et définitions utiles
##################################################
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset
import os

##################################################
# 2) Main : chargement du modèle, des données, fine-tuning
##################################################
def main():
    # 2.1 Charger le modèle Flan-T5-Small et le tokenizer
    model_name = "google/flan-t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # 2.2 Vérification des fichiers JSON (train et validation)
    train_file = "train.json"
    valid_file = "valid.json"
    
    if not os.path.exists(train_file):
        raise FileNotFoundError(f"Fichier d'entraînement introuvable : {train_file}")
    if not os.path.exists(valid_file):
        raise FileNotFoundError(f"Fichier de validation introuvable : {valid_file}")

    # Charger les datasets JSON
    dataset = load_dataset(
        'json',
        data_files={
            'train': train_file,
            'validation': valid_file
        }
    )

    ##############################################################
    # 2.3 Définir une fonction de prétraitement pour formater les données
    ##############################################################
    def preprocess_function(examples):
        inputs = []
        targets = []
        for instruction, user_text, bot_text in zip(examples["instruction"], examples["user"], examples["bot"]):
            # Construire l'input en incluant l'instruction, la question utilisateur et la balise pour la réponse
            input_text = f"{instruction}\n<USER>: {user_text}\n<BOT>:"
            inputs.append(input_text)
            # La cible (target) est la réponse attendue
            targets.append(bot_text)
        model_inputs = tokenizer(inputs, truncation=True, max_length=256, padding="max_length")
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(targets, truncation=True, max_length=150, padding="max_length")
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    # Appliquer le prétraitement au dataset
    tokenized_dataset = dataset.map(
        preprocess_function,
        batched=True,
        num_proc=4,
        remove_columns=["instruction", "user", "bot"]
    )

    ###################################################
    # 2.4 Configuration du data collator pour Seq2Seq
    ###################################################
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    ###################################################
    # 2.5 Configuration du Trainer et lancement du fine-tuning
    ###################################################
    training_args = TrainingArguments(
        output_dir="./results",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_steps=100,
        learning_rate=5e-5,
        warmup_steps=100
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        data_collator=data_collator
    )

    print("---------- Début du fine-tuning ----------")
    trainer.train()
    print("---------- Fine-tuning terminé ----------")

    # Sauvegarder le modèle et le tokenizer finetunés
    model_dir = "./flan-t5-small-finetuned"
    model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)
    print(f">>> Modèle et tokenizer sauvegardés dans '{model_dir}'")

##################################################
# 3) Le bloc indispensable sous Windows
##################################################
if __name__ == '__main__':
    main()
