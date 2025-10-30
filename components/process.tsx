export function Process() {
  const steps = [
    {
      number: "01",
      title: "Browse",
      description:
        "Explore our carefully curated collection of authentic products and find exactly what you're looking for.",
    },
    {
      number: "02",
      title: "Select",
      description: "Choose your preferred items and add them to your cart with confidence in our quality guarantee.",
    },
    {
      number: "03",
      title: "Checkout",
      description: "Complete your purchase securely with our easy and safe checkout process.",
    },
    {
      number: "04",
      title: "Deliver",
      description: "Receive your order at your doorstep with our reliable and fast delivery service.",
    },
  ]

  return (
    <section className="py-32 bg-secondary/30">
      <div className="container px-4">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center space-y-4 mb-20">
            <p className="text-sm uppercase tracking-[0.3em] text-accent font-medium">Our Process</p>
            <h2
              className="text-5xl md:text-6xl font-serif font-bold text-primary text-balance"
              style={{ fontFamily: "var(--font-playfair)" }}
            >
              Simple & Easy
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty leading-relaxed">
              Shopping with Josmee is simple, secure, and satisfying. Follow our straightforward process to get quality
              products delivered to your door.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-x-12 gap-y-12 mb-20">
            {steps.map((step, index) => (
              <div key={index} className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-14 h-14 rounded-full bg-accent text-accent-foreground flex items-center justify-center text-lg font-bold">
                    {step.number}
                  </div>
                </div>
                <div className="space-y-3 pt-1">
                  <h3 className="text-2xl font-bold text-foreground">{step.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{step.description}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Process image */}
          <div className="rounded-xl overflow-hidden shadow-2xl">
            <img
              src="/traditional-palm-sap-collection-and-karupatti-maki.jpg"
              alt="Shopping process"
              className="w-full h-auto object-cover"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
