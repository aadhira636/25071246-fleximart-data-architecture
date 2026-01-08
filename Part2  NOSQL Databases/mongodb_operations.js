// Operation 1: Import JSON
// Import the provided JSON file into collection 'products'
    //Process in MongoDB Compass
        //Compass → fleximart → IMPORT → select products_catalog.json → Collection products → Import
        // Result: products collection with 10 docs ready for Operations 2-5.

// Basic Query: Electronics category, price < 50000
// Return: name, price, stock only
    db.products.find(
    { 
        "category": "Electronics", 
        "price": { "$lt": 50000 } 
    },
)
// OPERATION 3: Review Analysis (2 marks)
// Find products with average rating >= 4.0 using aggregation

// use fleximart;

db.products.aggregate([
  // Stage 1: Filter products with non-empty reviews
  { $match: { "reviews": { $exists: true, $ne: [] } } },
  
  // Stage 2: Calculate average rating
  { $addFields: { 
      avg_rating: { $avg: "$reviews.rating" } 
    } 
  },
  
  // Stage 3: Filter average >= 4.0, project key fields
  { $match: { avg_rating: { $gte: 4.0 } } },
  
  { $project: { name: 1, avg_rating: 1, _id: 0 } }
]);

// OPERATION 4: Update Operation (2 marks)
// Add new review to product ELEC001

//use fleximart;

db.products.updateOne(
  { "product_id": "ELEC001" },  // Filter: exact product
  { 
    "$push": {  // Append to array (non-destructive)
      "reviews": { 
        "user": "U999", 
        "rating": 4, 
        "comment": "Good value", 
        "date": new ISODate()  // Current timestamp
      } 
    }
  }
);

// Verify update
db.products.findOne(
  { "product_id": "ELEC001" }, 
  { "name": 1, "reviews": 1 }
);

// OPERATION 5: Complex Aggregation (3 marks)
// Calculate average price by category, count products, sort by avg_price DESC

//use fleximart;

db.products.aggregate([
  // Stage 1: Group by category, compute avg price & count
  {
    $group: {
      "_id": "$category",
      "avg_price": { $avg: "$price" },
      "product_count": { $sum: 1 }
    }
  },
  
  // Stage 2: Sort by avg_price descending
  { $sort: { avg_price: -1 } },
  
  // Stage 3: Project clean output (category, avg_price, product_count)
  {
    $project: {
      "category": "$_id",
      "avg_price": { $round: ["$avg_price", 2] },  // Optional: round to 2 decimals
      "product_count": 1,
      "_id": 0
    }
  }
]);
