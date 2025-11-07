## Drizzle Schema Handling:

```typescript
import { serial, text, pgTable, timestamp, numeric, integer } from 'drizzle-orm/pg-core';

export const productsTable = pgTable('products', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  description: text('description'), // Nullable by default, matches Zod schema
  price: numeric('price', { precision: 10, scale: 2 }).notNull(), // Use numeric for monetary values with precision
  stock_quantity: integer('stock_quantity').notNull(), // Use integer for whole numbers
  created_at: timestamp('created_at').defaultNow().notNull(),
});

// TypeScript type for the table schema
export type Product = typeof productsTable.$inferSelect; // For SELECT operations
export type NewProduct = typeof productsTable.$inferInsert; // For INSERT operations

// Important: Export all tables and relations for proper query building
export const tables = { products: productsTable };
```

## Handler implementation:

server/src/handlers/create_product.ts
```typescript
import { db } from '../db';
import { productsTable } from '../db/schema';
import { type CreateProductInput, type Product } from '../schema';

export const createProduct = async (input: CreateProductInput): Promise<Product> => {
  try {
    // Insert product record
    const result = await db.insert(productsTable)
      .values({
        name: input.name,
        description: input.description,
        price: input.price.toString(), // Convert number to string for numeric column
        stock_quantity: input.stock_quantity // Integer column - no conversion needed
      })
      .returning()
      .execute();

    // Convert numeric fields back to numbers before returning
    const product = result[0];
    return {
      ...product,
      price: parseFloat(product.price) // Convert string back to number
    };
  } catch (error) {
    console.error('Product creation failed:', error);
    throw error;
  }
};
```
