# kaggle 房價預測模型 -> 利用Random Forest Regressor
# 不容易有overfitting的問題，因為在建模的時候就有兩個隨機性(隨機抽樣、隨機選取分類特徵)

# 隨機森林模型是集成式(ensemble)的模型，等於是把這片隨機森林裡面所有決策樹的效果集合起來，
# 一棵決策樹模型會根據餵給他的資料去決定每個節點要用什麼特徵去split這群資料，而每棵決策樹最後停止的葉節點裡面只有兩種可能的情況，
# 一種是資料已經被分到到達這個葉節點(leaf node)的時候只剩下一筆，沒辦法再分成兩類；另一種是現在這個葉節點裡的資料全部都是同一個類別或同一個值，
# 所以利用決策樹模型預測資料的時候，這筆新的資料餵進去，它會從根節點(root node)開始根據每一個它遇到的節點往下走，
# 最後走到的那個葉節點的類別或數值就是它的預測結果，而隨機森林模型做預測的時候是把這筆新的資料同時餵給這片森林裡面的每棵樹，
# 每棵樹都會給出一個針對這筆資料的預測結果，如果是分類問題的話，會依據票數多寡，最多棵樹產生出來的結果就會是這個隨機森林模型預測出來的最終結果，
# 如果是預測數值的問題，就會根據每棵樹所佔的權重加權每棵樹預測出來的數值，最後加權算出來的數值就是這個隨機森林模型的預測結果。

import pandas as pd
melb_data = pd.read_csv(r"C:\Users\馮滸\OneDrive\桌面\python training\kaggle\melb_data.csv")
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
melb_model = DecisionTreeRegressor(random_state = 1)
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
from sklearn.ensemble import RandomForestRegressor
forest_model = RandomForestRegressor(random_state = 1)
forest_model.fit(train_X, train_y)
melb_predictions = forest_model.predict(val_X)
print("Random Forest Model的MAE:", mean_absolute_error(val_y, melb_predictions))