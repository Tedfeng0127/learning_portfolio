# random forest classifier跟decision tree regressor的概念是什麼啊？

import pandas as pd
melb_data = pd.read_csv("melb_data.csv")
print("全部資料的描述:\n", melb_data.describe())    
print("全部資料的最前面五筆:\n", melb_data.head())   
print("全部資料的最後五筆:\n", melb_data.tail())
print("所有特徵:\n", melb_data.columns)             # 印出全部的features
melb_data = melb_data.dropna(axis = 0)             # 去除缺值的資料
y = melb_data.Price
print("Prediction Target:\n", y)
t1 = melb_data.iloc[0]
print("第一筆資料:\n", t1)
print("第一筆資料的第三個column(地址):\n", t1[2])
melb_data_features = ["Rooms", "Bathroom", "Landsize", "Lattitude", "Longtitude"]
X = melb_data[melb_data_features]                  # 選擇要用來訓練模型的特徵(變數、column)
print("被選到的features的資料描述:\n", X.describe())
print("被選到的features的前五筆資料:\n", X.head())


from sklearn.tree import DecisionTreeRegressor
# Define model
melb_model = DecisionTreeRegressor(random_state = 1)     # random_state = 1 是什麼意思啊？
# Fit model
melb_model.fit(X, y)
# 拿前五筆房屋資料來預測
print("根據這五間房屋的特徵，預測結果為:\n", melb_model.predict(X.head()))
print("這五間房屋的實際結果為:\n", list(y.head()))


# 計算模型的MAE(Mean Absolute Error)
from sklearn.metrics import mean_absolute_error
predicted_home_prices = melb_model.predict(X)
print("這個模型的MAE:\n", mean_absolute_error(y, predicted_home_prices))


# 把資料分成training data和validation data
from sklearn.model_selection import train_test_split
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 0)
# Define model 跟上面的melb_model不一樣的model
melbourne_model = DecisionTreeRegressor()
# Fit model
melbourne_model.fit(train_X, train_y)
# 用這個新train的model去預測valdation data的結果
val_predictions = melbourne_model.predict(val_X)
print("新模型的MAE:\n", mean_absolute_error(val_y, val_predictions))


# 比較不同max_leaf_nodes的mae大小
def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):   # max_leaf_nodes 跟 depth 有什麼不一樣？
    model = DecisionTreeRegressor(max_leaf_nodes = max_leaf_nodes, random_state = 0)
    model.fit(train_X, train_y)
    predict_values = model.predict(val_X)
    mae = mean_absolute_error(val_y, predict_values)
    return mae

print("不同max_leaf_nodes時的MAE:")
for max_leaf_nodes in [5, 50, 500, 5000]:
    my_mae = get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y)
    print("Max leaf nodes: %d \t\t Mean Absolute Error: %d" %(max_leaf_nodes, my_mae))
mae = {max_leaf_nodes:get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y) for max_leaf_nodes in [5, 50, 500, 5000]}
best_tree_size = min(mae, key = mae.get)
print("決策樹最適大小:", best_tree_size)


# Random Forest Model 隨機森林模型
from sklearn.ensemble import RandomForestRegressor    # RandomForestClassifier 跟 RandomForestRegressor差在哪啊？
forest_model = RandomForestRegressor(random_state = 1)
forest_model.fit(train_X, train_y)
melb_predictions = forest_model.predict(val_X)
print("Random Forest Model的MAE:", mean_absolute_error(val_y, melb_predictions))