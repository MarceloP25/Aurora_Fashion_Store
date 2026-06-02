# CRM e Retenção: Cases Sintéticos para Portfólio

## Objetivo do projeto

Este projeto foi desenhado como um portfólio analítico de alto valor para vagas de Data Science, Analytics, BI, CRM e produtos orientados a dados. A proposta é simular empresas fictícias com desafios realistas de retenção, recorrência, engajamento e personalização, a fim de construir um ambiente de experimentação completo para exploração analítica, SQL, modelagem preditiva e recomendação de ações.

A abordagem não é a de um notebook isolado. O projeto será tratado como um produto de dados, com visão de negócio, backlog, hipóteses, regras de domínio, dicionário de dados e critérios de sucesso. A meta é gerar dados sintéticos coerentes, persistidos em múltiplos formatos, para permitir análises em Python, SQL e ferramentas de BI.

---

## Estrutura conceitual do projeto

Cada case será construído com a seguinte lógica de produto:

1. Contexto estratégico da empresa e posicionamento no mercado.
2. Problema de negócio detalhado e sintoma operacional.
3. Causas prováveis e hipóteses de investigação.
4. Objetivo esperado pela área de CRM, produto ou retenção.
5. Regras de negócio e comportamento esperado dos dados.
6. Dicionário de dados e granularidade da base.
7. Backlog inicial de análises, modelagens e entregáveis.
8. Critérios de sucesso e métricas de validação.

A partir disso, a base sintética será gerada de forma estruturada e exportada nos formatos `.csv`, `.xlsx`, `.json` e SQLite.

---

# Case — Aurora Fashion Club

## 1.1 Visão da empresa

Aurora Fashion Club é uma varejista omnichannel de moda feminina e masculina que opera com três frentes de relacionamento: e-commerce, aplicativo próprio e lojas físicas. O posicionamento da marca é intermediário-premium, com apelo forte em conveniência, lançamentos frequentes e coleções sazonais. O modelo de receita é baseado em compra recorrente, recorrência por categoria, fidelização via benefícios e ativação de base por campanhas promocionais.

A operação comercial depende de uma combinação de aquisição, retenção e aumento de ticket médio. O negócio trabalha com:
- aquisição de clientes por mídia paga, influenciadores, social commerce e campanhas sazonais;
- venda de produtos com alto giro e sensibilidade relevante a preço e desconto;
- programa de fidelidade com benefícios progressivos por faixa de gasto;
- jornadas integradas entre app, site e loja física;
- comunicação recorrente por e-mail, SMS, push e remarketing;
- estratégia comercial baseada em coleção, sazonalidade e reposição de inventário.

O comportamento do cliente é especialmente relevante para a operação porque moda tem alto componente emocional, forte competição entre marcas e grande dependência de percepção de valor. A experiência de compra, a entrega, a comunicação e a relevância da campanha interferem diretamente na retenção.

## 1.2 Cenário de negócio

A empresa cresceu de forma acelerada em aquisição nos últimos trimestres, impulsionada por campanhas promocionais e mídia digital. No entanto, esse crescimento veio acompanhado de deterioração na qualidade da base ativa. A expansão não foi convertida na mesma proporção em recorrência, retenção e lifetime value.

A área de CRM passou a observar uma queda consistente na recompra após a segunda compra, baixa ativação no programa de fidelidade e redução da eficiência das campanhas de relacionamento. O problema não está apenas em gerar novas compras, mas em sustentar um relacionamento rentável com o cliente ao longo do tempo.

Em paralelo, surgiram sinais claros de fadiga de comunicação. Clientes com alta exposição a campanhas começaram a responder menos, o uso do app caiu, e os segmentos mais recentes da base passaram a abandonar o relacionamento muito antes do sexto mês de vida. Parte da base compra uma vez, retorna uma segunda vez e depois entra em inatividade ou migra para concorrentes com maior agressividade promocional.

A operação também enfrenta um problema de pressão sobre margem. Para sustentar volume, a empresa vem aumentando desconto, o que melhora conversão no curto prazo, mas piora rentabilidade e pode atrair um público mais oportunista do que fiel.

## 1.3 Problema de negócio

O problema central deste case não é apenas churn. O problema é a falta de inteligência para entender em que ponto da jornada o relacionamento se deteriora e quais alavancas realmente explicam esse comportamento.

Hoje, o time de CRM sabe que há perda de recorrência, mas não consegue responder com segurança:
- se a aquisição está atraindo clientes pouco qualificados;
- se a primeira experiência de compra está gerando fricção;
- se a comunicação está sendo excessiva, irrelevante ou mal segmentada;
- se o uso excessivo de desconto está canibalizando margens e fidelidade;
- se a ausência de personalização por estilo, faixa de gasto e ciclo de vida está reduzindo o retorno das campanhas;
- se existe ruptura entre canais digitais e lojas físicas que afeta a repetição de compra.

A companhia hoje trata a base como se ela fosse homogênea. Na prática, isso faz com que campanhas de retenção sejam genéricas e com baixa capacidade de resposta. Clientes de alto valor recebem a mesma comunicação que clientes oportunistas, clientes recém-adquiridos recebem as mesmas ofertas que clientes inativos e segmentos premium são estimulados com estímulos pouco sofisticados. O resultado é baixo aproveitamento da base e desperdício de investimento promocional.

## 1.4 Sintomas observáveis

Os sintomas que indicam o problema são os seguintes:
- queda de recompra após a segunda compra;
- aumento do intervalo médio entre pedidos;
- baixa ativação de clientes recém-adquiridos;
- redução da frequência de acesso ao app;
- queda na taxa de abertura e clique em campanhas;
- baixa adesão ao programa de fidelidade;
- forte sensibilidade de parte da base a desconto;
- retenção menor em clientes adquiridos por mídia paga de baixo valor;
- clientes premium com potencial subexplorado;
- campanhas promocionais com conversão inferior ao esperado;
- devoluções acima do desejado em determinados perfis e categorias.

