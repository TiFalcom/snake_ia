import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x


    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()


    def train_step(self, state, acao, recompensa, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        acao = torch.tensor(acao, dtype=torch.long)
        recompensa = torch.tensor(recompensa, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            acao = torch.unsqueeze(acao, 0)
            recompensa = torch.unsqueeze(recompensa, 0)
            game_over = (game_over, )

        pred = self.model(state)

        target = pred.clone()

        for idx in range(len(game_over)):
            Q_new = recompensa[idx]
            if not game_over[idx]:
                Q_new = recompensa[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(acao).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()

