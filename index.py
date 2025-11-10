import csv

# --- CLASSE BASE ---
class Imovel:
    """
    Classe base para todos os tipos de locação, define valores comuns
    como o contrato imobiliário.
    """
    # [cite_start]Valor fixo do contrato (R$ 2.000,00 divididos em até 5 vezes) [cite: 24, 31]
    VALOR_CONTRATO = 2000.00
    MAX_PARCELAS_CONTRATO = 5

    def __init__(self, tem_garagem=False):
        self.valor_base = 0.0
        self.mensalidade_total = 0.0
        self.tem_garagem = tem_garagem

    def calcular_mensalidade(self):
        """Método abstrato/base que deve ser sobrescrito (Polimorfismo)."""
        raise NotImplementedError("Este método deve ser implementado nas classes filhas.")

    def _aplicar_acrescimo_garagem(self):
        """Aplica o acréscimo de garagem para Casa e Apartamento[cite: 28]."""
        if self.tem_garagem:
            # R$ 300,00 para vaga de garagem em Casas e Apartamentos
            return 300.00
        return 0.0
    
    def get_resumo(self):
        """Retorna o resumo do orçamento para apresentação[cite: 31]."""
        return {
            "Aluguel Mensal Orçado": self.mensalidade_total,
            "Valor do Contrato": self.VALOR_CONTRATO,
            "Parcelamento do Contrato": f"Em até {self.MAX_PARCELAS_CONTRATO} vezes"
        }

# --- CLASSES FILHAS (HERANÇA) ---

class Apartamento(Imovel):
    """Implementa as regras de cálculo para Apartamentos."""
    VALOR_BASE_1Q = 700.00  # R$ 700,00/1 Quarto [cite: 17]
    ACRESCIMO_2Q = 200.00   # Acréscimo por 2 quartos [cite: 25, 26]
    DESCONTO_SEM_CRIANCAS = 0.05 # 5% de desconto para quem não tem crianças [cite: 30]

    def __init__(self, num_quartos, tem_garagem, tem_criancas):
        super().__init__(tem_garagem)
        self.num_quartos = num_quartos
        self.tem_criancas = tem_criancas

    def calcular_mensalidade(self):
        self.mensalidade_total = self.VALOR_BASE_1Q
        
        # 1. Acréscimo por número de quartos
        if self.num_quartos == 2:
            self.mensalidade_total += self.ACRESCIMO_2Q

        # 2. Acréscimo da Garagem (R$ 300,00)
        self.mensalidade_total += self._aplicar_acrescimo_garagem()

        # 3. Desconto por não ter crianças (5%)
        if not self.tem_criancas:
            self.mensalidade_total *= (1 - self.DESCONTO_SEM_CRIANCAS)
            
        return self.mensalidade_total

class Casa(Imovel):
    """Implementa as regras de cálculo para Casas."""
    VALOR_BASE_1Q = 900.00  # R$ 900,00/ 1 Quarto [cite: 18]
    ACRESCIMO_2Q = 250.00   # Acréscimo por 2 quartos [cite: 27]

    def __init__(self, num_quartos, tem_garagem):
        super().__init__(tem_garagem)
        self.num_quartos = num_quartos

    def calcular_mensalidade(self):
        self.mensalidade_total = self.VALOR_BASE_1Q

        # 1. Acréscimo por número de quartos
        if self.num_quartos == 2:
            self.mensalidade_total += self.ACRESCIMO_2Q

        # 2. Acréscimo da Garagem (R$ 300,00)
        self.mensalidade_total += self._aplicar_acrescimo_garagem()
            
        return self.mensalidade_total

class Estudio(Imovel):
    """Implementa as regras de cálculo específicas para Estúdios."""
    VALOR_BASE = 1200.00    # R$ 1200,00 [cite: 19]
    VALOR_ESTAC_2_VAGAS = 250.00  # 2 vagas custam R$ 250,00 [cite: 29]
    VALOR_ESTAC_ADICIONAL = 60.00 # R$ 60,00 por vaga adicional [cite: 29]

    def __init__(self, num_vagas_estacionamento):
        # O Estúdio não usa a lógica simples de garagem da classe base
        super().__init__(False) 
        self.num_vagas = num_vagas_estacionamento
        
    def _aplicar_acrescimo_estacionamento(self):
        """Calcula o acréscimo específico para vagas de Estúdio."""
        if self.num_vagas == 0:
            return 0.0
        
        # 2 vagas custam R$ 250,00
        acrescimo = self.VALOR_ESTAC_2_VAGAS 
        
        # Vagas adicionais (acima de 2) custam R$ 60,00 cada
        if self.num_vagas > 2:
            vagas_adicionais = self.num_vagas - 2
            acrescimo += vagas_adicionais * self.VALOR_ESTAC_ADICIONAL
            
        return acrescimo
    def calcular_mensalidade(self):
        self.mensalidade_total = self.VALOR_BASE
        
        # Acréscimo do Estacionamento
        self.mensalidade_total += self._aplicar_acrescimo_estacionamento()
            
        return self.mensalidade_total

