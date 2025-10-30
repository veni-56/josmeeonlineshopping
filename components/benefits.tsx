import { Heart, Leaf, Sparkles, Shield } from "lucide-react"

const benefits = [
  {
    icon: Heart,
    title: "Rich in Quality",
    description: "Carefully selected products that meet our high standards for quality and authenticity.",
  },
  {
    icon: Leaf,
    title: "100% Authentic",
    description: "Genuine products sourced directly, ensuring you get the real deal every time.",
  },
  {
    icon: Sparkles,
    title: "Best Prices",
    description: "Competitive pricing without compromising on quality or authenticity.",
  },
  {
    icon: Shield,
    title: "Trusted Service",
    description: "Reliable delivery and customer support you can count on for a seamless experience.",
  },
]

export function Benefits() {
  return (
    <section className="py-32 bg-background">
      <div className="container px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-4 mb-20">
            <p className="text-sm uppercase tracking-[0.3em] text-accent font-medium">Why Choose Us</p>
            <h2
              className="text-5xl md:text-6xl font-serif font-bold text-primary text-balance"
              style={{ fontFamily: "var(--font-playfair)" }}
            >
              Why Choose Josmee?
            </h2>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <div key={index} className="space-y-5 text-center group">
                <div className="w-16 h-16 rounded-full bg-accent/10 flex items-center justify-center mx-auto group-hover:bg-accent/20 transition-colors">
                  <benefit.icon className="w-8 h-8 text-accent" />
                </div>
                <h3 className="text-xl font-bold text-foreground">{benefit.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{benefit.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
