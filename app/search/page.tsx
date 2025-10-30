"use client"

import { useSearchParams } from "next/navigation"
import { useEffect, useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ShoppingCart } from "lucide-react"

interface Product {
  id: number
  name: string
  slug: string
  price: string
  image: string
  description: string
  in_stock: boolean
  stock: number
}

interface SearchResponse {
  results: Product[]
  total: number
  page: number
  pages: number
  has_next: boolean
  has_previous: boolean
}

export default function SearchPage() {
  const searchParams = useSearchParams()
  const query = searchParams.get("q") || ""
  const [results, setResults] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [pagination, setPagination] = useState({ page: 1, pages: 1, total: 0 })

  useEffect(() => {
    if (!query) {
      setLoading(false)
      return
    }

    const fetchResults = async () => {
      try {
        setLoading(true)
        const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}&page=1`)
        const data: SearchResponse = await response.json()
        setResults(data.results)
        setPagination({ page: data.page, pages: data.pages, total: data.total })
        setError("")
      } catch (err) {
        setError("Failed to fetch search results")
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchResults()
  }, [query])

  return (
    <div className="min-h-screen bg-background">
      <div className="container px-4 py-12">
        {/* Search header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-foreground mb-2">Search Results</h1>
          <p className="text-muted-foreground">{query && `Found ${pagination.total} results for "${query}"`}</p>
        </div>

        {/* Loading state */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        )}

        {/* Error state */}
        {error && <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">{error}</div>}

        {/* No results */}
        {!loading && !error && results.length === 0 && (
          <div className="text-center py-12">
            <p className="text-lg text-muted-foreground mb-4">No products found matching your search.</p>
            <Link href="/products">
              <Button>Browse All Products</Button>
            </Link>
          </div>
        )}

        {/* Results grid */}
        {!loading && !error && results.length > 0 && (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
              {results.map((product) => (
                <div key={product.id} className="group space-y-4">
                  {/* Product Image Container */}
                  <Link href={`/products/${product.slug}`}>
                    <div className="relative aspect-square overflow-hidden rounded-lg bg-card border border-border cursor-pointer">
                      <img
                        src={product.image || "/placeholder.svg"}
                        alt={product.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                      {!product.in_stock && (
                        <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                          <span className="text-white font-semibold">Out of Stock</span>
                        </div>
                      )}
                    </div>
                  </Link>

                  {/* Product Details */}
                  <div className="space-y-2">
                    <Link href={`/products/${product.slug}`}>
                      <h3 className="text-lg font-semibold text-foreground line-clamp-2 hover:text-accent transition-colors">
                        {product.name}
                      </h3>
                    </Link>
                    <p className="text-sm text-muted-foreground line-clamp-2">{product.description}</p>

                    {/* Price */}
                    <div className="flex items-center gap-2 pt-2">
                      <span className="text-xl font-bold text-accent">₹{product.price}</span>
                      <span className="text-sm text-muted-foreground">({product.stock} available)</span>
                    </div>

                    {/* Action Button */}
                    <Button
                      className="w-full bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg mt-3"
                      disabled={!product.in_stock}
                    >
                      <ShoppingCart className="mr-2 h-4 w-4" />
                      Add to Cart
                    </Button>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination info */}
            <div className="text-center text-sm text-muted-foreground">
              Page {pagination.page} of {pagination.pages}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