## 1.5 Hipóteses de investigação

A investigação deve partir de hipóteses claras e acionáveis:
- clientes com alta dependência de desconto têm maior risco de churn;
- clientes com menor diversidade de categorias compradas possuem menor retenção;
- clientes que interagem pouco com o app têm menor probabilidade de recompra;
- clientes com maior exposição a campanhas sem conversão tendem a apresentar fadiga de comunicação;
- campanhas genéricas convertem menos do que campanhas segmentadas por estilo, faixa de gasto e ciclo de vida;
- clientes de maior valor respondem melhor a benefícios de exclusividade do que a cupons agressivos;
- clientes com alta taxa de devolução tendem a repetir menos compras;
- perfis adquiridos em determinados canais podem ter qualidade distinta de lifetime value.

## 1.6 Objetivo do produto de dados

O objetivo do produto analítico é permitir ao time de CRM e Growth operar com uma visão preditiva e segmentada da base. O produto precisa apoiar decisões do tipo:
- quem tem maior risco de abandono;
- quais fatores antecedem a queda de recorrência;
- como agrupar clientes por comportamento real;
- qual jornada faz sentido para cada segmento;
- qual é o melhor estímulo para cada grupo;
- onde vale investir retenção, onde vale priorizar reativação e onde vale proteger margem.

Em termos práticos, a solução deve sair de uma lógica reativa para uma lógica orientada por probabilidade, valor e contexto de relacionamento.

## 1.7 Escopo funcional esperado

A solução deste case deverá permitir:
- leitura da jornada completa do cliente, do primeiro contato à recompra;
- visão unificada de compras, canais, campanhas e comportamento digital;
- geração de score de risco de churn;
- cálculo de lifetime value;
- segmentação de clientes por perfil de comportamento;
- identificação de grupos com maior sensibilidade a desconto;
- priorização de campanhas por valor esperado;
- recomendação de ações por segmento;
- monitoramento de desempenho de retenção ao longo do tempo.

## 1.8 Backlog de produto

### Épico 1 — Fundamentos da base e qualidade do dado
Objetivo: garantir que a base represente de forma confiável a jornada do cliente.
- identificar inconsistências cadastrais;
- padronizar datas, faixas e categorias;
- garantir coerência entre primeira compra, última compra e número de pedidos;
- estruturar regras para clientes ativos, inativos e churnados;
- validar relações entre campanhas recebidas e comportamento observado.

### Épico 2 — Jornada e comportamento de compra
Objetivo: entender como o cliente evolui ao longo da relação com a marca.
- mapear recência, frequência e monetização;
- medir tempo entre compras;
- identificar padrões de recompra por canal;
- analisar comportamento por categoria e faixa de gasto;
- detectar queda de engajamento ao longo do ciclo de vida.

### Épico 3 — Segmentação de clientes
Objetivo: criar grupos acionáveis para CRM.
- estruturar um modelo RFM;
- separar clientes por valor, frequência e recência;
- identificar clientes sensíveis a promoção;
- identificar clientes premium;
- identificar clientes de risco;
- gerar clusters comportamentais para campanhas específicas.

### Épico 4 — Predição de churn
Objetivo: antecipar abandono e perda de recorrência.
- definir target de churn;
- criar features de engajamento, compras e campanhas;
- avaliar modelos de classificação para risco de churn;
- calcular score por cliente;
- priorizar listas de retenção.

### Épico 5 — LTV e priorização comercial
Objetivo: definir onde a empresa deve concentrar esforço.
- estimar lifetime value;
- combinar LTV com churn risk;
- identificar contas/segmentos mais valiosos;
- orientar priorização de campanhas e jornadas;
- estabelecer régua de investimento por tipo de cliente.

### Épico 6 — Recomendação de ações de CRM
Objetivo: transformar análise em decisão.
- recomendar tipo de campanha;
- sugerir canal ideal;
- indicar frequência de contato;
- propor ações de reativação;
- propor ações de fidelização;
- propor ações de cross-sell e upsell.

## 1.9 Critérios de sucesso

O case será considerado bem-sucedido se conseguir demonstrar:
- redução da invisibilidade sobre o comportamento de recompra;
- clareza sobre quais clientes têm maior risco de sair;
- identificação de segmentos acionáveis para campanhas;
- conexão entre engajamento digital e retenção;
- capacidade de transformar o dado em ação comercial;
- recomendação de intervenções diferentes para perfis diferentes.


## 1.10 Dicionário de dados — Aurora Fashion Club

### Entidade principal: customers

| Campo | Tipo | Descrição |
|---|---|---|
| customer_id | string | Identificador único do cliente |
| gender | category | Gênero informado ou estimado |
| age | int | Idade do cliente |
| region | category | Região geográfica |
| city | string | Cidade do cliente |
| income_band | category | Faixa de renda estimada |
| acquisition_channel | category | Canal de aquisição |
| first_purchase_date | date | Data da primeira compra |
| last_purchase_date | date | Data da última compra |
| number_of_orders | int | Quantidade total de pedidos |
| total_spent | float | Gasto total acumulado |
| average_ticket | float | Ticket médio por pedido |
| discount_usage_rate | float | Percentual de compras com desconto |
| returns_rate | float | Taxa de devolução |
| app_sessions | int | Quantidade de sessões no app |
| email_open_rate | float | Taxa de abertura de e-mail |
| email_click_rate | float | Taxa de clique em campanhas |
| sms_response_rate | float | Taxa de resposta a SMS |
| loyalty_tier | category | Faixa no programa de fidelidade |
| campaign_exposure_count | int | Número de campanhas recebidas |
| campaign_conversion_rate | float | Conversão em campanhas |
| days_since_last_purchase | int | Dias desde a última compra |
| category_preference | category | Categoria predominante de compra |
| churn_flag | int | Indicador de churn |
| churn_risk_score | float | Score preditivo de churn |
| estimated_ltv | float | Lifetime value estimado |

