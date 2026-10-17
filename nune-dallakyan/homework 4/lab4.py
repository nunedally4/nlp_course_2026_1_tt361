import re
import collections
import numpy as np
import pandas as pd
import scipy.sparse as sp

from contextlib import redirect_stdout
import io
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# 1. SETTINGS

DATA_PATH = "bbc-text (1).csv"
TEST_SIZE = 0.20
RANDOM_STATE = 42


# 2. TEXT PREPROCESSING

def preprocess(text):
    text = str(text).lower()
    tokens = re.findall(r"[a-z]+", text)

    tokens = [
        word for word in tokens
        if len(word) > 1 and word not in ENGLISH_STOP_WORDS
    ]

    return tokens


# 3. BUILD VOCABULARY

def build_vocabulary(tokenized_docs):
    vocabulary = set()

    for doc in tokenized_docs:
        for word in doc:
            vocabulary.add(word)

    return sorted(vocabulary)


# 4. BAG OF WORDS FROM SCRATCH

def bow_vectorize(tokenized_docs, word_to_index):
    rows = []
    cols = []
    values = []

    for row_index, doc in enumerate(tokenized_docs):
        counts = collections.Counter()

        for word in doc:
            if word in word_to_index:
                counts[word] += 1

        for word, count in counts.items():
            rows.append(row_index)
            cols.append(word_to_index[word])
            values.append(count)

    matrix = sp.csr_matrix(
        (values, (rows, cols)),
        shape=(len(tokenized_docs), len(word_to_index)),
        dtype=float
    )

    return matrix


# 5. CALCULATE IDF FROM SCRATCH

def calculate_idf(bow_train):
    n_documents = bow_train.shape[0]

    document_frequency = np.asarray(
        (bow_train > 0).sum(axis=0)
    ).ravel()

    idf = np.log(
        n_documents / np.maximum(document_frequency, 1)
    )

    return idf, document_frequency


# 6. CALCULATE TF-IDF FROM SCRATCH

def calculate_tfidf(bow_matrix, idf):
    tfidf_matrix = bow_matrix.multiply(idf).tocsr()

    return tfidf_matrix


# 7. L2 NORMALIZATION

def l2_normalize(matrix):
    squared_values = matrix.multiply(matrix)

    squared_sums = np.asarray(
        squared_values.sum(axis=1)
    ).ravel()

    norms = np.sqrt(squared_sums)

    inverse_norms = np.divide(
        1.0,
        norms,
        out=np.zeros_like(norms),
        where=norms != 0
    )

    normalized_matrix = sp.diags(inverse_norms).dot(matrix)

    return normalized_matrix.tocsr()


# 8. TRAIN NEAREST CLASS CENTROID CLASSIFIER

def fit_centroids(X_train, y_train):
    class_names = sorted(set(y_train))
    centroids = []

    for class_name in class_names:
        class_rows = np.where(y_train == class_name)[0]

        class_vectors = X_train[class_rows]

        centroid = np.asarray(
            class_vectors.mean(axis=0)
        ).ravel()

        norm = np.linalg.norm(centroid)

        if norm > 0:
            centroid = centroid / norm

        centroids.append(centroid)

    centroids = np.vstack(centroids)

    return class_names, centroids


# 9. PREDICT CATEGORY USING COSINE SIMILARITY

def predict_by_cosine(X, class_names, centroids):
    similarities = X.dot(centroids.T)

    best_indices = np.asarray(similarities).argmax(axis=1)

    predictions = np.asarray(class_names)[best_indices]

    return predictions


# 10. ANALYZE TOP 10 WORDS FOR EACH CATEGORY

def analyze_category_words(
    tokenized_docs,
    labels,
    vocabulary,
    word_to_index,
    idf
):
    print("\nTOP 10 WORDS BY CATEGORY")

    for category in sorted(set(labels)):
        category_indices = np.where(labels == category)[0]

        category_docs = [
            tokenized_docs[i]
            for i in category_indices
        ]

        category_bow = bow_vectorize(
            category_docs,
            word_to_index
        )

        category_tfidf = calculate_tfidf(
            category_bow,
            idf
        )

        average_scores = np.asarray(
            category_tfidf.mean(axis=0)
        ).ravel()

        top_indices = np.argsort(average_scores)[::-1][:10]

        print(f"\nCategory: {category}")

        for index in top_indices:
            print(
                vocabulary[index],
                round(average_scores[index], 4)
            )


