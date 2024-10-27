# [BEAUTY FROM THE SEOUL](http://muhammad-ghaza31-beautyfromtheseoul.pbp.cs.ui.ac.id/)

## Group Members
1. [Anindiyo Banu Prabasworo - 2306256236](https://github.com/skibidiyo)
2. [Athazahra Nabila Ruby - 2306173113](https://github.com/thataruby)
3. [Kayla Soraya Djakaria - 2306256381](https://github.com/luticakep)
4. [Min Kim - 2306199743](https://github.com/wuyu0107)
5. [Muhammad Ghaza Fadhlibaqi - 2306173321](https://github.com/GhazaFadhlilbaqi)
6. [Muhammad Jordan Ar-Razi Aziz - 2306173555](https://github.com/jordanaziz18)

## Application Description
The proposed application, Beauty from the Seoul, serves as a comprehensive guide for skincare enthusiasts visiting or living in Seoul, South Korea. As a city renowned for its skincare products, Seoul boasts a diverse range of brands and types of skincare items. This application aims to help users easily find information about various skincare products, as it can be overwhelming to choose from the vast amount of selection available.

By providing detailed product listings, user reviews, store locations, and promotion events, our application will empower users to make informed purchasing decisions——or to get your money's worth, as they say——while exploring Seoul's vibrant beauty scene.

## Modules to be Implemented
### 📜 Landing Page
**Done by Athazahra Nabila Ruby**  
Displays a carousell of ads and various other cards that redirects you to another feature/page. Anyone can submit an ad, but it has to be appproved by a admin first. Only an admin can delete and edit the ads. The ads also redirects you to the brand's catalogue. All of the features implemented are able to be viewed from the navigation bar.

### 🧼 Product Catalogue  
**Done by Muhammad Ghaza Fadhlibaqi, Anindiyo Banu Prabasworo, & Muhammad Jordan Ar-Razi Aziz**  
Displays cards of the skincare products. Each card contains the product's name, brand, price, and a 'favorite' button. When clicked, the card expands to also include description, type, and reviews. You are able to filter the catalogue by brand or product type. Other than viewing, users can add a product to their 'favorites' list and review a product by leaving a rating and comment, while an admin can add, delete, and edit the products.

### 💌 User Favorites  
**Done by Min Kim**  
Each user has their own "favorites" list. They can "love" a product to add it to the list and also remove a product from their list. A user is able to sort the products in the favorites list in the order of 'Most Recent' and 'Most Oldest". A user can also filter the products based on the skincare product types an user has in the favorites list. Only the 'logged in' users are allowed to add products to their favorites list. 

### 🗺️ Skincare Store Locator
**Done by Athazahra Nabila Ruby & Min Kim**  
Includes interactive map that shows users where they can buy skincare products in Seoul, with integration to Google Maps. Also displays cards of skincare stores in Seoul, with the ability to filter the stores by district.

### 📆 Promotion Events
**Done by Kayla Soraya Djakaria**  
Contains cards of promotion events occuring/about to occur in Seoul. Each card contains info about the store location, promotion type, and period of promotion. A user can RSVP or Cancel RSVP to multiple events and filter the events by date and year. The page will sorts the events by the nearest date and differentiate between events that has been RSVP'd and not.

## Source for Intial Dataset
This application is going to utilize the dataset [Skin Care](https://www.kaggle.com/datasets/taniadh/skin-care?resource=download) which is available on Kaggle. The dataset contains a list of Korean skincare products along with their name, brand, price, description, and type.

## Roles
1. User: View, rate, and leave a comment on products, add product to favorites, RSVP to events, submit ads.
2. Admin: Add, delete, edit products, delete reviews, approve ads, create events, add store location, and everything else a User can do.