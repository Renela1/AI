import pandas as pd 
import numpy as np

r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('data/movies_data.txt', sep='\t', names= r_cols, usecols=range(3))

MovieProperties = ratings.groupby('movie_id').agg({'rating':[np.size, np.mean]})

pmp = MovieProperties.head(10)

MovieRating = pd.DataFrame(MovieProperties['rating']['size'])

pmp2 = MovieRating.head(10)

MnormalizedR = MovieRating.apply(lambda x: (x-np.min(x)) / (np.max(x) - np.min(x)) )
# print(MnormalizedR.head(10))

MovieDictionary = {}

with open('data/movies_item.txt') as f:
    for line in f:

        fields = line.rstrip('\n').split('|')
        movieId = int(fields[0])
        name = fields[1]
        genre = [int(x) for x in fields[5:25]]
        genres = map(int, genre)
        MovieDictionary[movieId] = (name, genre, MnormalizedR.loc[movieId].get('size'),
                                    MovieProperties.loc[movieId].rating.get('mean'))

# print(MovieDictionary[1])

from scipy import spatial

def compute_distance(a, b):

    genre_a = a[1]
    genre_b = b[1]

    genre_distance = spatial.distance.cosine(genre_a, genre_b)

    poppularitie_a = a[2]
    poppularitie_b = b[2]

    poppularite_distance = abs(poppularitie_a - poppularitie_b)#absoulute number

    return genre_distance + poppularite_distance

# print(compute_distance(MovieDictionary[2], MovieDictionary[3]))


import operator
def get_neighbors(movie_id, n):
    distances=[]

    for id in MovieDictionary:

        if id != movie_id:

            dist = compute_distance(MovieDictionary[id], MovieDictionary[movie_id])
            distances.append((id, dist))

    distances.sort(key= operator.itemgetter(1))
    neighbors = []

    for x in range(n):
        neighbors.append(distances[x][0])
    
    return neighbors


for movie_id in get_neighbors(1, 10):

    print(MovieDictionary[movie_id])

k = 10

average_rating = 0
neighbors = get_neighbors(1, k)

for neighbor in neighbors:
    average_rating += MovieDictionary[neighbor][3]
    print(f'{MovieDictionary[neighbor][0]}: {MovieDictionary[neighbor][3]}')

average_rating /= float(k)
print(average_rating)