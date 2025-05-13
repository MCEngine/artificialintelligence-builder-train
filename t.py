import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import joblib
from torch.utils.data import DataLoader, TensorDataset, random_split

# Load dataset
df = pd.read_csv("ai_blocks.csv")

# Encode type labels
df["type_encoded"] = df["type"].astype("category").cat.codes
label_mapping = dict(enumerate(df["type"].astype("category").cat.categories))
joblib.dump(label_mapping, "labels.joblib")

# Convert to tensors
X = torch.tensor(df[["x", "y", "z", "block"]].values, dtype=torch.float32)
y = torch.tensor(df["type_encoded"].values, dtype=torch.long)

# Create dataset and split
dataset = TensorDataset(X, y)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=1024, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1024)

# Define model
class BlockClassifier(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(BlockClassifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, output_dim)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        return self.fc2(x)

model = BlockClassifier(input_dim=4, output_dim=len(label_mapping))

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(10):
    model.train()
    total_loss = 0
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

# Save model
torch.save(model.state_dict(), "model.pt")
print("Model saved to model.pt")
