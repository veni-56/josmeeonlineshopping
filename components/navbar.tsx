"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Search, ShoppingCart, Menu, X, User } from "lucide-react"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import Image from "next/image"

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const router = useRouter()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery)}`)
      setSearchQuery("")
    }
  }

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-border shadow-sm">
      <div className="bg-white border-b border-border">
        <div className="container px-4 py-3 flex items-center justify-between gap-4">
          {/* Logo */}
          <Link href="/" className="flex-shrink-0">
            <div className="flex items-center gap-2">
              <Image
                src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/WhatsApp%20Image%202025-10-25%20at%202.01.11%20AM-tVR9fmPDUAb15kyGln4iiS7FKSNkKl.jpeg"
                alt="Josmee Logo"
                width={50}
                height={50}
                className="h-12 w-auto"
                priority
              />
              <span className="hidden sm:inline font-bold text-xl text-primary">JOSMEE</span>
            </div>
          </Link>

          {/* Search bar - prominent on desktop */}
          <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-md mx-4">
            <div className="relative w-full">
              <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-2.5 rounded-full border border-border bg-white focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm"
              />
              <button
                type="submit"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-primary"
              >
                <Search className="w-5 h-5" />
              </button>
            </div>
          </form>

          {/* Right side - Account and Cart */}
          <div className="flex items-center gap-4">
            {/* Account dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="hidden sm:flex gap-2 text-foreground hover:text-primary">
                  <User className="w-5 h-5" />
                  <span className="text-sm">Account</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuItem asChild>
                  <Link href="/accounts/phone-verification">Login</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/accounts/register">Register</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/accounts/seller-register">Seller Register</Link>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Cart */}
            <Button variant="ghost" size="icon" className="relative text-foreground hover:text-primary">
              <ShoppingCart className="w-5 h-5" />
              <span className="absolute -top-2 -right-2 bg-primary text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">
                0
              </span>
            </Button>

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden text-foreground"
              onClick={() => setIsOpen(!isOpen)}
            >
              {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile search */}
        <form onSubmit={handleSearch} className="md:hidden px-4 pb-3">
          <div className="relative w-full">
            <input
              type="text"
              placeholder="Search products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2.5 rounded-full border border-border bg-white focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm"
            />
            <button
              type="submit"
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-primary"
            >
              <Search className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>

      {/* Main navigation bar */}
      <div className="bg-white border-b border-border">
        <div className="container px-4">
          <div className="hidden md:flex items-center justify-between py-3">
            {/* Categories dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="text-foreground hover:text-primary gap-2 font-semibold">
                  <Menu className="w-5 h-5" />
                  <span>Categories</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56">
                <DropdownMenuItem asChild>
                  <Link href="/products?category=jaggery">Palm Jaggery</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/products?category=spices">Spices</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/products?category=oils">Oils</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/products?category=grains">Grains</Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href="/products?category=honey">Honey & Sweeteners</Link>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Navigation links */}
            <div className="flex items-center gap-6">
              <Link href="/" className="text-sm font-medium text-foreground hover:text-primary transition-colors">
                Home
              </Link>
              <Link href="/about" className="text-sm font-medium text-foreground hover:text-primary transition-colors">
                About Us
              </Link>
              <Link
                href="/products"
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Products
              </Link>
              <Link
                href="/health-benefits"
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Health Benefits
              </Link>
              <Link
                href="/recipes"
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Recipes
              </Link>
              <Link
                href="/contact"
                className="text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Contact
              </Link>
            </div>

            {/* Seller register link */}
            <Link
              href="/accounts/seller-register"
              className="text-sm font-medium text-foreground hover:text-primary transition-colors"
            >
              Seller Register
            </Link>
          </div>

          {/* Mobile navigation menu */}
          {isOpen && (
            <div className="md:hidden py-4 space-y-3 border-t border-border">
              <Link href="/" className="block text-sm font-medium text-foreground hover:text-primary transition-colors">
                Home
              </Link>
              <Link
                href="/about"
                className="block text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                About Us
              </Link>
              <Link
                href="/products"
                className="block text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Products
              </Link>
              <Link
                href="/health-benefits"
                className="block text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Health Benefits
              </Link>
              <Link
                href="/recipes"
                className="block text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Recipes
              </Link>
              <Link
                href="/contact"
                className="block text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Contact
              </Link>
              <Link
                href="/accounts/seller-register"
                className="block text-sm font-medium text-foreground hover:text-primary transition-colors"
              >
                Seller Register
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
