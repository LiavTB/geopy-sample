# {
#     "ACCESS_GATEWAY": 4000, # שדות תעופה
# "ADMINISTRATIVE_DIVISION": None,
# "ADVENTURE_SPORTS_VENUE": 50,
# "AGRICULTURE":
# "AIRPORT"
# "AMUSEMENT_PARK"
# "AUTOMOTIVE_DEALER"
# "BANK"
# "BEACH"
# "BUILDING_POINT"
# "BUSINESS_PARK"
# "CAFE_PUB"
# "CAMPING_GROUND"
# "CAR_WASH"
# "CASH_DISPENSER"
# "CASINO"
# "CINEMA"
# "CITY_CENTER"
# "CLUB_ASSOCIATION"
# "COLLEGE_UNIVERSITY"
# "COMMERCIAL_BUILDING"
# "COMMUNITY_CENTER"
# "COMPANY"
# "COURTHOUSE"
# "CULTURAL_CENTER"
# "DENTIST"
# "DEPARTMENT_STORE"
# "DOCTOR"
# "ELECTRIC_VEHICLE_STATION"
# "EMBASSY"
# "EMERGENCY_MEDICAL_SERVICE"
# "ENTERTAINMENT"
# "EXCHANGE"
# "EXHIBITION_CONVENTION_CENTER"
# "FERRY_TERMINAL"
# "FIRE_STATION_BRIGADE"
# "FRONTIER_CROSSING"
# "FUEL_FACILITIES"
# "GEOGRAPHIC_FEATURE"
# "GOLF_COURSE"
# "GOVERNMENT_OFFICE"
# "HEALTH_CARE_SERVICE"
# "HELIPAD_HELICOPTER_LANDING"
# "HOLIDAY_RENTAL"
# "HOSPITAL_POLYCLINIC"
# "HOTEL_MOTEL"
# "ICE_SKATING_RINK"
# "IMPORTANT_TOURIST_ATTRACTION"
# "INDUSTRIAL_BUILDING"
# "LEISURE_CENTER"
# "LIBRARY"
# "MANUFACTURING_FACILITY"
# "MARINA"
# "MARKET"
# "MEDIA_FACILITY"
# "MILITARY_INSTALLATION"
# "MOTORING_ORGANIZATION_OFFICE"
# "MOUNTAIN_PASS"
# "MUSEUM"
# "NATIVE_RESERVATION"
# "NIGHTLIFE"
# "NON_GOVERNMENTAL_ORGANIZATION"
# "OPEN_PARKING_AREA"
# "OTHER"
# "PARKING_GARAGE"
# "PARK_RECREATION_AREA"
# "PETROL_STATION"
# "PHARMACY"
# "PLACE_OF_WORSHIP"
# "POLICE_STATION"
# "PORT_WAREHOUSE_FACILITY"
# "POST_OFFICE"
# "PRIMARY_RESOURCE_UTILITY"
# "PRISON_CORRECTIONAL_FACILITY"
# "PUBLIC_AMENITY"
# "PUBLIC_TRANSPORT_STOP"
# "RAILWAY_STATION"
# "RENT_A_CAR_FACILITY"
# "RENT_A_CAR_PARKING"
# "REPAIR_FACILITY"
# "RESEARCH_FACILITY"
# "RESIDENTIAL_ACCOMMODATION"
# "RESTAURANT"
# "RESTAURANT_AREA"
# "REST_AREA"
# "SCENIC_PANORAMIC_VIEW"
# "SCHOOL"
# "SHOP"
# "SHOPPING_CENTER"
# "SPORTS_CENTER"
# "STADIUM"
# "SWIMMING_POOL"
# "TENNIS_COURT"
# "THEATER"
# "TOURIST_INFORMATION_OFFICE"
# "TRAFFIC_LIGHT"
# "TRAFFIC_SERVICE_CENTER"
# "TRAFFIC_SIGN"
# "TRAIL_SYSTEM"
# "TRANSPORT_AUTHORITY VEHICLE_REGISTRATION"
# "TRUCK_STOP"
# "VETERINARIAN"
# "WATER_SPORT"
# "WEIGH_STATION"
# "WELFARE_ORGANIZATION"
# "WINERY"
# "ZOOS_ARBORETA_BOTANICAL_GARDEN"
#  }


def get_max_distance_for_classification(classification):
    if classification.upper() in type_to_point_distances:
        distance = type_to_point_distances[classification.upper()]
        if distance is not None:
            return distance
    return get_default_distance()


def get_default_distance():
    return type_to_point_distances["default".upper()]