### Entidade: products

| Campo | Tipo | Descrição |
|---|---|---|
| product_id | string | Identificador único do produto |
| product_name | string | Nome comercial do produto |
| category | category | Categoria macro |
| subcategory | category | Subcategoria |
| gender_target | category | Público-alvo |
| season | category | Sazonalidade da coleção |
| brand | category | Marca ou linha |
| list_price | float | Preço cheio |
| avg_discount_rate | float | Desconto médio aplicado |
| margin_rate | float | Margem estimada |
| launch_date | date | Data de lançamento |
| is_bestseller | int | Indicador de sucesso comercial |
| return_rate | float | Taxa média de devolução |

### Entidade: orders

| Campo | Tipo | Descrição |
|---|---|---|
| order_id | string | Identificador do pedido |
| customer_id | string | Chave do cliente |
| order_date | date | Data do pedido |
| channel | category | Canal de compra |
| order_status | category | Status do pedido |
| gross_amount | float | Valor bruto do pedido |
| discount_amount | float | Valor total de desconto |
| net_amount | float | Valor líquido do pedido |
| payment_method | category | Forma de pagamento |
| shipping_type | category | Tipo de entrega |
| shipping_cost | float | Custo de frete |
| delivery_days | int | Prazo de entrega |
| return_flag | int | Indicador de devolução |

### Entidade: order_items

| Campo | Tipo | Descrição |
|---|---|---|
| order_item_id | string | Identificador do item do pedido |
| order_id | string | Chave do pedido |
| product_id | string | Chave do produto |
| quantity | int | Quantidade comprada |
| unit_price | float | Preço unitário |
| discount_value | float | Desconto aplicado ao item |
| line_amount | float | Valor total do item |

### Entidade de apoio: interactions

| Campo | Tipo | Descrição |
|---|---|---|
| interaction_id | string | Identificador da interação |
| customer_id | string | Chave do cliente |
| interaction_date | date | Data da interação |
| channel | category | Canal utilizado |
| interaction_type | category | Tipo de contato |
| response_flag | int | Indicador de resposta |
| conversion_flag | int | Indicador de conversão |
| campaign_id | string | Identificador da campanha |
| message_theme | category | Tema da mensagem |

### Entidade de apoio: campaigns

| Campo | Tipo | Descrição |
|---|---|---|
| campaign_id | string | Identificador da campanha |
| campaign_name | string | Nome da campanha |
| campaign_type | category | Tipo de campanha |
| target_segment | category | Segmento-alvo |
| channel | category | Canal de execução |
| send_date | date | Data de disparo |
| offer_type | category | Tipo de oferta |
| cost | float | Custo da campanha |
| impressions | int | Número de impactos |
| opens | int | Aberturas |
| clicks | int | Cliques |
| conversions | int | Conversões |
| revenue_generated | float | Receita atribuída |

### Entidade de apoio: support_tickets

| Campo | Tipo | Descrição |
|---|---|---|
| ticket_id | string | Identificador do chamado |
| customer_id | string | Chave do cliente |
| open_date | date | Data de abertura |
| close_date | date | Data de encerramento |
| issue_type | category | Tipo de problema |
| severity | category | Severidade |
| resolution_time_hours | float | Tempo de resolução |
| satisfaction_score | float | Satisfação pós-atendimento |
| reopened_flag | int | Indicador de reabertura |

### Entidade de apoio: digital_events

| Campo | Tipo | Descrição |
|---|---|---|
| event_id | string | Identificador do evento |
| customer_id | string | Chave do cliente |
| event_date | date | Data do evento |
| event_type | category | Tipo de evento |
| device_type | category | Dispositivo usado |
| session_duration | float | Duração da sessão |
| page_views | int | Número de páginas visualizadas |
| add_to_cart_flag | int | Indicador de adição ao carrinho |
| checkout_start_flag | int | Indicador de início de checkout |
| purchase_flag | int | Indicador de compra |

## 1.11 Objetivos do produto analítico

O produto de dados deste case deve funcionar como uma plataforma analítica de CRM e retenção orientada a decisão. O objetivo não é apenas construir dashboards ou modelos isolados, mas criar inteligência operacional para suportar marketing, CRM, growth e liderança comercial.

A solução deverá responder perguntas estratégicas do negócio:
- quais clientes têm maior probabilidade de churn;
- quais segmentos possuem maior potencial de LTV;
- quais canais atraem clientes mais rentáveis;
- quais campanhas realmente geram recorrência;
- quais perfis possuem alta dependência de desconto;
- quais comportamentos antecedem abandono;
- como personalizar campanhas por estágio da jornada;
- quais clientes devem receber ações de retenção, reativação ou upsell.

O produto deverá permitir decisões práticas como:
- definição de régua de relacionamento;
- priorização de investimento em mídia;
- personalização de campanhas;
- proteção de margem;
- redução de churn;
- aumento de recompra;
- aumento de ticket médio;
- melhoria de experiência.

## 1.12 Métricas de negócio

### Métricas de retenção

| Métrica | Descrição |
|---|---|
| Churn Rate | Percentual de clientes inativos após janela definida |
| Repeat Purchase Rate | Percentual de clientes com recompra |
| Retention Rate | Percentual de clientes retidos ao longo do tempo |
| Reactivation Rate | Percentual de clientes reativados |
| Days Between Orders | Tempo médio entre pedidos |
| Cohort Retention | Retenção por coorte de aquisição |

### Métricas financeiras

| Métrica | Descrição |
|---|---|
| Average Ticket | Ticket médio |
| Gross Revenue | Receita bruta |
| Net Revenue | Receita líquida |
| Contribution Margin | Margem estimada |
| Customer Lifetime Value (LTV) | Valor estimado do cliente |
| Revenue per Customer | Receita média por cliente |

### Métricas de CRM

