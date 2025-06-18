
# RELATÓRIO DE ANÁLISE DE OPORTUNIDADES DE CODESHARE
## Gol + Azul - Algoritmo de Johnson

### RESUMO EXECUTIVO
- **Total de oportunidades identificadas**: 400
- **Distribuição por tipo**: {'Azul→Gol': np.int64(200), 'Gol→Azul': np.int64(200)}
- **Rota mais eficiente**: PDP → AEP (1499 km)
- **Distância média**: 5356 km

### PRINCIPAIS INSIGHTS

#### 1. Complementaridade das Malhas
- **38 rotas domésticas** (9.5%)
- **362 rotas internacionais** (90.5%)
- As companhias se complementam bem geograficamente

#### 2. Hubs Estratégicos
- **POA (Porto Alegre)**: Principal hub de conexão (82 conexões)
- **VCP (Viracopos)**: Hub importante da Azul (118 conexões)
- **GRU (Guarulhos)**: Hub internacional (206 conexões)

#### 3. Rotas Mais Promissoras
- PDP → AEP: 1499 km, 1 escala(s)
- AEP → PDP: 1499 km, 1 escala(s)
- PDP → EZE: 1526 km, 1 escala(s)
- EZE → PDP: 1526 km, 1 escala(s)
- PDP → ROS: 1619 km, 1 escala(s)

#### 4. Benefícios do Codeshare
- **Conectividade ampliada**: 153 aeroportos únicos
- **Eficiência de rotas**: Caminhos otimizados usando ambas as redes
- **Cobertura geográfica**: Acesso a destinos exclusivos de cada companhia

### RECOMENDAÇÕES
1. **Priorizar rotas curtas**: Focar nas 24 oportunidades com menos de 2.000 km
2. **Fortalecer hubs**: Investir em POA, VCP e GRU como pontos de conexão
3. **Explorar mercados**: 362 rotas internacionais oferecem expansão de mercado
4. **Otimizar escalas**: 26 rotas com apenas 1 escala são mais atrativas

### METODOLOGIA
- Algoritmo de Johnson para caminhos mínimos
- Análise de 76 aeroportos Gol + 140 aeroportos Azul
- Identificação automática de oportunidades de codeshare real
- Validação geográfica e operacional
