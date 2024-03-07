import requests 
import pandas as pd
import json

page_no=0


# Declaring lists to store each coloumn value separately
id               = []
model_name       = []
image_url        = []
size             = []
avgRating        = []
market_price     = []
lenscart_price   = []
color            = []
width            = []
brand_name       = []
totalNoOfRatings = []
purchaseCount    = []
qty              = []


# Pagination is done by dynamically incrementing the pageno
while True:

    # getting the Json containing the sunglasses info from API
    response = requests.get(f"https://api-gateway.juno.lenskart.com/v2/products/category/3362?page-size=1000&page={page_no}")
    data = json.loads(response.content)
    length = len(data['result']["product_list"])
    
    # condtion to stop pagination
    if length == 0:
        break

    for i in range(length):
        id.append(data['result']["product_list"][i]['id'])
        brand_name.append(data['result']["product_list"][i]['brand_name'])
        purchaseCount.append(data['result']["product_list"][i]['purchaseCount'])
        model_name.append(data['result']["product_list"][i]['model_name'])
        image_url.append(data['result']["product_list"][i]['image_url'])
        size.append(data['result']["product_list"][i]['size'])
        avgRating.append(data['result']["product_list"][i]['avgRating'])
        market_price.append(data['result']["product_list"][i]['prices'][0]['price'])
        lenscart_price.append(data['result']["product_list"][i]['prices'][1]['price'])
        qty.append(data['result']["product_list"][i]['qty'])

        # handeling missing data
        if 'color' in data['result']["product_list"][i]:
            color.append(data['result']["product_list"][i]['color'])
        else:
            color.append(None)

        if('width') in data['result']["product_list"][i]:
            width.append(data['result']["product_list"][i]['width'])
        else:
            width.append(None)

        if('totalNoOfRatings') in data['result']["product_list"][i]:
            totalNoOfRatings.append(data['result']["product_list"][i]['totalNoOfRatings'])
        else:
            totalNoOfRatings.append(0)

        url = data['result']["product_list"][i]["product_url"]
        # product_details = requests.get(url)
    page_no+=1


# Data frame is created using all list coloumns
df = pd.DataFrame(
    {
        "id"               : id,
        "model_name"       : model_name,
        "brand_name"       : brand_name,
        "image_url"        : image_url,
        "market_price"     : market_price,
        "lenscart_price"   : lenscart_price,
        "purchaseCount"    : purchaseCount,
        "size"             : size,
        "color"            : color,
        "width"            : width,
        "totalNoOfRatings" : totalNoOfRatings,
        "avgRating"        : avgRating,
        "quantity"         : qty
    }
)

# DataFrame is converted to an excel file
df.to_excel('SunGlassesTot.xlsx', index=False)


