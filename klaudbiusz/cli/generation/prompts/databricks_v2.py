"""Databricks v2 prompts - realistic human-style requests for dashboards/apps"""

PROMPTS = {
    # Wanderbricks (Travel Platform)
    "property_search_app": "I need an app to search through properties in the wanderbricks schema. Users should be able to filter by price range, number of bedrooms, and pick a city. Show results on a map with the prices and let them click for details. Oh and my product manager says the search needs to feel 'fast' even with lots of results - figure out what that means technically.",

    "booking_calendar": "Build me a booking calendar using data from wanderbricks about reservations or bookings or whatever you call them. Show all bookings for the next few months, color coded by status. When I click a date I should see full booking details and be able to filter by property.",

    "property_comparison": "Build me a tool using the wanderbricks property data where I can select 2-3 properties and compare them side by side - price, amenities, reviews, location. Make it interactive so I can swap properties in and out.",

    "city_performance_app": "Using wanderbricks booking data and property listings, show which cities are making the most money. Let me click into a city to see all properties there, their occupancy rates, and booking trends over time. Finance team wants revenue, ops team wants occupancy - they argue about which metric matters more. Just show both but make it clear which cities are 'good' overall somehow.",

    "guest_booking_history": "Need an app where I can search for any guest in wanderbricks and see their complete booking history - where they stayed, dates, how much they paid, their reviews. Show it as a timeline.",

    "property_pricing_wizard": "Using wanderbricks property info and booking history, build an app that suggests optimal pricing. Show current price vs suggested price based on occupancy and also I want it to have like a slider where I can simulate 'what if I increase price by 10%' and see projected revenue impact. Make it colorful.",

    "host_onboarding_checklist": "Build an app for new hosts using wanderbricks. Show a checklist of things they need to complete - add photos, set pricing, write description. Track completion percentage and show them how similar properties are performing to give them benchmarks.",

    # TPC-DS (Retail)
    "store_manager_simulator": "This is gonna sound weird but using tpcds store sales and stock levels, build an app where I can pretend to be a store manager. Show me my current inventory, sales trends, and let me simulate decisions like 'order more of this product' or 'put this on sale' and show projected outcomes based on historical data.",

    "return_pattern_analysis": "Using tpcds returns data, I need to identify unusual return patterns that might indicate fraud or quality issues. Show customers with high return rates, products that get returned frequently, and any patterns by day of week or time period. Let me set thresholds for what counts as 'high' and flag suspicious cases. Legal says we can't accuse anyone of fraud directly so word things carefully - maybe 'requires review' instead of 'suspicious'.",

    "customer_lookalike_finder": "Using tpcds customer data and shopping history, build an app where I input a customer ID and it finds other customers who shop similarly - same categories, similar spend, similar frequency. Show the top 10 matches with a similarity score for targeting similar customer segments.",

    # TPC-H (Supply Chain)
    "parts_catalog_app": "Build a searchable parts catalog from tpch. Users should filter by manufacturer, type, size. Show all suppliers for each part with pricing, and let me compare suppliers.",

    "supplier_risk_assessment": "Using tpch supplier and order data, build a dashboard that scores suppliers by risk. Consider factors like delivery reliability, concentration risk (do we depend on them too much?), and geographic diversity. Color code them red/yellow/green. Procurement team thinks we should weight price heavily, but supply chain team says reliability matters more - come up with a balanced scoring approach and explain your reasoning in the UI somewhere.",

    "part_substitution_finder": "This might be tricky but using tpch parts data, find parts that could substitute for each other - like same size, same type, similar price. Build an app where I search for a part and it suggests alternatives. Include a feature where I can flag two parts as 'definitely substitutable' and save that somehow.",

    "order_archaeology": "Using tpch order history, build something where I can dig into the history of an order - when it was placed, when each item shipped, who touched it, delays, everything. Make it look like a timeline with annotations. Also add a way to compare this order to 'typical' orders to see if it was unusually slow or expensive.",

    # NYC Taxi
    "taxi_zones_map": "Using nyctaxi trip data, build a map showing pickup zones colored by trip volume. Let me filter by time of day and day of week. When I click a zone show average fares and trip counts.",

    "driver_opportunity_map": "Using nyctaxi trip history, build an app showing optimal pickup locations by time of day. Show best pickup zones by hour, average fares, typical trip distances. Let me click on a zone and time to see expected earnings potential and trip frequency.",

    "fare_fairness_checker": "Using nyctaxi trip data, build an app that checks if fares look reasonable for the distance. Flag trips where the fare seems off for the distance traveled. Here's the tricky part: what counts as 'unfair' is subjective - a tourist might not mind overpaying, but a local would. Let me toggle between 'strict' and 'lenient' fairness thresholds. Show outliers on a map and calculate what a 'typical' fare would be for that route.",

    # Complex / Multi-table
    "property_booking_funnel": "Using wanderbricks user activity data and actual bookings, build a funnel visualization showing the path from property view to booking. Show drop-off rates at each step and let me filter by property type.",

    "host_property_management": "Build a complete host dashboard using wanderbricks. Let hosts see all their properties, upcoming bookings, recent reviews, and revenue metrics in one place. Different hosts have different priorities - some care about revenue, some about ratings, some about occupancy. The dashboard should somehow surface what matters most to each host type without being overwhelming. Think about information hierarchy.",

    "retail_inventory_sales_reconciliation": "Using tpcds warehouse inventory and sales records, build an app that cross-references inventory movements with actual sales. Flag mismatches and let me drill into specific products and warehouses.",

    "supplier_part_explorer": "Using tpch supplier and parts data, create an interactive app showing relationships between suppliers and parts. Let me search for a part and see all suppliers, or pick a supplier and see all their parts with order history.",

    "omnichannel_customer_view": "Using tpcds customer and sales data from all channels, build an app showing complete customer purchase history across web, store, and catalog. Let me search for customers and see their preferred channel, total spend per channel, and purchase timeline.",

    "review_trends_dashboard": "Using wanderbricks reviews, build a dashboard showing review trends over time. Here's the thing: a property going from 4.8 to 4.5 stars is very different from one going 3.2 to 2.9, even though both dropped 0.3. Figure out a smart way to flag 'concerning' rating drops that accounts for the baseline. Show trends over time and let me see actual review text when I click.",

    "cross_platform_customer_analysis": "I want to explore potential overlap between wanderbricks users and tpcds customers. Try matching by email or name to identify customers who both book travel and shop retail. This is experimental since the datasets aren't explicitly linked, but could reveal interesting patterns. Make sure to clearly label this as an experimental analysis.",

    "order_journey_narrative": "Using tpch order and supplier data, build an app that shows the complete journey of an order in a narrative format. Pick an order and present it as a story: 'Customer X ordered parts from 3 different suppliers in 2 countries, Part Y was delayed by 5 days because Supplier Z had issues, total value was $$$'. Make it visual and easy to understand, not just raw data tables.",

    # Simple ML/Predictive with judgment calls
    "price_prediction_tool": "Using wanderbricks property and booking data, build a price prediction tool. Use linear regression on property features (bedrooms, location, amenities) to predict optimal nightly price. Show predicted price and which factors contribute most. But here's the thing - the model might suggest $200 for a property currently priced at $150. Show the gap and let hosts understand the tradeoff: predicted price vs current occupancy rate. Let me adjust features and see how prediction changes.",

    "customer_segment_clusters": "Using tpcds customer demographics and purchase behavior, build a customer segmentation tool with K-means clustering. But the 'right' number of clusters is debatable - marketing wants 3-4 broad segments, analytics wants 6-7 precise ones. Let me toggle between k=3, k=5, k=7 and show how groupings change. Display each cluster's characteristics: average spend, frequency, preferred categories, and explain what makes each segment distinct.",

    "churn_risk_predictor": "Using wanderbricks guest booking history, build a churn prediction tool. Use logistic regression on features like days since last booking, total bookings, average spend. Show customers ranked by churn risk. But be careful with interpretation - a 'high risk' frequent traveler who just booked is different from a 'high risk' one-time guest. Add context to the scores so I understand why someone is flagged.",

    "similar_properties_recommender": "Using wanderbricks property features and booking data, build a recommendation tool using KNN. When I select a property, show 10 most similar ones. But 'similar' is subjective - a family cares about bedrooms, a business traveler cares about location and wifi. Let me choose similarity mode: 'family friendly', 'business travel', 'budget conscious', or 'overall'. Explain which features drove each match.",

    "sales_trend_analyzer": "Using tpcds store sales data, create a trend analysis tool with linear regression. For each store/category, show if sales are trending up or down and at what rate. But raw trends lie - a 5% drop in a volatile category is normal, a 5% drop in a stable one is alarming. Factor in historical volatility when flagging concerns. Show confidence intervals, not just point estimates.",
}
