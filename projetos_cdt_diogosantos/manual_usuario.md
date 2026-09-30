# 📖 Manual do Usuário — Nação dos Mantos

## ⚽ Sobre o sistema

O Nação dos Mantos é uma loja virtual de camisas de futebol brasileiras desenvolvida em Python.

O sistema permite que o usuário consulte produtos, faça pedidos, acompanhe suas compras e avalie os produtos.

---

## 👤 Cadastro

Para utilizar a loja, o usuário pode criar uma conta informando seus dados.

Depois do cadastro, poderá entrar no sistema utilizando suas credenciais.

---

## 🔐 Login

Na tela inicial, informe:

- Usuário
- Senha

Depois, clique para entrar.

---

## 🛍️ Catálogo

No catálogo é possível visualizar as camisas disponíveis, seus preços e informações dos produtos.

O usuário pode escolher uma camisa para adicioná-la ao carrinho.

---

## 🛒 Carrinho

No carrinho, o usuário pode:

- Visualizar os produtos escolhidos
- Conferir os preços
- Alterar a quantidade
- Remover produtos
- Finalizar o pedido

---

## 👕 Personalização

Algumas camisas podem receber personalização.

A personalização possui um valor adicional de **R$ 20,00**.

---

## 🎟️ Cupons e descontos

O sistema possui recursos relacionados a descontos e cupons, que podem ser utilizados durante o processo de compra quando disponíveis.

---

## 📦 Pedidos

Após finalizar uma compra, o sistema registra o pedido.

O usuário pode consultar informações relacionadas ao seu pedido.

---

## 🚚 Rastreamento

O sistema possui acompanhamento do status dos pedidos, permitindo consultar a situação da compra.

---

## ⭐ Avaliações

Após uma compra, o usuário pode utilizar o sistema de avaliações para registrar sua opinião sobre os produtos.

---

## 🌙 Aparência

O sistema possui suporte a diferentes modos de aparência, incluindo modo claro e modo escuro.

---

## 👨‍💼 Área administrativa

O sistema possui uma área destinada ao administrador.

Nela podem existir funções relacionadas a:

- Produtos
- Estoque
- Pedidos
- Avaliações
- Estatísticas
- Gerenciamento da loja

---

## 💾 Dados do sistema

O sistema utiliza SQLite para armazenar informações da loja e arquivos JSON para determinados dados locais.

Esses arquivos são gerados/atualizados durante a utilização do programa.

---

## ▶️ Execução

Para instalar as dependências:

```bash
pip install -r requirements.txt