import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from tqdm import tqdm

from model import CNNTransformer
from dataset_loader import ASVspoofDataset


def main():
    BATCH_SIZE = 8
    EPOCHS = 12
    LR = 3e-4
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.backends.cudnn.benchmark = True


    TRAIN_PROTOCOL = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"
    DEV_PROTOCOL   = "../data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.dev.trl.txt"

    TRAIN_AUDIO = "../data/LA/ASVspoof2019_LA_train/flac"
    DEV_AUDIO   = "../data/LA/ASVspoof2019_LA_dev/flac"

    CHECKPOINT_PATH = "../checkpoints/best_model.pth"
    os.makedirs("../checkpoints", exist_ok=True)

    train_dataset = ASVspoofDataset(TRAIN_PROTOCOL, TRAIN_AUDIO, training=True)
    dev_dataset   = ASVspoofDataset(DEV_PROTOCOL, DEV_AUDIO, training=False)

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=2,
        pin_memory=True
    )

    dev_loader = DataLoader(
        dev_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=2,
        pin_memory=True
    )
    import time

    print("Testing dataloader speed...")
    start = time.time()

    for i, (mel, wave, labels) in enumerate(train_loader):
        if i == 20:
           print("20 batches took:", time.time() - start, "seconds")
           break


    model = CNNTransformer().to(DEVICE)

    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=LR)

    best_val_loss = float("inf")

    print("Using device:", DEVICE)
    print("Model on:", next(model.parameters()).device)

    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0

        for mel, wave, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Train]"):
            mel = mel.unsqueeze(1).to(DEVICE, non_blocking=True)
            wave = wave.to(DEVICE, non_blocking=True)
            labels = labels.to(DEVICE, non_blocking=True)

            optimizer.zero_grad()

            outputs = model(mel, wave)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        # ----- Validation -----
        model.eval()
        val_loss = 0

        with torch.no_grad():
            for mel, wave, labels in tqdm(dev_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Val]"):
                mel = mel.unsqueeze(1).to(DEVICE)
                wave = wave.to(DEVICE)
                labels = labels.to(DEVICE)

                outputs = model(mel, wave)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

        print(f"Epoch {epoch+1} | Train Loss: {train_loss/len(train_loader):.4f} | Val Loss: {val_loss/len(dev_loader):.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                "model_state": model.state_dict(),
            }, CHECKPOINT_PATH)
            print("Saved best model")


if __name__ == "__main__":
    main()