| Métrica | Descrição |
|---|---|
| Open Rate | Taxa de abertura de campanhas |
| Click Through Rate | Taxa de clique |
| Campaign Conversion Rate | Conversão por campanha |
| Engagement Score | Score agregado de engajamento |
| Campaign Fatigue Index | Índice de fadiga de comunicação |
| Loyalty Activation Rate | Ativação no programa de fidelidade |

### Métricas digitais

| Métrica | Descrição |
|---|---|
| App Session Frequency | Frequência de sessões |
| Add-to-Cart Rate | Taxa de adição ao carrinho |
| Checkout Abandonment Rate | Taxa de abandono de checkout |
| Digital Engagement Index | Índice agregado de comportamento digital |

### Métricas operacionais

| Métrica | Descrição |
|---|---|
| Return Rate | Taxa de devolução |
| Delivery SLA | Prazo médio de entrega |
| Support Satisfaction Score | Satisfação com atendimento |
| Ticket Resolution Time | Tempo médio de resolução |

## 1.13 Regras de geração sintética dos dados

Os dados devem simular um ambiente corporativo realista, incluindo comportamento humano, sazonalidade, inconsistências moderadas e relações causais plausíveis entre tabelas.

A geração sintética não deve produzir dados totalmente aleatórios. Os dados precisam respeitar regras de negócio para que as análises tenham valor analítico.

### Volume esperado

| Tabela | Volume estimado |
|---|---|
| customers | 80 mil a 150 mil clientes |
| products | 3 mil a 8 mil produtos |
| orders | 500 mil a 1,5 milhão de pedidos |
| order_items | 1,5 milhão a 4 milhões de itens |
| campaigns | 500 a 2 mil campanhas |
| interactions | 2 milhões a 8 milhões de interações |
| support_tickets | 50 mil a 200 mil chamados |
| digital_events | 10 milhões+ eventos |

## 1.14 Regras de comportamento sintético por entidade

### customers

Os clientes devem possuir perfis distintos de comportamento.

Segmentos comportamentais esperados:
- clientes premium altamente recorrentes;
- clientes ocasionais;
- clientes sensíveis a desconto;
- clientes recém-adquiridos;
- clientes inativos;
- clientes de alto risco de churn;
- clientes altamente digitais;
- clientes concentrados em loja física.

Regras importantes:
- clientes premium possuem maior ticket médio e menor sensibilidade a desconto;
- clientes adquiridos via mídia agressiva possuem maior churn médio;
- clientes com baixa interação digital tendem a recomprar menos;
- clientes com alta devolução possuem menor retenção;
- clientes mais engajados em campanhas possuem maior recorrência.

### products

Os produtos devem refletir dinâmica real de varejo de moda.

Regras importantes:
- categorias possuem sazonalidade;
- produtos bestseller possuem maior volume de venda;
- determinados produtos possuem maior taxa de devolução;
- produtos premium possuem maior margem e menor desconto;
- novas coleções devem influenciar aumento de engajamento.

### orders

Pedidos devem respeitar distribuição comportamental.

Regras importantes:
- clientes recorrentes fazem mais pedidos ao longo do tempo;
- pedidos promocionais possuem ticket médio menor;
- períodos sazonais aumentam volume de pedidos;
- frete impacta conversão;
- atraso de entrega aumenta chance de reclamação e churn;
- devoluções devem ocorrer com maior frequência em determinadas categorias.

### order_items

Regras importantes:
- pedidos possuem entre 1 e 8 itens;
- produtos complementares podem aparecer juntos;
- categorias premium possuem menor quantidade por pedido;
- descontos variam conforme campanha e perfil do cliente.

### campaigns

Campanhas devem possuir lógica de performance.

Regras importantes:
- campanhas segmentadas convertem melhor;
- excesso de comunicação reduz taxa de abertura;
- clientes premium respondem melhor a exclusividade do que desconto;
- campanhas genéricas possuem menor ROI;
- campanhas sazonais aumentam receita.

### interactions

As interações devem representar comportamento omnichannel.

Tipos esperados:
- e-mail;
- push notification;
- SMS;
- WhatsApp;
- remarketing;
- campanhas in-app.

Regras importantes:
- clientes mais engajados possuem maior taxa de abertura;
- fadiga de campanha reduz clique e conversão;
- excesso de contato aumenta risco de opt-out.

### support_tickets

Chamados devem impactar experiência.

Regras importantes:
- atrasos aumentam tickets;
- baixa satisfação aumenta churn;
- clientes premium possuem SLA melhor;
- reabertura de chamados reduz NPS.

### digital_events

Eventos digitais devem representar comportamento navegacional.

Eventos esperados:
- page_view;
- product_view;
- add_to_cart;
- wishlist;
- checkout_start;
- purchase;
- app_open;
- campaign_click.

Regras importantes:
- clientes mais engajados possuem mais sessões;
- abandono de checkout antecede churn;
- sessões longas aumentam probabilidade de compra;
- campanhas influenciam comportamento de navegação.

## 1.15 Regras analíticas esperadas

A base deverá permitir desenvolvimento de:
- SQL analítico avançado;
- modelagem dimensional;
- construção de data marts;
- análise de cohort;
- análise RFM;
- clusterização de clientes;
- previsão de churn;
- previsão de LTV;
- recomendação de produtos;
- análise de campanhas;
- dashboards executivos;
- feature engineering;
- pipelines ETL/ELT;
- validação de qualidade de dados;
- testes estatísticos e A/B testing.

## 1.16 Complexidades intencionais da base

A base deverá conter problemas controlados para simular ambiente corporativo real:
- dados faltantes;
- inconsistências cadastrais;
- valores extremos;
- duplicidade parcial;
- atraso de atualização;
- clientes sem histórico suficiente;
- campanhas sem tracking completo;
- produtos descontinuados;
- mudanças sazonais abruptas;
- drift de comportamento ao longo do tempo.

