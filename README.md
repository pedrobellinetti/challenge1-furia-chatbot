
# 🤖 FURIA Fan Chatbot (Telegram Bot)

Este é um bot do Telegram desenvolvido para os fãs da equipe de CS:GO **FURIA**. Ele fornece atualizações automáticas sobre:

- Partidas passadas e futuras
- Curiosidades da equipe
- Notícias recentes (via Liquipedia)
- Agendamento de lembretes para partidas
- Atualizações diárias personalizadas

## Funcionalidades

- `/start` — Boas-vindas e instruções
- `/historico_partidas` — Mostra partidas anteriores e seus resultados
- `/partidas_futuras` — Exibe as próximas partidas
- `/lembrar_partida` — Agenda lembrete para partidas futuras
- `/agendar HH:MM` — Define um horário fixo para notificações diárias
- `/curiosidades` — Exibe fatos interessantes sobre a FURIA
- `/noticias` — Busca notícias em tempo real da equipe via Liquipedia

## Instalação

1. Clone ou baixe este repositório:
   ```bash
   git clone https://github.com/seuusuario/furia-bot.git
   cd furia-bot/challenge1-furia-fan-chatbot
   ```

2. Crie um ambiente virtual e ative:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` e adicione seu token do bot:
   ```env
   TOKEN=seu_token_do_bot_aqui
   ```

## Executando o bot

```bash
python app.py
```

## Estrutura do Projeto

```
challenge1-furia-fan-chatbot/
├── app.py                     # Código principal do bot
├── buscar_partidas_furia.py  # Função de scraping via API da Liquipedia
├── lembretes.py              # Funções para agendamento e lembretes
├── .env                      # Contém o token do bot
├── requirements.txt          # Dependências
└── README.md                 # Este arquivo
```

## Tecnologias Usadas

- Python 3.12+
- python-telegram-bot
- BeautifulSoup (web scraping)
- APScheduler (agendamento de tarefas)
- dotenv (gerenciamento de variáveis de ambiente)

---

Feito com 💛 para os fãs da FURIA!
