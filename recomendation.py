import pandas as pd
from sklearn.neighbors import NearestNeighbors
from typing import List
from dataclasses import dataclass
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class BookRecommendation:
    """Representa uma recomendação de livro com seu título e score de similaridade."""
    title: str
    similarity_score: float

class BookRecommender:
    """Sistema de recomendação de livros usando KNN baseado em ratings de usuários."""
    
    def __init__(self, books_file: str, ratings_file: str, min_book_ratings: int = 100, min_user_ratings: int = 10):
        """
        Inicializa o sistema de recomendação.

        Args:
            books_file: Caminho para o arquivo CSV de livros
            ratings_file: Caminho para o arquivo CSV de ratings
            min_book_ratings: Número mínimo de ratings que um livro deve ter
            min_user_ratings: Número mínimo de ratings que um usuário deve ter
        """
        self.min_book_ratings = min_book_ratings
        self.min_user_ratings = min_user_ratings
        self.model = None
        self.books_data = None
        
        try:
            self._load_and_process_data(books_file, ratings_file)
            self._train_model()
        except Exception as e:
            logging.error(f"Erro na inicialização do sistema: {str(e)}")
            raise

    def _load_and_process_data(self, books_file: str, ratings_file: str) -> None:
        """
        Carrega e processa os dados dos arquivos CSV.
        
        Args:
            books_file: Caminho para o arquivo CSV de livros
            ratings_file: Caminho para o arquivo CSV de ratings
            
        Raises:
            FileNotFoundError: Se os arquivos não forem encontrados
            pd.errors.EmptyDataError: Se os arquivos estiverem vazios
        """
        try:
            df_books = pd.read_csv(
                books_file,
                encoding="ISO-8859-1",
                sep=";",
                header=0,
                names=['isbn', 'title', 'author'],
                usecols=['isbn', 'title', 'author'],
                dtype={'isbn': 'str', 'title': 'str', 'author': 'str'}
            )

            df_ratings = pd.read_csv(
                ratings_file,
                encoding="ISO-8859-1",
                sep=";",
                header=0,
                names=['user', 'isbn', 'rating'],
                usecols=['user', 'isbn', 'rating'],
                dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'}
            )

  
            df_books.dropna(inplace=True)
            
       
            active_users = df_ratings['user'].value_counts()
            active_users = active_users[active_users > self.min_user_ratings].index
            df_ratings = df_ratings[df_ratings['user'].isin(active_users)]
            
   
            frequent_books = df_ratings['isbn'].value_counts()
            frequent_books = frequent_books[frequent_books > self.min_book_ratings].index
            df_ratings = df_ratings[df_ratings['isbn'].isin(frequent_books)]
            
      
            df_merged = pd.merge(df_ratings, df_books, on='isbn')
            self.books_data = df_merged.pivot_table(
                index=['user'],
                columns=['isbn'],
                values='rating'
            ).fillna(0).T
            
            self.books_data.index = self.books_data.join(df_books.set_index('isbn'))['title']
            
            logging.info(f"Dados carregados com sucesso. Shape da matriz de ratings: {self.books_data.shape}")
            
        except FileNotFoundError as e:
            logging.error(f"Arquivo não encontrado: {str(e)}")
            raise
        except pd.errors.EmptyDataError as e:
            logging.error(f"Arquivo vazio ou corrompido: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Erro no processamento dos dados: {str(e)}")
            raise

    def _train_model(self) -> None:
        """
        Treina o modelo KNN usando a métrica de similaridade por cosseno.
        
        Raises:
            ValueError: Se os dados não foram carregados corretamente
        """
        if self.books_data is None:
            raise ValueError("Dados não foram carregados corretamente")
        
        try:
            self.model = NearestNeighbors(metric='cosine')
            self.model.fit(self.books_data.values)
            logging.info("Modelo treinado com sucesso")
        except Exception as e:
            logging.error(f"Erro no treinamento do modelo: {str(e)}")
            raise

    def get_recommendations(self, book_title: str, n_recommendations: int = 10) -> List[BookRecommendation]:
        """
        Obtém recomendações de livros similares ao título fornecido.

        Args:
            book_title: Título do livro para buscar recomendações
            n_recommendations: Número de recomendações desejadas

        Returns:
            Lista de BookRecommendation com as recomendações

        Raises:
            ValueError: Se o título do livro não for encontrado
            RuntimeError: Se o modelo não estiver treinado
        """
        if self.model is None:
            raise RuntimeError("Modelo não está treinado")
            
        try:
            if book_title not in self.books_data.index:
                raise ValueError(f"Livro '{book_title}' não encontrado na base de dados")
            
            idx = self.books_data.index.get_loc(book_title)
            book_values = self.books_data.iloc[idx, :].values.reshape(1, -1)
            
            distances, indices = self.model.kneighbors(book_values, n_recommendations + 1)
            
            recommendations = []
            for distance, index in zip(distances.flatten()[1:], indices.flatten()[1:]):
                recommendations.append(
                    BookRecommendation(
                        title=self.books_data.index[index],
                        similarity_score=1 - distance  # Converte distância em score de similaridade
                    )
                )
            
            return recommendations
            
        except Exception as e:
            logging.error(f"Erro ao gerar recomendações: {str(e)}")
            raise

def main():
    """Função principal para demonstração do sistema."""
    try:

        recommender = BookRecommender('dataset_books/BX-Books.csv', 'dataset_books/BX-Book-Ratings.csv')
        
        
     
        book_title = "Jewel"
        recommendations = recommender.get_recommendations(book_title, n_recommendations=5)
        
        print(f"\nRecomendações para: {book_title}\n")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec.title} (Score: {rec.similarity_score:.3f})")
            
    except Exception as e:
        logging.error(f"Erro na execução: {str(e)}")
        raise

if __name__ == "__main__":
    main()