O objetivo é permitir experiência prática em:
- data cleaning;
- engenharia de features;
- reconciliação de dados;
- tratamento de inconsistências;
- monitoramento de qualidade;
- construção de pipelines robustos.

## 1.17 Relacionamento entre tabelas

A base deverá ser desenhada com integridade referencial entre as entidades, permitindo consultas analíticas e modelagem relacional consistente.

### Chaves primárias e relações esperadas
- `customers.customer_id` é a chave principal da entidade de clientes.
- `products.product_id` é a chave principal da entidade de produtos.
- `orders.order_id` é a chave principal da entidade de pedidos.
- `order_items.order_item_id` é a chave principal da entidade de itens do pedido.
- `campaigns.campaign_id` é a chave principal da entidade de campanhas.
- `support_tickets.ticket_id` é a chave principal da entidade de suporte.
- `digital_events.event_id` é a chave principal da entidade de eventos digitais.
- `interactions.interaction_id` é a chave principal da entidade de interações.

### Relações funcionais
- Um cliente pode ter vários pedidos.
- Um pedido pode ter vários itens.
- Um item pertence a um único pedido e a um único produto.
- Um cliente pode receber várias campanhas e gerar várias interações.
- Um cliente pode abrir vários tickets de suporte.
- Um cliente pode registrar múltiplos eventos digitais ao longo do tempo.
- Uma campanha pode ser associada a múltiplas interações e múltiplas conversões.

### Regra de coerência relacional
- todo pedido deve pertencer a um cliente válido;
- todo item deve pertencer a um pedido válido e a um produto válido;
- toda interação deve pertencer a um cliente válido;
- todo ticket deve pertencer a um cliente válido;
- todo evento digital deve pertencer a um cliente válido;
- toda campanha deve ter janela temporal coerente com as interações associadas.

## 1.18 Estratégia de geração sintética por camada

A geração dos dados deverá seguir uma lógica em camadas para manter coerência entre atributos, comportamento e desfechos.

### Camada 1 — Perfil do cliente
Primeiro serão definidos perfil demográfico, canal de aquisição, faixa de renda, propensão a desconto, sensibilidade a campanha e perfil de engajamento. Essa camada servirá como base para o comportamento futuro.

### Camada 2 — Jornada de compra
Com base no perfil do cliente, serão gerados pedidos ao longo do tempo com variação de frequência, ticket médio, canal, desconto, frete e devolução.

### Camada 3 — Engajamento digital
Os eventos digitais serão gerados de forma dependente da intensidade de uso do cliente, da frequência de campanhas e da maturidade de relacionamento.

### Camada 4 — Campanhas e interações
As campanhas deverão ter impacto probabilístico em abertura, clique e conversão, com efeito diferente por segmento. Clientes premium, oportunistas e inativos devem reagir de forma distinta.

### Camada 5 — Suporte e fricção operacional
Tickets de suporte devem ser criados com base em regras de experiência, prazo de entrega, devolução e frequência de problemas, influenciando a probabilidade de churn.

### Camada 6 — Labels analíticas
Por fim, serão calculados churn, LTV, engajamento, retenção, probabilidade de recompra e outros indicadores derivados com base no comportamento acumulado.

## 1.19 Regras de geração por tabela

### customers
- gerar primeiro o universo de clientes;
- distribuir clientes entre segmentos premium, intermediário, sensível a desconto, novo e inativo;
- vincular canais de aquisição a perfis de qualidade diferentes;
- calcular recência, frequência, monetização e score de risco com base na jornada;
- introduzir pequena proporção de dados ausentes e valores extremos controlados.

### products
- gerar catálogo por categoria, subcategoria e linha de marca;
- associar sazonalidade a coleções e períodos do ano;
- definir preços, margens e taxas de devolução por segmento de produto;
- introduzir produtos bestsellers, produtos de baixo giro e produtos premium;
- permitir produtos com diferentes elasticidades a desconto.

### orders
- gerar pedidos ao longo do tempo com padrão temporal realista;
- aumentar volume em períodos sazonais;
- variar desconto, frete e método de pagamento por perfil de cliente;
- permitir cancelamentos, devoluções e pedidos com status distintos;
- concentrar maior ticket em clientes com maior renda e menor dependência promocional.

### order_items
- decompor cada pedido em itens individuais;
- permitir composição do carrinho com diferentes categorias;
- manter consistência entre valor bruto do pedido e soma dos itens;
- introduzir itens com desconto e sem desconto;
- refletir mix de compra por perfil e coleção.

### campaigns
- gerar campanhas por objetivo: retenção, reativação, upsell, cross-sell, conversão e fidelidade;
- variar canal de disparo, custo, volume de envio e desempenho;
- associar conversão mais alta a campanhas segmentadas;
- associar queda de performance a excesso de volume e baixa relevância.

### interactions
- registrar interações por canal e por tema;
- diferenciar resposta entre clientes engajados e desengajados;
- criar relação entre campanha recebida e reação do cliente;
- manter coerência temporal entre envio e resposta.

### support_tickets
- gerar tickets com severidade, tempo de resolução e satisfação;
- aumentar volume de tickets em clientes com alta fricção operacional;
- associar maior probabilidade de churn a tickets recorrentes;
- permitir reabertura de chamados em parte da base.

### digital_events
- gerar sessões e eventos compatíveis com o nível de engajamento do cliente;
- modelar funil digital: abertura de app, navegação, produto visualizado, carrinho, checkout e compra;
- criar intensidade maior de eventos em clientes de maior propensão de compra;
- reduzir atividade digital em clientes de risco.

## 1.20 Saídas analíticas esperadas do case

A estrutura deste case deverá sustentar os seguintes entregáveis:
- base relacional sintética e validada;
- consulta SQL com análises de retenção, churn e cohort;
- notebook com EDA profunda;
- segmentação RFM e clusterização;
- modelo de churn com score por cliente;
- cálculo de LTV e priorização comercial;
- análise de campanhas por canal, segmento e conversão;
- painel executivo de CRM;
- recomendação de ações por cluster de cliente.