# 11. ANALYZE HIGH TF AND HIGH IDF WORDS

def analyze_tf_idf(
    bow_train,
    vocabulary,
    idf,
    document_frequency
):
    mean_tf = np.asarray(
        bow_train.mean(axis=0)
    ).ravel()

    print("\nTOP 10 WORDS BY MEAN TF")

    top_tf_indices = np.argsort(mean_tf)[::-1][:10]

    for index in top_tf_indices:
        print(
            vocabulary[index],
            "Mean TF:", round(mean_tf[index], 4),
            "IDF:", round(idf[index], 4),
            "Document Frequency:", int(document_frequency[index])
        )

    print("\nTOP 10 WORDS BY IDF")

    top_idf_indices = np.argsort(idf)[::-1][:10]

    for index in top_idf_indices:
        print(
            vocabulary[index],
            "Mean TF:", round(mean_tf[index], 4),
            "IDF:", round(idf[index], 4),
            "Document Frequency:", int(document_frequency[index])
        )


# 12. MAIN PROGRAM

def main():
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Check required columns
    if not {"category", "text"}.issubset(df.columns):
        raise ValueError(
            "CSV file must contain 'category' and 'text' columns."
        )

    # Remove missing values
    df = df.dropna(subset=["category", "text"]).reset_index(drop=True)

    # Preprocess articles
    tokenized_docs = [
        preprocess(text)
        for text in df["text"]
    ]

    labels = df["category"].astype(str).to_numpy()

    # Split data into training and testing sets
    indices = np.arange(len(df))

    train_idx, test_idx = train_test_split(
        indices,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=labels
    )

    train_docs = [
        tokenized_docs[i]
        for i in train_idx
    ]

    test_docs = [
        tokenized_docs[i]
        for i in test_idx
    ]

    y_train = labels[train_idx]
    y_test = labels[test_idx]

    # Build vocabulary using training data only
    vocabulary = build_vocabulary(train_docs)

    word_to_index = {
        word: index
        for index, word in enumerate(vocabulary)
    }

    # Create Bag of Words matrices
    X_train_bow = bow_vectorize(
        train_docs,
        word_to_index
    )

    X_test_bow = bow_vectorize(
        test_docs,
        word_to_index
    )

    # Calculate IDF using training data
    idf, document_frequency = calculate_idf(
        X_train_bow
    )

    # Calculate TF-IDF matrices
    X_train_tfidf = calculate_tfidf(
        X_train_bow,
        idf
    )

    X_test_tfidf = calculate_tfidf(
        X_test_bow,
        idf
    )

    # Normalize TF-IDF matrices
    X_train_norm = l2_normalize(
        X_train_tfidf
    )

    X_test_norm = l2_normalize(
        X_test_tfidf
    )

    # Train classifier
    class_names, centroids = fit_centroids(
        X_train_norm,
        y_train
    )

    # Predict categories
    predictions = predict_by_cosine(
        X_test_norm,
        class_names,
        centroids
    )

    # Evaluate results
    print("\nDATASET INFORMATION")
    print("Total articles:", len(df))
    print("Training articles:", len(train_idx))
    print("Testing articles:", len(test_idx))
    print("Number of categories:", len(set(labels)))
    print("Vocabulary size:", len(vocabulary))

    print("\nMATRIX SHAPES")
    print("Training BoW:", X_train_bow.shape)
    print("Testing BoW:", X_test_bow.shape)
    print("Training TF-IDF:", X_train_tfidf.shape)
    print("Testing TF-IDF:", X_test_tfidf.shape)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nMODEL ACCURACY")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Accuracy percentage: {accuracy * 100:.2f}%")

    print("\nCLASSIFICATION REPORT")
    print(
        classification_report(
            y_test,
            predictions,
            digits=4,
            zero_division=0
        )
    )

    # Analyze words by category
    analyze_category_words(
        tokenized_docs,
        labels,
        vocabulary,
        word_to_index,
        idf
    )

    # Analyze TF and IDF
    analyze_tf_idf(
        X_train_bow,
        vocabulary,
        idf,
        document_frequency
    )

if __name__ == "__main__":
    output = io.StringIO()

    with redirect_stdout(output):
        main()

    results = output.getvalue()

    print(results)

    with open("results.txt", "w", encoding="utf-8") as file:
        file.write(results)

    print("\nԱրդյունքները պահպանվեցին results.txt ֆայլում։")