"use client"

import { Button } from "@/components/ui/button"
import { ShoppingCart, Star } from "lucide-react"
import { Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext } from "@/components/ui/carousel"

const todaysDeals = [
  {
    id: 1,
    name: "Turmeric Powder",
    price: "₹5.85",
    originalPrice: "₹8.00",
    discount: "-27%",
    image: "/turmeric-powder.png",
  },
  {
    id: 2,
    name: "Mustard Oil",
    price: "₹185.85",
    originalPrice: "₹273.00",
    discount: "-32%",
    image: "/mustard-oil.jpg",
  },
  {
    id: 3,
    name: "Coriander Seeds",
    price: "₹225.75",
    originalPrice: "₹346.50",
    discount: "-35%",
    image: "/coriander-seeds.jpg",
  },
  {
    id: 4,
    name: "Cumin Seeds",
    price: "₹126.00",
    originalPrice: "₹183.75",
    discount: "-31%",
    image: "/cumin-seeds.jpg",
  },
  {
    id: 5,
    name: "Red Chili Powder",
    price: "₹231.00",
    originalPrice: "₹300.00",
    discount: "-23%",
    image: "/red-chili-powder.jpg",
  },
  {
    id: 6,
    name: "Salt",
    price: "₹63.00",
    originalPrice: "₹78.75",
    discount: "-20%",
    image: "/pile-of-salt.png",
  },
  {
    id: 7,
    name: "Jaggery Blocks",
    price: "₹157.50",
    originalPrice: "₹231.00",
    discount: "-32%",
    image: "/jaggery-blocks.jpg",
  },
  {
    id: 8,
    name: "Honey",
    price: "₹180.00",
    originalPrice: "₹270.00",
    discount: "-33%",
    image: "/golden-honey.png",
  },
]

const featuredProducts = [
  {
    id: 1,
    name: "Classic Blocks",
    weight: "500g",
    price: "₹250",
    discount: "-17%",
    rating: 4.5,
    reviews: 128,
    image: "/jaggery-blocks.jpg",
    description: "Traditional solid blocks",
  },
  {
    id: 2,
    name: "Powder Form",
    weight: "500g",
    price: "₹280",
    discount: "-20%",
    rating: 4.7,
    reviews: 95,
    image: "/jaggery-powder.jpg",
    description: "Finely ground powder",
  },
  {
    id: 3,
    name: "Premium Gift Box",
    weight: "1kg",
    price: "₹550",
    discount: "-15%",
    rating: 4.8,
    reviews: 156,
    image: "/colorful-gift-box.png",
    description: "Beautifully packaged set",
  },
  {
    id: 4,
    name: "Organic Jaggery",
    weight: "250g",
    price: "₹180",
    discount: "-12%",
    rating: 4.6,
    reviews: 87,
    image: "/organic-jaggery.jpg",
    description: "Pure organic jaggery",
  },
]

export function Products() {
  return (
    <section className="py-16 bg-white">
      <div className="container px-4">
        <div className="max-w-7xl mx-auto space-y-20">
          {/* Today's Deal Section */}
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-3xl font-bold text-foreground">Today's Deals</h2>
              <a href="#" className="text-primary font-semibold hover:underline">
                View All
              </a>
            </div>

            {/* Carousel */}
            <div className="bg-gradient-to-r from-primary/10 to-primary/5 rounded-lg p-8">
              <Carousel className="w-full">
                <CarouselContent className="-ml-2 md:-ml-4">
                  {todaysDeals.map((product) => (
                    <CarouselItem
                      key={product.id}
                      className="pl-2 md:pl-4 basis-full sm:basis-1/2 md:basis-1/3 lg:basis-1/4"
                    >
                      <div className="flex flex-col items-center text-center space-y-3">
                        {/* Product Image */}
                        <div className="w-32 h-32 rounded-lg overflow-hidden bg-white flex items-center justify-center border border-border">
                          <img
                            src={product.image || "/placeholder.svg"}
                            alt={product.name}
                            className="w-full h-full object-cover"
                          />
                        </div>

                        {/* Product Info */}
                        <div className="space-y-2">
                          <p className="text-foreground text-sm font-medium">{product.name}</p>
                          <div className="space-y-1">
                            <p className="text-primary text-lg font-bold">{product.price}</p>
                            <p className="text-muted-foreground text-xs line-through">{product.originalPrice}</p>
                          </div>
                          <span className="inline-block bg-primary text-white text-xs font-bold px-2 py-1 rounded">
                            {product.discount}
                          </span>
                        </div>
                      </div>
                    </CarouselItem>
                  ))}
                </CarouselContent>
                <CarouselPrevious className="left-0 bg-primary/20 hover:bg-primary/30 border-0 text-primary" />
                <CarouselNext className="right-0 bg-primary/20 hover:bg-primary/30 border-0 text-primary" />
              </Carousel>
            </div>
          </div>

          {/* Featured Products Section */}
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-3xl font-bold text-foreground">Featured Products</h2>
              <a href="#" className="text-primary font-semibold hover:underline">
                View All
              </a>
            </div>

            {/* Grid Layout */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {featuredProducts.map((product) => (
                <div
                  key={product.id}
                  className="group space-y-4 bg-white rounded-lg border border-border p-4 hover:shadow-lg transition-shadow"
                >
                  {/* Product Image Container */}
                  <div className="relative aspect-square overflow-hidden rounded-lg bg-muted border border-border">
                    {/* Discount Badge */}
                    {product.discount && (
                      <div className="absolute top-3 right-3 z-10 bg-primary text-white text-xs font-bold px-2 py-1 rounded">
                        {product.discount}
                      </div>
                    )}

                    <img
                      src={product.image || "/placeholder.svg"}
                      alt={product.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>

                  {/* Product Details */}
                  <div className="space-y-2">
                    <h3 className="text-base font-semibold text-foreground line-clamp-2">{product.name}</h3>
                    <p className="text-xs text-muted-foreground">{product.weight}</p>
                    <p className="text-xs text-muted-foreground line-clamp-1">{product.description}</p>

                    {/* Rating */}
                    <div className="flex items-center gap-1 pt-1">
                      <div className="flex items-center gap-0.5">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`w-3 h-3 ${
                              i < Math.floor(product.rating) ? "fill-primary text-primary" : "text-muted-foreground"
                            }`}
                          />
                        ))}
                      </div>
                      <span className="text-xs text-muted-foreground">({product.reviews})</span>
                    </div>

                    {/* Price */}
                    <div className="flex items-center gap-2 pt-2">
                      <span className="text-lg font-bold text-primary">{product.price}</span>
                    </div>

                    {/* Action Button */}
                    <Button className="w-full bg-primary hover:bg-primary/90 text-white rounded-lg mt-3 font-semibold">
                      <ShoppingCart className="mr-2 h-4 w-4" />
                      Add to Cart
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