## 1.21 Critérios de aceite do case

Para considerar o Case 1 pronto para desenvolvimento, ele deve atender aos seguintes critérios:
- possuir narrativa de negócio clara;
- conter problema relevante e mensurável;
- ter dados sintéticos com coerência relacional;
- permitir exploração em SQL e Python;
- gerar métricas de negócio úteis para CRM;
- permitir construção de modelos preditivos;
- suportar análise executiva e recomendação de ação;
- apresentar potencial real de portfólio para vagas de dados.

## 1.22 Próximo passo de implementação

Quando este case for validado, a próxima etapa será a definição do pipeline de geração sintética e da arquitetura de arquivos:
- script principal de geração em Python;
- persistência em `.csv`, `.xlsx`, `.json` e SQLite;
- verificação de consistência entre formatos;
- criação de um notebook de exploração;
- criação de um notebook de modelagem;
- documentação do projeto no README.


## 2. Arquitetura Técnica do Projeto

### 2.1 Visão geral da arquitetura

A arquitetura deste projeto será construída para suportar um ciclo completo de dados: geração sintética, persistência em múltiplos formatos, validação de consistência, exploração analítica, modelagem preditiva e publicação de insights. A proposta não é apenas criar arquivos isolados, mas estruturar um ambiente reprodutível que permita ler, transformar, analisar e modelar os mesmos dados a partir de diferentes origens tabulares.

A arquitetura será composta por quatro camadas principais:
- geração sintética e persistência;
- camada de ingestão e padronização;
- camada analítica e de modelagem;
- camada de visualização e entrega executiva.

### 2.2 Estrutura de pastas

```text
aurora_fashion_club/
├── data/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── csv/
│   ├── xlsx/
│   ├── json/
│   └── sqlite/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_segmentacao.ipynb
│   ├── 03_churn_modeling.ipynb
│   └── 04_crm_dashboard.ipynb
├── src/
│   ├── generate_data.py
│   ├── validators.py
│   ├── transforms.py
│   ├── features.py
│   ├── modeling.py
│   ├── utils.py
│   └── config.py
├── dashboards/
├── reports/
├── tests/
├── docs/
├── README.md
└── requirements.txt
```

### 2.3 Pipeline ETL/ELT

O pipeline seguirá uma lógica híbrida entre ETL e ELT.

**ETL** será utilizado para:
- geração e tratamento inicial dos dados sintéticos;
- normalização de nomes e tipos;
- criação de regras de coerência;
- cálculo de campos derivados básicos.

**ELT** será utilizado para:
- carregar os dados brutos em SQLite e arquivos tabulares;
- transformar os dados em estruturas analíticas;
- gerar visões de negócio, métricas e tabelas derivadas;
- preparar data marts para análise em notebooks e BI.

A lógica do pipeline será:
1. gerar dados sintéticos com relacionamento entre entidades;
2. persistir as tabelas em CSV, XLSX, JSON e SQLite;
3. validar integridade estrutural e referencial;
4. carregar dados na camada bronze;
5. limpar e padronizar na camada silver;
6. criar features, métricas e agregações na camada gold;
7. alimentar notebooks de EDA, modelagem e visualização.

### 2.4 Fluxo dos dados

O fluxo dos dados será orientado por uma cadeia de dependência entre entidades:
- `customers` origina a jornada analítica;
- `orders` e `order_items` representam o comportamento transacional;
- `products` explica o mix comercial;
- `campaigns` e `interactions` explicam a pressão de CRM;
- `support_tickets` representa fricção operacional;
- `digital_events` representa engajamento e navegação.

O modelo relacional permitirá que o usuário navegue da origem do comportamento até o desfecho analítico, por exemplo:
- campanha → interação → pedido → recompra;
- evento digital → carrinho → checkout → compra;
- ticket de suporte → satisfação → churn;
- produto → categoria → margem → retenção por segmento.

### 2.5 Estratégia de ingestão multi-formato

Os dados serão exportados nos formatos `.csv`, `.xlsx`, `.json` e SQLite. O objetivo é trabalhar o mesmo conteúdo em diferentes representações de dados tabulares.

**CSV** será usado para:
- leitura simples;
- interoperabilidade;
- consultas rápidas;
- testes de importação.

**XLSX** será usado para:
- validação manual;
- análise exploratória rápida;
- integração com usuários de negócio;
- demonstração em ferramentas de BI.

**JSON** será usado para:
- inspeção de estrutura aninhada quando necessário;
- integração com aplicações e APIs futuras;
- simulação de payloads de origem externa.

**SQLite** será usado para:
- consultas SQL;
- simulação de ambiente relacional real;
- criação de joins;
- validação de cardinalidade e integridade.

### 2.6 Camadas Bronze, Silver e Gold

A arquitetura analítica será organizada em três camadas.

**Bronze**
- dados brutos gerados pelo script;
- arquivos persistidos sem transformações analíticas profundas;
- preservação da estrutura original.

**Silver**
- dados padronizados;
- limpeza de nulos e inconsistências;
- padronização de formatos de data, categorias e tipos;
- normalização de colunas e relacionamento entre chaves.

**Gold**
- tabelas agregadas;
- features analíticas;
- métricas de negócio;
- data marts para churn, LTV, CRM e campanha;
- visões prontas para modelagem e visualização.

### 2.7 Estratégia SQLite

O SQLite funcionará como o banco central do projeto para consultas e experimentação relacional. Ele armazenará todas as entidades principais em tabelas independentes, preservando as chaves primárias e estrangeiras.

A base SQLite deverá permitir:
- joins entre tabelas;
- consultas por cliente, campanha e pedido;
- análises temporais;
- coortes de aquisição;
- cálculo de RFM;
- querys para features de churn e LTV.

A modelagem no SQLite deverá respeitar as relações do dicionário de dados e permitir carregamento reprodutível do projeto.

