# Máquina de Prospecção (Semi-automática, com foco em conformidade)

Este playbook transforma prospecção por WhatsApp em rotina escalável **sem comportamento de spam**.

## 1) Princípios de segurança e conformidade

- Use apenas contatos com base legal adequada (consentimento, relação comercial prévia ou legítimo interesse bem documentado).
- Respeite LGPD e políticas do WhatsApp Business.
- Ofereça opt-out claro em toda abordagem.
- Nunca use automação total para disparos em massa.

> Objetivo: **conversa útil e contextual**, não volume cego.

## 2) Estrutura mínima do funil

Planilha/CRM com campos:

- `nome`
- `empresa`
- `segmento`
- `origem_lead`
- `temperatura` (frio/morno/quente)
- `status` (novo, enviado_1, respondeu, follow_1, follow_2, fechado, sem_interesse)
- `ultima_interacao`
- `proxima_acao`

## 3) Cadência recomendada

### Dia 1 — 1º contato
- Blocos de 5 contatos
- Intervalo de 10–15 minutos entre blocos
- No máximo 20–40 contatos/dia para número novo
- No máximo 40–60 contatos/dia para número aquecido

### Dia 2 — Follow-up 1
Somente para quem não respondeu.

### Dia 4 — Follow-up 2 (encerramento leve)
Mensagem curta com saída elegante.

## 4) Templates (com variação)

## 4.1 Primeiro contato (3 variações)

### V1
> Fala, tudo bem?  
> Trabalho com fornecimento de aço na região (chapas, tubos e perfis), com corte sob medida.  
> Se fizer sentido pra vocês, te mando uma cotação rápida por aqui. 👊  
> Se preferir não receber mensagens, me avisa que removo seu contato.

### V2
> Olá, tudo certo?  
> Sou da Trucar Metal Center e atendemos empresas com fornecimento de aço na região.  
> Se vocês usam chapa/tubo/perfil, posso apoiar com preço e prazo. 👍  
> Se não for o momento, sem problema — posso encerrar por aqui.

### V3
> Fala, tudo bem?  
> Atendo empresas com fornecimento de aço (chapas, tubos e perfis), com entrega rápida e material cortado.  
> Se tiver alguma demanda esta semana, fico à disposição. 👊  
> Caso não queira receber contato, é só me sinalizar.

## 4.2 Follow-up 1 (D+1)
> Oi, tudo certo?  
> Só reforçando meu contato caso tenham alguma demanda de material nesses dias — consigo retorno rápido de preço e prazo. 👊

## 4.3 Follow-up 2 (D+3)
> Passando pela última vez para não te incomodar.  
> Se quiser, deixo meus contatos salvos para quando surgir demanda de aço.  
> Se preferir, encerro por aqui.

## 5) Versões por segmento

## 5.1 Metalúrgica
- Dor comum: falta de previsibilidade de prazo.
- Gancho: corte sob medida + regularidade de entrega.

Mensagem:
> Atendemos metalúrgicas com chapa/tubo/perfil sob medida e prazo previsível.  
> Quer que eu te envie uma condição base para itens de giro?

## 5.2 Obra / Construção
- Dor comum: atraso de cronograma.
- Gancho: disponibilidade e logística.

Mensagem:
> Fornecemos aço para obras com foco em disponibilidade e entrega ágil para não travar cronograma.  
> Se quiser, te passo prazo real para os itens que vocês mais compram.

## 5.3 Manutenção industrial
- Dor comum: urgência e parada de produção.
- Gancho: atendimento rápido e reposição.

Mensagem:
> No atendimento de manutenção, nosso foco é retorno rápido para demanda urgente de chapa/tubo/perfil.  
> Se você me passar um item exemplo, já te retorno com prazo e preço.

## 6) Rotina diária (execução)

### 08:30–09:00
- Revisar pipeline e separar 15–30 leads do dia.
- Escolher variação de mensagem por segmento.

### 09:00–11:00
- Envio em blocos + registro de cada envio no CRM.
- Responder qualquer retorno em até 5–10 minutos.

### 14:00–15:00
- Follow-ups de D+1.

### 16:30–17:00
- Atualizar status e preparar lista do próximo dia.

## 7) Regras de ouro anti-bloqueio

- Não repetir texto idêntico para todos.
- Evitar links no primeiro toque.
- Evitar anexos pesados em massa.
- Priorizar conversa real (perguntas curtas e úteis).
- Parar disparos quando o volume de resposta subir.
- Responder rapidamente quem engajar.

## 8) KPIs simples para escalar

- Taxa de resposta = respostas / contatos enviados
- Taxa de qualificação = leads qualificados / respostas
- Taxa de reunião/cotação = reuniões ou cotações / qualificados
- Tempo médio de primeira resposta

Ajuste semanal:
- Se taxa de resposta < 10%: revisar copy e segmentação.
- Se resposta alta e qualificação baixa: ajustar ICP/lista.
- Se qualificação alta e fechamento baixo: melhorar proposta e follow-up comercial.