# --- FUNÇÃO DE GERAÇÃO DE CSV ---

def gerar_csv_parcelas(imovel_objeto, nome_arquivo="orcamento.csv"):
    """
    [cite_start]Gera um arquivo CSV com as 12 parcelas do orçamento mensal[cite: 32].
    """
    # Certifica-se de que o cálculo foi feito
    if imovel_objeto.mensalidade_total == 0.0:
        imovel_objeto.calcular_mensalidade()
        
    mensalidade = imovel_objeto.mensalidade_total
    
    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Cabeçalho do CSV
            writer.writerow(["Mês", "Parcela Mensalidade (R$)", "Observação"])
            
            # Geração das 12 parcelas
            for mes in range(1, 13):
                writer.writerow([mes, f"{mensalidade:.2f}", "Aluguel Mensal Orçado"])

        print(f"\nArquivo '{nome_arquivo}' gerado com sucesso!")
        
    except IOError:
        print(f"Erro ao tentar escrever no arquivo: {nome_arquivo}")

# --- EXEMPLO DE USO / SIMULAÇÃO ---

def simular_orcamentos():
    # Exemplo 1: Apartamento
    # CÁLCULO: (R$ 700 base + R$ 200 por 2 quartos + R$ 300 garagem) * 0.95 (5% de desconto)
    # R$ 1200 * 0.95 = R$ 1140,00
    apto1 = Apartamento(num_quartos=2, tem_garagem=True, tem_criancas=False)
    apto1.calcular_mensalidade()

    print("--- SIMULAÇÃO DE ORÇAMENTO 1: APARTAMENTO ---")
    print("Características: 2 Quartos, com Garagem, SEM Crianças (aplica 5% desc.)")
    resumo_apto = apto1.get_resumo()

    print(f"Aluguel Mensal Orçado: R$ {resumo_apto['Aluguel Mensal Orçado']:.2f}")
    print(f"Valor do Contrato: R$ {resumo_apto['Valor do Contrato']:.2f}")
    print(f"Parcelamento do Contrato: {resumo_apto['Parcelamento do Contrato']}")
    gerar_csv_parcelas(apto1, "orcamento_apto_ex1.csv")

    print("\n" + "="*50 + "\n")

    # Exemplo 2: Casa
    # CÁLCULO: R$ 900 base + R$ 250 por 2 quartos + R$ 0 garagem
    # R$ 1150,00
    casa1 = Casa(num_quartos=2, tem_garagem=False)
    casa1.calcular_mensalidade()

    print("--- SIMULAÇÃO DE ORÇAMENTO 2: CASA ---")
    print("Características: 2 Quartos, SEM Garagem.")
    resumo_casa = casa1.get_resumo()

    print(f"Aluguel Mensal Orçado: R$ {resumo_casa['Aluguel Mensal Orçado']:.2f}")
    print(f"Valor do Contrato: R$ {resumo_casa['Valor do Contrato']:.2f}")
    print(f"Parcelamento do Contrato: {resumo_casa['Parcelamento do Contrato']}")
    gerar_csv_parcelas(casa1, "orcamento_casa_ex2.csv")
    
    print("\n" + "="*50 + "\n")
    
    # Exemplo 3: Estúdio
    # CÁLCULO: R$ 1200 base + R$ 250 por 2 vagas + (1 vaga adicional * R$ 60)
    # R$ 1200 + R$ 250 + R$ 60 = R$ 1510,00
    estudio1 = Estudio(num_vagas_estacionamento=3)
    estudio1.calcular_mensalidade()

    print("--- SIMULAÇÃO DE ORÇAMENTO 3: ESTÚDIO ---")
    print("Características: 3 Vagas de Estacionamento.")
    resumo_estudio = estudio1.get_resumo()

    print(f"Aluguel Mensal Orçado: R$ {resumo_estudio['Aluguel Mensal Orçado']:.2f}")
    print(f"Valor do Contrato: R$ {resumo_estudio['Valor do Contrato']:.2f}")
    print(f"Parcelamento do Contrato: {resumo_estudio['Parcelamento do Contrato']}")
    gerar_csv_parcelas(estudio1, "orcamento_estudio_ex3.csv")


if __name__ == "__main__":
    simular_orcamentos()