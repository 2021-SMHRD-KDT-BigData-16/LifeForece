def Prediction(test_df):
    
    import numpy as np
    import pandas as pd
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    
    X_test = []
    pid_x = test_df.drop(columns=['p_id', 'Gender']) 
    pid_x = pid_x.astype(float)
    X_test.append(pid_x)
    X_test = np.array(X_test)
    
    model_path = './LFmodel.pt'

    class Attention(nn.Module):
        def __init__(self, hidden_dim):
            super(Attention, self).__init__()
            self.hidden_dim = hidden_dim
            self.attn_weights = nn.Parameter(torch.Tensor(hidden_dim, hidden_dim))
            nn.init.xavier_uniform_(self.attn_weights)

        def forward(self, x):
            attn_scores = torch.matmul(x, self.attn_weights)  # Compute attention scores
            attn_weights = F.softmax(attn_scores, dim=-1)  # Apply softmax to get attention weights
            context_vector = torch.matmul(attn_weights.transpose(-1, -2), x)  # Compute context vector
            return context_vector

    class LifeForce(nn.Module):
        def __init__(self, input_dim, hidden_dim):
            super(LifeForce, self).__init__()
            self.embedding = nn.Linear(input_dim, hidden_dim)
            self.LSTM = nn.LSTM(hidden_dim, hidden_dim, 3)
            self.relu = nn.ReLU()
            self.attention = Attention(hidden_dim)
            self.clf = nn.Linear(hidden_dim, 1)
            self.sigmoid = nn.Sigmoid()

        def forward(self, x):
            x = self.embedding(x)
            x = self.relu(x)
            lstm_output, _ = self.LSTM(x)  # Get LSTM output and hidden state
            x = self.attention(lstm_output)  # Apply attention mechanism to LSTM output
            x = x[:, -1, :]  # Extract the last output from the LSTM sequence
            x = self.clf(x)
            x = self.sigmoid(x)
            return x

    model = LifeForce(40, 128)

    model.load_state_dict(torch.load(model_path))
    
    X_test = torch.Tensor(X_test)
    
    with torch.no_grad():
        # Forward pass to get the predictions
        predictions = model(X_test)  # Assuming you are using GPU (CUDA)

    # Convert the predictions tensor to a NumPy array
    predictions = predictions.cpu().numpy()
    
    return predictions[0][0]*100
