from sentence_transformers import SentenceTransformer
from torch.utils.data import DataLoader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from src.job_scraper.utils import time_it
from data_manager import DataProcessor


class JobMatcher:
    def __init__(self, model_name: str = 'dunzhang/stella_en_1.5B_v5', batch_size: int = 64):
        self.model = SentenceTransformer(model_name)
        self.batch_size = batch_size
        self.data_processor = DataProcessor()

    def batch_encode(self, texts):
        dataloader = DataLoader(texts, batch_size=self.batch_size)
        all_embeddings = []    
        for batch in dataloader:
            batch_embeddings = self.model.encode(batch)
            all_embeddings.extend(batch_embeddings)
        return all_embeddings
    
    @staticmethod
    def vector_search(resume_vector, job_vectors, top_n=5):
        similarities = cosine_similarity([resume_vector], job_vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:top_n]
        return top_indices, similarities[top_indices]

    def bm25_search(self, resume, job_list, top_n=5):
        tokenized_docs = [self.data_processor.clean_text(job, for_bm25 = True).split() for job in job_list]
        bm25 = BM25Okapi(tokenized_docs)
        tokenized_query = self.data_processor.clean_text(resume, for_bm25 = True).split()
        scores = bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_n]
        return top_indices, scores

    @staticmethod
    def reciprocal_rank_fusion(ranked_lists, k=60):
        scores = {}
        for ranked_list in ranked_lists:
            for rank, index in enumerate(ranked_list):
                if index not in scores:
                    scores[index] = 0
                scores[index] += 1 / (k + rank + 1)
        final_ranking = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return final_ranking
    
    @time_it
    def get_final_ranking(self, resume_text, job_texts, top_n=5):
        bm25_indices, _ = self.bm25_search(resume_text, job_texts, top_n=top_n)    
        job_vectors = self.batch_encode([self.data_processor.clean_text(job) for job in job_texts])
        resume_vector = self.model.encode([self.data_processor.clean_text(resume_text)])[0]
        vector_indices, _ = self.vector_search(resume_vector, job_vectors, top_n=top_n)
        combined_ranking = self.reciprocal_rank_fusion([bm25_indices, vector_indices], k=top_n)
        final_ranking = [(index, score) for index, score in combined_ranking[:top_n]]
        return final_ranking