type_to_point_distances_temp = {
    "default": 70,
    "PUBLIC_TRANSPORT_STOP": 50,
    "RAILWAY_STATION": 250,
    "HOTEL_MOTEL": 150,
    "IMPORTANT_TOURIST_ATTRACTION": 500, # if want more need to gry the extent
    "SCHOOL": 760,
    "RESTAURANT": 550,
    "PLACE_OF_WORSHIP": 370,
    "MUSEUM": 150,
    "SHOP": 500,
    "PETROL_STATION": 90,
    "AMUSEMENT_PARK": 80,
    "CAFE_PUB": 70,
    "STADIUM": 70,
    "SHOPPING_CENTER": 500,
    "EXHIBITION_CONVENTION_CENTER": 400,
    "MARKET": 200,
    "BANK": 100,
    "COMMUNITY_CENTER": 90, # consider maybe 500
    "HOSPITAL_POLYCLINIC": 200, # consider maybe 500
    "HEALTH_CARE_SERVICE": 200, # consider maybe 500
    "COMMERCIAL_BUILDING": 200,
    "[COLLEGE_UNIVERSITY]": 90,
    "RESIDENTIAL_ACCOMMODATION": 90,
    "SPORTS_CENTER": 90,
    "PHARMACY": 90,
    "RENT_A_CAR_FACILITY": None,
    "CINEMA": 210 , # consider maybe 700
    "DOCTOR": None,
    "THEATER": None,
    "AUTOMOTIVE_DEALER": 350,
    "EMBASSY": None,
    "NIGHTLIFE": None,
    "PARKING_GARAGE": 300,
    "PUBLIC_AMENITY": 100,
    "COMPANY": 100,
    "PARK_RECREATION_AREA": None,
    "DENTIST": None,
    "SWIMMING_POOL": 500,
    "LIBRARY": 200,
    "OPEN_PARKING_AREA": None , # Check what to do
    "CASH_DISPENSER": None,
    "POST_OFFICE": None,
    "GOVERNMENT_OFFICE": 350,
    "REPAIR_FACILITY": 350,
    "DEPARTMENT_STORE": 100,
    "VETERINARIAN": None,
    "COURTHOUSE": None, # It's very formal and accurate, but can help to find somthing else near by
    "TRANSPORT_AUTHORITY_VEHICLE_REGISTRATION": None,
    "ZOOS_ARBORETA_BOTANICAL_GARDEN": 150,
    "AIRPORT": 2400,
    "POLICE_STATION": None,
    "ENTERTAINMENT": None,
    "BEACH": 350,
    "LEISURE_CENTER": None,
    "TOURIST_INFORMATION_OFFICE": None,

#     arcgis
    "ATM": None,
    "Auto Dealership": None,
    "Auto Maintenance": 350,
    "Bakery": None,
    "Bar or Pub": 200,  # Consider this
    "BBQ and Southern Food": None,
    "Burgers": None,
    "Bus Station": 220,
    "Business Facility": 90,
    "Campground": None,
    "Cemetery": 400,
    "Childrens Apparel": None,
    "Church": 120,
    "City Hall": 140,
    "Civic Center": 200,
    "Clothing Store": None,
    "Coffee Shop": 150,
    "College": 120,  # maybe 400 or 1500 (but with filtering on the address)
    "Consumer Electronics Store": 180,
    "Convenience Store": None,
    "Convention Center": 150,
    "Court House": None,
    "Dentist": None,
    "Department Store": None,
    "Doctor": None,
    "Embassy": None,
    "Fast Food": None,
    "Fitness Center": None,
    "Food and Beverage Shop": 160,
    "French Food": None,
    "Furniture Store": 250,
    "Fusion Food": 150,
    "Gas Station": None,
    "Government Office": None,  # Check the results for that classification
    "Grill": None,
    "Grocery": 190,
    "Historical Monument": 150,
    "Home Improvement Store": None,
    "Hospital": 500,
    "Hotel": 120,  # Maybe 500
    "Ice Cream Shop": None,
    "Industrial Zone": None,
    "International Food": 100,
    "Italian Food": 180,
    "Japanese Food": None,
    "Kosher Food": None,
    "Library": None,
    "Medical Clinic": 700,
    "Middle Eastern Food": None,
    "Mosque": None,
    "Museum": 400,
    "Nature Reserve": 700,
    "Office Supplies Store": None,
    "Other Travel": 100,
    "Park": 200,
    "Parking": 110,
    "Pastries": None,
    "Performing Arts": 200,
    "Pizza": None,
    "Police Station": None,
    "Post Office": None,
    "Rental Cars": 700,
    "Ruin": 1200,
    "Sandwich Shop": 180,
    "Sea": None,
    "Seafood": None,
    "Shopping Center": 250,
    "Southeast Asian Food": None,
    "Specialty Store": 600,  # Maybe 200
    "Sporting Goods Store": None,
    "Sports Center": 200,
    "Sushi": None,
    "Synagogue": 200,
    "Tourist Attraction": 400,
    "Train Station": 200,
    "Winery": None
}

type_to_point_distances = {k.upper(): v for k, v in type_to_point_distances_temp.items()}
