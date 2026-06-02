# Aurora Fashion Club — CRM e Retenção com Dados Sintéticos

Projeto de portfólio para simular uma varejista omnichannel de moda com foco em CRM, retenção, recorrência, churn, LTV e campanhas.

## O que este repositório entrega

- geração sintética coerente para `customers`, `products`, `orders`, `order_items`, `campaigns`, `interactions`, `support_tickets` e `digital_events`;
- persistência em `CSV`, `XLSX`, `JSON`, `SQLite` e camadas `bronze`, `silver`, `gold`;
- validação básica de integridade referencial;
- base pronta para EDA, segmentação, churn e LTV.

## Como executar

```bash
python -m src.pipeline
```

Parâmetros úteis:

```bash
python -m src.pipeline --n-customers 10000 --n-products 1500 --n-campaigns 250 --seed 7
```

## Estrutura

```text
aurora_fashion_club/
├── data/
├── notebooks/
├── src/
└── README.md
```

## Próximos passos sugeridos

1. criar notebook de EDA;
2. criar notebook de RFM e segmentação;
3. treinar um baseline de churn;
4. estimar LTV;
5. construir dashboard executivo.
