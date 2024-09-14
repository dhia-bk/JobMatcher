from sentence_transformers import SentenceTransformer
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from src.data_manager.DataProcessor import DataProcessor


data_processor = DataProcessor() 
class JobMatcher:
    def __init__(self, model_name: str = 'dunzhang/stella_en_1.5B_v5', batch_size: int = 32):
        self.model = SentenceTransformer(model_name)
        self.batch_size = batch_size

    def batch_encode(self, df : pd.DataFrame) -> pd.DataFrame:
        texts = [data_processor.clean_text(job) for job in df['Description'].tolist()]
        dataloader = DataLoader(texts, batch_size=self.batch_size)
        all_embeddings = []    
        for batch in dataloader:
            batch_embeddings = self.model.encode(batch)
            all_embeddings.extend(batch_embeddings)
        result_df = pd.DataFrame({
            'job_id': df['ID'].values,  
            'job_embedding': all_embeddings  
        })
        return result_df
    
    def encode_resume(self, resume_text):
        return self.model.encode(resume_text)
    
    @staticmethod
    def vector_search(resume_vector, job_df):
        job_vectors = np.array(job_df['job_embedding'].tolist())
        job_ids = job_df['job_id'].tolist()
        similarities = cosine_similarity([resume_vector], job_vectors)[0]
        return pd.DataFrame({'job_id': job_ids, 'score': similarities})

    def bm25_search(self, resume, job_df):
        job_list = job_df['Description'].tolist()
        job_ids = job_df['ID'].tolist()
        tokenized_docs = [data_processor.clean_text(job, for_bm25=True).split() for job in job_list]
        bm25 = BM25Okapi(tokenized_docs)
        tokenized_query = data_processor.clean_text(resume, for_bm25=True).split()
        scores = bm25.get_scores(tokenized_query)
        return pd.DataFrame({'job_id': job_ids, 'score': scores})

    @staticmethod
    def reciprocal_rank_fusion(vector_df, bm25_df, k=60):
        bm25_df = bm25_df.rename(columns={'score': 'score_bm25_df'})        
        vector_df = vector_df.rename(columns={'score': 'score_vector_df'})
        combined_df = pd.concat([vector_df.set_index('job_id'), bm25_df.set_index('job_id')], axis=1, join='outer').fillna(0).reset_index()

        scores = {}
        if 'score_vector_df' in combined_df.columns:
            for rank, row in combined_df[['job_id', 'score_vector_df']].dropna().sort_values(by='score_vector_df', ascending=False).iterrows():
                index = row['job_id']
                score = row['score_vector_df']
                if index not in scores:
                    scores[index] = 0
                scores[index] += score / (k + rank + 1)
        else:
            print("Column 'score_vector_df' not found in combined_df")
        if 'score_bm25_df' in combined_df.columns:
            for rank, row in combined_df[['job_id', 'score_bm25_df']].dropna().sort_values(by='score_bm25_df', ascending=False).iterrows():
                index = row['job_id']
                score = row['score_bm25_df']
                if index not in scores:
                    scores[index] = 0
                scores[index] += score / (k + rank + 1)
        else:
            print("Column 'score_bm25_df' not found in combined_df")
        final_ranking = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return pd.DataFrame({'job_id': [index for index, _ in final_ranking], 'score': [score for _, score in final_ranking]})