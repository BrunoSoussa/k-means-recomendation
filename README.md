# 📚 Sistema de Recomendação de Livros com K-Nearest Neighbors

## Visão Geral

Sistema avançado de recomendação de livros que utiliza o algoritmo K-Nearest Neighbors (KNN) para gerar recomendações personalizadas baseadas em similaridade de preferências de usuários. O sistema implementa uma abordagem de filtragem colaborativa eficiente para prever e recomendar livros com base nos padrões de avaliação dos usuários.

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4.1-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Características

- **Algoritmo KNN Otimizado**: Implementação eficiente do K-Nearest Neighbors para cálculo de similaridade entre livros
- **Filtragem Colaborativa**: Sistema baseado em ratings de usuários para recomendações mais precisas
- **Tratamento de Dados Robusto**: Limpeza e processamento eficiente de datasets
- **Design Orientado a Objetos**: Arquitetura modular e extensível
- **Documentação Completa**: Documentação detalhada com type hints e docstrings
- **Tratamento de Erros**: Sistema robusto de tratamento de exceções

## 🔧 Arquitetura

### Core do Sistema (`recomendation.py`)
- **Classe `BookRecommendation`**: 
  - Data class para encapsulamento de recomendações
  - Atributos tipados para título e score de similaridade
  
- **Classe `BookRecommender`**: 
  - Processamento de dados com Pandas
  - Implementação do algoritmo KNN da scikit-learn
  - Sistema robusto de tratamento de erros
  - Documentação completa com type hints
  - Métodos para carregamento e processamento de dados
  - Geração de recomendações baseadas em similaridade

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/book-recommendation-system.git
cd book-recommendation-system
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📊 Datasets

O sistema utiliza dois datasets principais:
- `BX-Books.csv`: Informações sobre livros (ISBN, título, autor)
- `BX-Book-Ratings.csv`: Ratings de usuários para livros

### Formato dos Datasets

#### BX-Books.csv
```csv
ISBN;Title;Author
0195153448;Classical Mythology;Mark P. O. Morford
```

#### BX-Book-Ratings.csv
```csv
User-ID;ISBN;Rating
276725;034545104X;0
```

## 💻 Uso

```python
from recomendation import BookRecommender

# Inicializar o sistema
recommender = BookRecommender(
    books_file='BX-Books.csv',
    ratings_file='BX-Book-Ratings.csv',
    min_book_ratings=100,  # Filtrar livros com menos de 100 ratings
    min_user_ratings=10    # Filtrar usuários com menos de 10 ratings
)

# Obter recomendações para um livro
recommendations = recommender.get_recommendations(
    book_title="The Fellowship of the Ring",
    n_recommendations=5
)

# Processar as recomendações
for rec in recommendations:
    print(f"Livro: {rec.title}")
    print(f"Score de Similaridade: {rec.similarity_score:.3f}\n")
```

## ⚙️ Configuração

Parâmetros principais do sistema:
```python
BookRecommender(
    min_book_ratings=100,  # Mínimo de ratings por livro
    min_user_ratings=10    # Mínimo de ratings por usuário
)
```

## 🔍 Métricas e Performance

- **Similaridade**: 
  - Baseada na distância do cosseno entre vetores de ratings
  - Normalização automática dos scores
  - Otimização para sparse matrices

- **Filtragem**: 
  - Remove livros com menos de 100 ratings para maior qualidade
  - Filtra usuários com poucas interações
  - Reduz ruído e melhora precisão das recomendações

- **Performance**:
  - Processamento eficiente de grandes datasets
  - Otimização de memória com sparse matrices
  - Rápida geração de recomendações

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: nova funcionalidade'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 📫 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/book-recommendation-system](https://github.com/seu-usuario/book-recommendation-system)

## 🙏 Agradecimentos

- [Book-Crossing Dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/)
- [scikit-learn](https://scikit-learn.org/)
