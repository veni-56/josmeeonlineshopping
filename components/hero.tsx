import { Button } from "@/components/ui/button"
import { ArrowRight, ChevronDown } from "lucide-react"

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-white">
      <div className="container relative z-10 px-4 py-32 md:py-40">
        <div className="max-w-5xl mx-auto text-center space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full bg-primary/10 border border-primary/20">
            <span className="text-sm font-bold text-primary uppercase tracking-wide">Shop Now</span>
          </div>

          {/* Main heading */}
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight text-balance leading-tight text-foreground">
            <span className="block">Your Favorite</span>
            <span className="block text-primary">Online Shopping</span>
            <span className="block">Destination</span>
          </h1>

          {/* Subheading */}
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto text-pretty leading-relaxed">
            Discover quality products, amazing deals, and authentic goods delivered to your doorstep. Shop with
            confidence.
          </p>

          {/* CTA buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-6">
            <Button
              size="lg"
              className="text-base px-10 py-6 bg-primary hover:bg-primary/90 text-white rounded-lg font-semibold"
            >
              Explore Products
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="text-base px-10 py-6 border-2 border-primary text-primary hover:bg-primary/5 bg-white rounded-lg font-semibold transition-all"
            >
              Learn More
            </Button>
          </div>

          {/* Hero image */}
          <div className="pt-16">
            <div className="relative rounded-xl overflow-hidden shadow-lg">
              <img src="/online-shopping-products.jpg" alt="Premium products" className="w-full h-auto object-cover" />
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <ChevronDown className="w-6 h-6 text-muted-foreground" />
      </div>
    </section>
  )
}
