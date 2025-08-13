# Building a Recommendation System: A Journey from Baseline to Tuning

Today, we embarked on a comprehensive journey to build and refine a recommendation system for Amazon beauty products. This log documents our process, from initial data exploration to in-depth model evaluation and hyperparameter tuning, and outlines the key findings and future directions.

## 1. Initial Setup and Data Exploration

We began with a dataset of user ratings for beauty products. The initial step involved loading the data and performing an exploratory data analysis (EDA) in a Jupyter notebook. This helped us understand the structure of the data, the distribution of ratings, and the number of users and items.

## 2. Building a Baseline Model: Alternating Least Squares (ALS)

Our first model was built using the **Alternating Least Squares (ALS)** algorithm from the `implicit` library. ALS is a powerful matrix factorization technique for collaborative filtering. After training the initial model, we realized we needed a robust way to evaluate its performance.

## 3. A Deeper Dive into Evaluation

A single performance metric can be misleading. To get a true picture of our model's performance, we implemented a rigorous evaluation script. This script:
- Sampled a large number of users (first 500, then 1000) from the test set.
- For each user, it calculated the **Precision@10**, which measures how many of the top 10 recommended items were actually relevant.

The results of this deep dive were eye-opening:

| Metric             | Value  |
| ------------------ | ------ |
| Mean Precision@10  | ~1.3%  |
| Median Precision@10| 0.0    |
| Max Precision@10   | 60.0%  |

The most critical insight was the **median precision of 0.0**. This meant that for at least half of our users, the model failed to recommend a single correct item. While the model worked very well for a few users (with a max precision of 60%), it was not generalizing well.

## 4. Systematic Hyperparameter Tuning

With a clear baseline and a solid evaluation strategy, we moved on to hyperparameter tuning to improve the model.

### Tuning `factors`
We first tuned the number of latent `factors`. The results showed that increasing the number of factors improved the mean precision, but the median precision remained at 0.

| Factors | Mean Precision | Median Precision |
| ------- | -------------- | ---------------- |
| 20      | 1.18%          | 0.0              |
| 50      | 1.51%          | 0.0              |
| 100     | 1.55%          | 0.0              |
| 150     | 1.62%          | 0.0              |
| 200     | 1.79%          | 0.0              |

### Tuning `regularization`
Next, we fixed the number of factors at 200 and tuned the `regularization` parameter. Again, we saw slight improvements in the mean precision, but no change in the median.

| Regularization | Mean Precision | Median Precision |
| -------------- | -------------- | ---------------- |
| 0.01           | 1.79%          | 0.0              |
| 0.1            | 1.76%          | 0.0              |
| 1.0            | 1.74%          | 0.0              |
| 10.0           | 1.55%          | 0.0              |
| 100.0          | 0.46%          | 0.0              |

## 5. Trying a Different Model: Bayesian Personalized Ranking (BPR)

Since we seemed to have hit a plateau with ALS, we experimented with a different model: **Bayesian Personalized Ranking (BPR)**. BPR is designed to optimize for ranking, which is exactly what we need. However, the results showed that BPR performed worse than ALS on this dataset, with a mean precision of only ~0.3%.

## 6. Conclusion and The Path Forward

Our extensive experiments led us to a clear conclusion: we have likely reached the limits of what purely collaborative filtering models can achieve with this dataset. The persistent zero median precision suggests that data sparsity is a major challenge.

The most logical and promising path forward is to build a **Hybrid Recommendation System**.

A hybrid model would combine our current collaborative filtering approach with a **content-based approach**. This involves using metadata about the items themselves, such as:
- Product brand
- Category
- Price
- Text from the description

By leveraging this item information, the model can make more intelligent recommendations, especially for users with few ratings. This is the standard industry practice for overcoming the "cold start" problem and building a truly robust recommendation engine.

We have successfully built and evaluated baseline models, and now have a clear, data-driven direction for the next phase of the project.