### 2.8 Estratégia de geração sintética

A geração dos dados será conduzida com base em regras probabilísticas e estatísticas para preservar coerência entre comportamento do cliente, desempenho comercial e resultados analíticos.

### 2.9 Regras probabilísticas

As variáveis não serão geradas de forma puramente aleatória. Elas seguirão dependências entre si.

Exemplos:
- clientes com maior sensibilidade a desconto terão maior probabilidade de resposta a campanhas promocionais;
- clientes com maior frequência de compra terão menor probabilidade de churn;
- clientes com maior tempo sem compra terão risco crescente de abandono;
- tickets de suporte com maior severidade aumentarão a chance de churn;
- produtos com maior taxa de devolução reduzirão retenção do cliente;
- campanhas segmentadas terão taxa de conversão maior do que campanhas genéricas.

### 2.10 Distribuições estatísticas

As variáveis devem respeitar distribuições plausíveis:
- idade: distribuição concentrada em faixas de consumo ativo;
- renda: distribuição assimétrica por faixa;
- ticket médio: distribuição com cauda longa;
- pedidos por cliente: distribuição assimétrica com poucos clientes muito recorrentes;
- sessões no app: distribuição com excesso de zeros para clientes pouco digitais;
- desconto utilizado: distribuição concentrada em perfis promocionais;
- churn: desbalanceamento moderado, com classe minoritária.

### 2.11 Dependência temporal

A base deve respeitar comportamento temporal. Um cliente não terá a mesma chance de compra em todos os períodos. O algoritmo deverá considerar:
- sazonalidade por mês e campanha;
- evolução do engajamento ao longo do ciclo de vida;
- desgaste da comunicação ao longo do tempo;
- impacto acumulado de suporte e devolução;
- efeito da primeira compra e da segunda compra na retenção.

### 2.12 Simulação de churn

O churn será simulado a partir de uma combinação de sinais:
- recência elevada;
- baixa frequência;
- baixa resposta a campanhas;
- alta devolução;
- baixo uso digital;
- tickets recorrentes;
- queda de ticket médio;
- menor diversidade de categorias compradas.

A probabilidade de churn será calculada como função dessas variáveis, com ruído controlado para simular comportamento real.

### 2.13 Simulação de comportamento CRM

O comportamento CRM será construído para refletir perfis diferentes:
- clientes reativos a promoção;
- clientes orientados à marca;
- clientes premium;
- clientes oportunistas;
- clientes sensíveis a canal;
- clientes digitais;
- clientes inativos;
- clientes de reativação.

Cada tipo deverá reagir de forma diferente a canal, tema, frequência e tipo de campanha.

## 3. Especificação do Gerador de Dados

### 3.1 Funções principais

O gerador de dados deverá ser implementado como um conjunto de funções modulares:
- `generate_customers()`;
- `generate_products()`;
- `generate_orders()`;
- `generate_order_items()`;
- `generate_campaigns()`;
- `generate_interactions()`;
- `generate_support_tickets()`;
- `generate_digital_events()`;
- `build_features()`;
- `export_datasets()`;
- `validate_referential_integrity()`.

### 3.2 Classes

Para organizar o projeto, o ideal é estruturar o gerador em classes:
- `CustomerGenerator`;
- `ProductGenerator`;
- `OrderGenerator`;
- `CampaignGenerator`;
- `InteractionGenerator`;
- `SupportTicketGenerator`;
- `DigitalEventGenerator`;
- `DataExporter`;
- `DataValidator`.

### 3.3 Seeds e reprodutibilidade

Todos os geradores devem trabalhar com `random seed` fixa para garantir reprodutibilidade. O projeto precisa permitir:
- repetição exata da base;
- comparação entre execuções;
- validação de alterações;
- controle experimental.

### 3.4 Relacionamentos e cardinalidade

A geração deverá respeitar cardinalidades reais:
- 1 cliente → N pedidos;
- 1 pedido → N itens;
- 1 produto → N itens;
- 1 cliente → N interações;
- 1 cliente → N tickets;
- 1 cliente → N eventos digitais;
- 1 campanha → N interações;
- 1 campanha → N conversões.

### 3.5 Regras de consistência interna

O gerador precisa assegurar:
- pedidos com soma de itens compatível com o valor total;
- datas coerentes entre campanha e interação;
- eventos digitais anteriores à compra;
- tickets de suporte após a ocorrência do problema;
- churn calculado após janela de inatividade;
- LTV superior para clientes recorrentes e premium.

## 4. Plano Analítico

### 4.1 Análise exploratória de dados (EDA)

A EDA deverá responder:
- qual é o perfil da base;
- quais segmentos concentram maior valor;
- onde ocorrem perdas de retenção;
- quais canais e campanhas performam melhor;
- quais produtos e categorias sustentam recorrência;
- como suporte e digital impactam o comportamento.

### 4.2 Segmentação

A segmentação deverá ser orientada por:
- RFM;
- clusterização comportamental;
- valor do cliente;
- dependência de desconto;
- maturidade digital;
- propensão de compra;
- risco de churn.

### 4.3 Churn Prediction

O objetivo do modelo de churn é identificar clientes com risco elevado de abandono e priorizar intervenções.

Saídas esperadas:
- probabilidade de churn;
- score de risco;
- ranking de clientes prioritários;
- análise de variáveis mais relevantes.

### 4.4 LTV

O cálculo de LTV deve estimar quanto valor cada cliente tende a gerar ao longo do tempo, combinando frequência, ticket, margem, retenção e risco de abandono.

### 4.5 Recomendação

A recomendação deve responder:
- qual canal usar;
- qual oferta enviar;
- qual frequência aplicar;
- qual segmento priorizar;
- qual ação de retenção adotar;
- qual jornada de reativação propor.

### 4.6 A/B Testing

O projeto deve prever lógica de experimentação:
- versão A e B de campanhas;
- avaliação de abertura, clique e conversão;
- comparação de impacto em churn;
- efeito de segmentação sobre retenção.

