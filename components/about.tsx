export function About() {
  return (
    <section className="py-32 bg-card">
      <div className="container px-4">
        <div className="max-w-4xl mx-auto text-center space-y-10">
          <div className="space-y-4">
            <p className="text-sm uppercase tracking-[0.3em] text-accent font-medium">The Story</p>
            <h2
              className="text-5xl md:text-6xl lg:text-7xl font-serif font-bold text-primary text-balance leading-tight"
              style={{ fontFamily: "var(--font-playfair)" }}
            >
              Quality & Authenticity
            </h2>
          </div>

          {/* Description */}
          <div className="space-y-6 max-w-3xl mx-auto">
            <p className="text-lg md:text-xl text-foreground leading-relaxed text-pretty">
              Josmee is your trusted online shopping destination for authentic, quality products. We bring you the
              finest selection of traditional goods and modern essentials, all carefully curated for your satisfaction.
            </p>
            <p className="text-lg md:text-xl text-muted-foreground leading-relaxed text-pretty">
              We believe in sustainable practices, fair trade, and bringing you products that celebrate tradition and
              quality. Each item in our collection tells a story of craftsmanship, authenticity, and the timeless wisdom
              of traditional practices that have been perfected over generations.
            </p>
          </div>

          {/* Decorative divider */}
          <div className="pt-8">
            <div className="w-24 h-px bg-accent mx-auto"></div>
          </div>
        </div>
      </div>
    </section>
  )
}
