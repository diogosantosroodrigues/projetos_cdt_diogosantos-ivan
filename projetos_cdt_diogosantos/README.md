# ⚽ Nação dos Mantos - Automação (Desktop)

Este é um aplicativo desktop completo para gerenciamento de pedidos de uma loja de camisas de futebol, desenvolvido em **Python** utilizando a biblioteca gráfica **Tkinter**[cite: 2, 6]. O sistema conta com banco de dados local para persistência de dados e automação de cadastros[cite: 2, 6].

---

## 🛠️ Tecnologias Utilizadas

* **Python 3** (Linguagem base)[cite: 6]
* **Tkinter** (Interface gráfica integrada)[cite: 2, 6]
* **SQLite3** (Banco de dados local e leve)[cite: 2, 6]
* **Pillow (PIL)** (Para manipulação e exibição dos escudos dos times em PNG)
* **Faker** (Para geração automática de nomes fictícios de clientes)[cite: 2]
* **JSON** (Para armazenamento de configurações gerais do sistema)[cite: 2]

---

## 🚀 Funcionalidades do Sistema

* **Seleção Dinâmica de Times:** Lista interativa com escudos e preços atualizados de diversos clubes de futebol.
* **Personalização de Camisas:** Opção de adicionar nome e número na camisa com cálculo automático de taxa adicional.
* **Carrinho de Compras:** Adiciona itens ao carrinho em tempo real com opção de remoção e recálculo automático de subtotal, frete e valor total.
* **Geração Automática de Cliente (Faker):** Preenchimento rápido de dados de teste com um único clique[cite: 2].
* **Checkout e Rastreio:** Finalização de pedidos com escolha da forma de pagamento e geração automática de código de rastreio (`NM******BR`).
* **Histórico de Pedidos:** Visualização completa dos pedidos armazenados no banco de dados SQLite[cite: 2].

---

## 📂 Estrutura Completa de Caminhos e Arquivos

Abaixo está o mapeamento exato de como os arquivos estão organizados no diretório do projeto após a compilação com o PyInstaller[cite: 2, 7]:

```text
📂 Área de Trabalho (Desktop)
└── 📂 projetos_cdt_matheussantos              # Pasta principal do projeto
    ├── 📂 build/                              # Arquivos temporários de compilação
    │   └── 📂 teste_lojacamisasdetimes_version_2.2/
    │       ├── 📂 localpycs/                  # Arquivos Python compilados (.pyc)
    │       ├── 📄 base_library.zip            # Biblioteca padrão do Python compactada
    │       ├── 📄 Analysis-00.toc             # Tabela de conteúdos da análise de dependências
    │       ├── 📄 EXE-00.toc                  # Metadados de criação do executável
    │       ├── 📄 PKG-00.toc                  # Metadados do pacote de arquivos
    │       └── 📄 PYZ-00.pyz & .toc           # Scripts Python compactados
    │
    ├── 📂 dist/                               # PASTA DO PROGRAMA PRONTO PARA USO
    │   └── 📂 teste_lojacamisasdetimes_version_2.2/
    │       ├── ⚙️ teste_lojacamisasdetimes_version_2.2.exe  # O Executável final do seu sistema (Aplicação)
    │       └── 🗄️ loja_camisas.db              # Banco de dados utilizado pelo Executável
    │
    ├── 📂 escudos/                            # Pasta com as imagens dos escudos dos times
    ├── 📄 configuracao.json                   # Arquivo de configuração JSON
    ├── 🗄️ loja_camisas.db                      # Banco de dados utilizado pelo código fonte .py
    ├── 🐍 main_cli.py                         # Versão em linha de comando (CLI - Tela Preta)
    ├── 🐍 teste_lojacamisasdetimes_version_2.2.py  # Seu código fonte original em Python (GUI)
    ├── 📄 teste_lojacamisasdetimes_version_2.2.spec # Arquivo de configuração de compilação do PyInstaller
    ├── 📄 requirements.txt                    # Lista de dependências do projeto
    └── 📄 README.md                           # Documentação do projeto