### 4.7 Cohort Analysis

A análise por coorte deverá medir:
- retenção por mês de aquisição;
- retenção por canal;
- retenção por campanha;
- evolução da recompra por período;
- degradação do engajamento ao longo do tempo.

## 5. Plano de Machine Learning

### 5.1 Features

As features principais devem incluir:
- recência;
- frequência;
- monetização;
- ticket médio;
- taxa de desconto;
- devolução;
- engajamento digital;
- resposta a campanhas;
- histórico de suporte;
- diversidade de categorias;
- canal de aquisição;
- loyalty tier;
- comportamento temporal.

### 5.2 Targets

Targets principais:
- `churn_flag`;
- `estimated_ltv`;
- `campaign_conversion_rate`;
- `renewal_probability`;
- `reactivation_probability`.

### 5.3 Pipelines

Os pipelines de ML devem incluir:
- imputação;
- codificação;
- escalonamento quando necessário;
- seleção de features;
- treinamento;
- validação;
- interpretação.

### 5.4 Métricas

### Classificação
- AUC;
- F1-score;
- precision;
- recall;
- KS;
- balanced accuracy.

### Regressão
- RMSE;
- MAE;
- MAPE;
- R².

### 5.5 Baselines

Modelos baseline esperados:
- regressão logística;
- árvore de decisão;
- regressão linear para LTV;
- regras heurísticas de churn;
- modelo de score simples baseado em RFM.

### 5.6 Modelos candidatos

Modelos candidatos:
- Random Forest;
- XGBoost;
- Gradient Boosting;
- LightGBM;
- Logistic Regression;
- CatBoost;
- KMeans para segmentação;
- Isolation Forest para anomalias.

## 6. Estratégia de Visualização

### 6.1 Dashboards

O projeto deve ter dashboards com visão executiva e analítica:
- visão geral de retenção;
- perfil de clientes;
- coortes de aquisição;
- churn e risco;
- campanhas e CRM;
- produto e categoria;
- digital e engajamento;
- suporte e experiência.

### 6.2 KPIs

KPIs prioritários:
- churn;
- retenção;
- ticket médio;
- LTV;
- taxa de abertura;
- taxa de clique;
- conversão por campanha;
- devolução;
- tempo entre pedidos;
- índice de engajamento digital.

### 6.3 Storytelling

A narrativa visual deve seguir esta lógica:
1. o negócio está crescendo, mas perdendo qualidade de base;
2. a retenção está concentrada em poucos perfis;
3. campanhas genéricas degradam performance;
4. suporte e digital ajudam a explicar churn;
5. ações segmentadas geram ganho de valor.

## 7. Plano de MLOps

### 7.1 Versionamento

O projeto deve versionar:
- dados sintéticos;
- scripts de geração;
- notebooks;
- features;
- modelos;
- métricas;
- relatórios.

### 7.2 MLflow

MLflow pode ser usado para:
- registrar experimentos;
- comparar modelos;
- armazenar métricas;
- salvar artefatos;
- rastrear execuções.

### 7.3 Monitoramento

O monitoramento deve observar:
- estabilidade do churn;
- mudança no perfil dos clientes;
- alteração do comportamento de compra;
- degradação de performance por segmento;
- consistência das features.

### 7.4 Drift

Tipos de drift esperados:
- drift de dados;
- drift de comportamento;
- drift de campanha;
- drift sazonal;
- drift de produto.

### 7.5 Retraining

O plano de retraining deve ser acionado quando:
- houver mudança expressiva de comportamento;
- a performance do modelo cair;
- novas campanhas forem introduzidas;
- a distribuição de segmentos se alterar.

## 8. README Técnico Profissional

# Aurora Fashion Club — CRM e Retenção com Dados Sintéticos

## Descrição
Projeto de portfólio construído como um produto analítico de CRM e retenção. O objetivo é simular uma varejista omnichannel de moda, gerar dados sintéticos realistas em múltiplos formatos e desenvolver análises, segmentações e modelos para apoiar decisões de negócio.

## Objetivos
- Simular base relacional rica para CRM.
- Trabalhar com CSV, XLSX, JSON e SQLite.
- Desenvolver EDA, segmentação, churn e LTV.
- Praticar SQL, Python, BI e machine learning.
- Produzir um case profissional de portfólio.

## Principais módulos
- Geração sintética de dados;
- Base relacional completa;
- Análise exploratória;
- Segmentação de clientes;
- Predição de churn;
- Cálculo de LTV;
- Recomendação de ações;
- Dashboards executivos.

## Tecnologias
- Python
- Pandas
- NumPy
- Scikit-learn
- SQLite
- OpenPyXL
- Jupyter Notebook
- Matplotlib / Seaborn

## Saídas
- CSV
- XLSX
- JSON
- SQLite
- notebooks analíticos
- dashboards
- relatório executivo

## Roadmap
1. Gerar dados sintéticos.
2. Persistir em múltiplos formatos.
3. Validar integridade relacional.
4. Executar EDA.
5. Criar features.
6. Treinar modelos de churn e LTV.
7. Desenvolver dashboards.
8. Documentar e publicar o case.

## 9. Roadmap Evolutivo do Projeto

### Fase 1 — Fundamentos
- definição final do caso;
- geração da base sintética;
- persistência multi-formato;
- validação relacional.

### Fase 2 — Análise
- EDA;
- cohort analysis;
- RFM;
- segmentação;
- identificação de padrões.

### Fase 3 — Modelagem
- churn prediction;
- LTV;
- recomendação;
- feature engineering;
- validação de métricas.

### Fase 4 — Produto
- dashboard executivo;
- relatório gerencial;
- documentação;
- README;
- publicação no GitHub.

### Fase 5 — Evolução
- inclusão de MLflow;
- deploy em API;
- monitoramento de drift;
- simulação de A/B testing;
- expansão para outros cases.

