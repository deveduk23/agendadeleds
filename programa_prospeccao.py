#!/usr/bin/env python3
"""Programa de prospecção semi-automática (WhatsApp) com foco em organização.

Não envia mensagens automaticamente: apenas organiza lista, sugere textos e controla cadência.
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

HEADERS = [
    "nome",
    "empresa",
    "segmento",
    "origem_lead",
    "temperatura",
    "status",
    "ultima_interacao",
    "proxima_acao",
    "opt_out",
]

STATUS_NOVO = "novo"
STATUS_ENVIADO_1 = "enviado_1"
STATUS_RESPONDEU = "respondeu"
STATUS_FOLLOW_1 = "follow_1"
STATUS_FOLLOW_2 = "follow_2"
STATUS_FECHADO = "fechado"
STATUS_SEM_INTERESSE = "sem_interesse"

MENSAGENS_1 = [
    "Fala, tudo bem?\n\nTrabalho com fornecimento de aço na região (chapas, tubos e perfis), com corte sob medida.\n\nSe fizer sentido, te mando uma cotação rápida 👊\n\nSe preferir não receber mensagens, me avisa.",
    "Olá, tudo certo?\n\nSou da Trucar Metal Center e atuamos com fornecimento de aço na região.\n\nSe vocês usam chapa ou tubo, posso ajudar com preço e prazo 👍\n\nSe não fizer sentido, encerro por aqui.",
    "Fala, tudo bem?\n\nAtendo empresas com fornecimento de aço (chapas, tubos e perfis), com entrega rápida e material cortado.\n\nSe tiver demanda, fico à disposição 👊\n\nSe quiser, removo seu contato da lista.",
]

MENSAGEM_FOLLOW_1 = (
    "Fala, tudo certo?\n\n"
    "Só reforçando meu contato caso tenham alguma demanda de material esses dias; "
    "consigo te atender rápido 👊"
)

MENSAGEM_FOLLOW_2 = (
    "Passando pela última vez para não te incomodar. "
    "Se quiser, deixo meus contatos para quando surgir demanda."
)


@dataclass
class Lead:
    nome: str
    empresa: str
    segmento: str
    origem_lead: str
    temperatura: str
    status: str
    ultima_interacao: str
    proxima_acao: str
    opt_out: str


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def ensure_csv(path: Path) -> None:
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=HEADERS).writeheader()


def load_leads(path: Path) -> list[Lead]:
    ensure_csv(path)
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    leads: list[Lead] = []
    for row in rows:
        leads.append(Lead(**{k: row.get(k, "") for k in HEADERS}))
    return leads


def save_leads(path: Path, leads: Iterable[Lead]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        for l in leads:
            writer.writerow(l.__dict__)


def cmd_add(args: argparse.Namespace) -> None:
    leads = load_leads(args.arquivo)
    leads.append(
        Lead(
            nome=args.nome,
            empresa=args.empresa,
            segmento=args.segmento,
            origem_lead=args.origem,
            temperatura=args.temperatura,
            status=STATUS_NOVO,
            ultima_interacao="",
            proxima_acao="enviar_1_contato",
            opt_out="nao",
        )
    )
    save_leads(args.arquivo, leads)
    print("Lead adicionado com sucesso.")


def _selecionar_leads(leads: list[Lead], limite: int) -> list[Lead]:
    candidatos = [
        l
        for l in leads
        if l.opt_out.lower() != "sim" and l.status in {STATUS_NOVO, STATUS_ENVIADO_1, STATUS_FOLLOW_1}
    ]
    return candidatos[:limite]


def _mensagem_para_status(status: str) -> str:
    if status == STATUS_NOVO:
        return random.choice(MENSAGENS_1)
    if status == STATUS_ENVIADO_1:
        return MENSAGEM_FOLLOW_1
    return MENSAGEM_FOLLOW_2


def cmd_bloco(args: argparse.Namespace) -> None:
    leads = load_leads(args.arquivo)
    selecionados = _selecionar_leads(leads, args.limite)
    if not selecionados:
        print("Nenhum lead elegível para o bloco.")
        return

    print(f"Bloco sugerido: {len(selecionados)} contatos")
    print("Sugestão: enviar manualmente e aguardar 10–15 min antes do próximo bloco.\n")

    for i, lead in enumerate(selecionados, 1):
        print(f"[{i}] {lead.nome} | {lead.empresa} | status={lead.status}")
        print(_mensagem_para_status(lead.status))
        print("-" * 60)


def cmd_registrar(args: argparse.Namespace) -> None:
    leads = load_leads(args.arquivo)
    alvo = None
    for l in leads:
        if l.nome.lower() == args.nome.lower() and l.empresa.lower() == args.empresa.lower():
            alvo = l
            break
    if alvo is None:
        print("Lead não encontrado.")
        return

    alvo.ultima_interacao = now_iso()
    if args.evento == "enviado":
        if alvo.status == STATUS_NOVO:
            alvo.status = STATUS_ENVIADO_1
            alvo.proxima_acao = "follow_up_1"
        elif alvo.status == STATUS_ENVIADO_1:
            alvo.status = STATUS_FOLLOW_1
            alvo.proxima_acao = "follow_up_2"
        elif alvo.status == STATUS_FOLLOW_1:
            alvo.status = STATUS_FOLLOW_2
            alvo.proxima_acao = "aguardar"
    elif args.evento == "respondeu":
        alvo.status = STATUS_RESPONDEU
        alvo.proxima_acao = "qualificar"
    elif args.evento == "sem_interesse":
        alvo.status = STATUS_SEM_INTERESSE
        alvo.proxima_acao = "encerrar"
    elif args.evento == "opt_out":
        alvo.opt_out = "sim"
        alvo.status = STATUS_SEM_INTERESSE
        alvo.proxima_acao = "nao_contatar"
    elif args.evento == "fechado":
        alvo.status = STATUS_FECHADO
        alvo.proxima_acao = "pos_venda"

    save_leads(args.arquivo, leads)
    print("Status atualizado.")


def cmd_kpi(args: argparse.Namespace) -> None:
    leads = load_leads(args.arquivo)
    total = len(leads)
    enviados = sum(l.status in {STATUS_ENVIADO_1, STATUS_FOLLOW_1, STATUS_FOLLOW_2, STATUS_RESPONDEU, STATUS_FECHADO} for l in leads)
    respondeu = sum(l.status in {STATUS_RESPONDEU, STATUS_FECHADO} for l in leads)
    fechados = sum(l.status == STATUS_FECHADO for l in leads)

    taxa_resposta = (respondeu / enviados * 100) if enviados else 0
    taxa_fechamento = (fechados / respondeu * 100) if respondeu else 0

    print(f"Total de leads: {total}")
    print(f"Leads com contato enviado: {enviados}")
    print(f"Leads que responderam: {respondeu}")
    print(f"Leads fechados: {fechados}")
    print(f"Taxa de resposta: {taxa_resposta:.1f}%")
    print(f"Taxa de fechamento sobre respostas: {taxa_fechamento:.1f}%")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Gestor de prospecção semi-automática")
    p.add_argument("--arquivo", type=Path, default=Path("leads.csv"), help="CSV de leads")

    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Adicionar lead")
    add.add_argument("--nome", required=True)
    add.add_argument("--empresa", required=True)
    add.add_argument("--segmento", default="geral")
    add.add_argument("--origem", default="manual")
    add.add_argument("--temperatura", default="frio")
    add.set_defaults(func=cmd_add)

    bloco = sub.add_parser("bloco", help="Gerar próximo bloco de mensagens")
    bloco.add_argument("--limite", type=int, default=5)
    bloco.set_defaults(func=cmd_bloco)

    reg = sub.add_parser("registrar", help="Registrar evento de interação")
    reg.add_argument("--nome", required=True)
    reg.add_argument("--empresa", required=True)
    reg.add_argument("--evento", required=True, choices=["enviado", "respondeu", "sem_interesse", "opt_out", "fechado"])
    reg.set_defaults(func=cmd_registrar)

    kpi = sub.add_parser("kpi", help="Mostrar indicadores")
    kpi.set_defaults(func=cmd_kpi)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
