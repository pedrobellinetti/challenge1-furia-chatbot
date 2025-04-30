from buscar_partidas_furia import *
from app import *

async def lembrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /lembrar 1 (por exemplo, para a 1ª partida listada)")
        return
    
    try:
        idx = int(context.args[0]) - 1 
        partidas = context.chat_data["partidas_futuras", []]
        
        if idx < 0 or idx >= len(partidas):
            await update.message.reply_text("Número inválido")
            return
        
        partida_str = partidas[idx]
        
        # Extrair data e hora do texto
        
        data_txt = partida_str.split("|")[0].replace("📅", "").strip()
        
        try:
            data_partida = parser.parse(data_txt, dayfirst = True)
            
        except Exception as e:
            await update.message.reply_text("Não consegui interpretar a data da partida.")
            return
        
        lembrar_partida(update, context, data_partida, partida_str) 
        await update.message.reply_text(f"Lembrete agendado para {data_partida.strftime('%d%m%Y %H:%M')}")
        
    except Exception as e:
        await update.message.reply_text("Ocorreu um erro ao processar o lembrete.")
        print("Erro no /lembrar: \n", e)
        
        
        