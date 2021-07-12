from hotel.models import HotelRoom, RoomDescription
from registration.models import *
from user.models import RoomReservation, Ratings
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import numpy as np


def getRecommendedHotel(query_index):
    df_hotels = pd.DataFrame(HotelRegistration.objects.all().values('hotelid', 'hotelname'))
    df_hotels.columns = ['hotelIdStr', 'hotelName']
    df_ratings = pd.DataFrame(
        Ratings.objects.all().values('userid', 'hotelid', 'ServiceRatings', 'CleanlinessRatings', 'LocationRatings',
                                     'SleepQualityRatings', 'RoomsRatings'))
    df_ratings.columns = ['userId', 'hotelId', 'Service_Ratings', 'Cleanliness_Ratings', 'Location_Ratings',
                          'SleepQuality_Ratings', 'Rooms_Ratings']
    df_users = pd.DataFrame(UserRegistration.objects.all().values('userid'))
    df_users.columns = ['userIdStr']

    def get_int(x):
        values = pd.unique(x)
        ston = dict(zip(values, range(len(values))))
        return x.replace(ston)

    df_users['userId'] = get_int(df_users['userIdStr'])
    df_hotels['hotelId'] = get_int(df_hotels['hotelIdStr'])

    m1 = df_users.set_index('userIdStr')['userId'].to_dict()
    v1 = df_ratings.filter(like='userId')
    df_ratings[v1.columns] = v1.replace(m1)

    m2 = df_hotels.set_index('hotelIdStr')['hotelId'].to_dict()
    v2 = df_ratings.filter(like='hotelId')
    df_ratings[v2.columns] = v2.replace(m2)
    df_ratings['rating'] = df_ratings[
        ['Service_Ratings', 'Cleanliness_Ratings', 'Location_Ratings', 'SleepQuality_Ratings', 'Rooms_Ratings']].mean(
        axis=1)
    df = pd.merge(df_ratings, df_hotels, on='hotelId')
    combine_hotel_rating = df.dropna(axis=0, subset=['hotelName'])
    hotel_ratingCount = (combine_hotel_rating.
        groupby(by=['hotelName'])['rating'].
        count().
        reset_index().
        rename(columns={'rating': 'totalRatingCount'})
    [['hotelName', 'totalRatingCount']]
        )
    rating_with_totalRatingCount = combine_hotel_rating.merge(hotel_ratingCount, left_on='hotelName',
                                                              right_on='hotelName', how='left')
    # Basic information about dataset
    pd.set_option('display.float_format', lambda x: '%3f' % x)
    # print(hotel_ratingCount['totalRatingCount'].describe())
    popularity_threshold = 5
    rating_popular_hotel = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
    # print(rating_popular_hotel)

    # Create a pivot matrix
    hotel_features_df = rating_popular_hotel.pivot_table(index='hotelId', columns='userId', values='rating').fillna(0)

    hotel_features_df_matrix = csr_matrix(hotel_features_df.values)

    # Fit pivot matrix to knn
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(hotel_features_df_matrix)

    distances, indices = model_knn.kneighbors(hotel_features_df.iloc[query_index, :].values.reshape(1, -1),
                                              n_neighbors=10)
    # for i in range(0, len(distances.flatten())):
    #     if i == 0:
    #         print('Recommendation for {0}\n'.format(hotel_features_df.index[query_index]))
    #     else:
    #         print('{0}: {1}, with distance of {2} '.format(i, hotel_features_df.index[indices.flatten()[i]],
    #                                                        distances.flatten()[i]))

    def get_recommendation(query_index):
        distances, indices = model_knn.kneighbors(hotel_features_df.iloc[query_index, :].values.reshape(1, -1),
                                                  n_neighbors=10)
        # for i in range(0, len(distances.flatten())):
        #     if i == 0:
        #         print('Recommendation for {0}\n'.format(hotel_features_df.index[query_index]))
        #     else:
        #         print('{0}: {1}, with distance of {2} '.format(i, hotel_features_df.index[indices.flatten()[i]],
        #                                                        distances.flatten()[i]))

    best_hotel_int_ids = []

    def get_recommendation_list(query_index):
        distances, indices = model_knn.kneighbors(hotel_features_df.iloc[query_index, :].values.reshape(1, -1),
                                                  n_neighbors=450)
        for i in range(0, len(distances.flatten())):
            if i == 0:
                None
            else:
                best_hotel_int_ids.append(hotel_features_df.index[indices.flatten()[i]])

    get_recommendation_list(query_index)
    # print(best_hotel_int_ids)
    best_hotel_str_ids = []
    for i in best_hotel_int_ids:
        value = df_hotels._get_value(i, 'hotelIdStr')
        best_hotel_str_ids.append(value)
    # print(best_hotel_str_ids)
    return best_hotel_str_ids
