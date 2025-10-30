import { Facebook, Instagram, Twitter, Mail, Phone, MapPin } from "lucide-react"
import Image from "next/image"

export function Footer() {
  return (
    <footer className="bg-white border-t border-border">
      <div className="container px-4 py-16">
        <div className="grid md:grid-cols-4 gap-12 mb-12">
          {/* Brand */}
          <div className="space-y-5">
            <div className="flex items-center gap-3">
              <Image
                src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/WhatsApp%20Image%202025-10-25%20at%202.01.11%20AM-tVR9fmPDUAb15kyGln4iiS7FKSNkKl.jpeg"
                alt="Josmee Logo"
                width={50}
                height={50}
                className="h-12 w-auto"
              />
              <h3 className="text-2xl font-bold text-primary">JOSMEE</h3>
            </div>
            <p className="text-muted-foreground leading-relaxed text-sm">
              Your trusted online shopping destination for quality products and authentic goods.
            </p>
            <div className="flex gap-3 pt-2">
              <a
                href="#"
                className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center hover:bg-primary hover:text-white transition-all"
                aria-label="Facebook"
              >
                <Facebook className="w-5 h-5 text-primary hover:text-white" />
              </a>
              <a
                href="#"
                className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center hover:bg-primary hover:text-white transition-all"
                aria-label="Instagram"
              >
                <Instagram className="w-5 h-5 text-primary hover:text-white" />
              </a>
              <a
                href="#"
                className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center hover:bg-primary hover:text-white transition-all"
                aria-label="Twitter"
              >
                <Twitter className="w-5 h-5 text-primary hover:text-white" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-5">
            <h4 className="font-bold text-foreground text-base">Quick Links</h4>
            <ul className="space-y-3">
              <li>
                <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                  About Us
                </a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                  Products
                </a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                  Health Benefits
                </a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                  Recipes
                </a>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div className="space-y-5">
            <h4 className="font-bold text-foreground text-base">Support</h4>
            <ul className="space-y-3">
              <li>
                <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                  FAQ
                </a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                  Shipping
                </a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                  Returns
                </a>
              </li>
              <li>
                <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                  Contact
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div className="space-y-5">
            <h4 className="font-bold text-foreground text-base">Contact Us</h4>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                <span className="text-muted-foreground text-sm">Tamil Nadu, India</span>
              </li>
              <li className="flex items-center gap-3">
                <Phone className="w-5 h-5 text-primary flex-shrink-0" />
                <div className="flex flex-col gap-1">
                  <a
                    href="tel:9442085847"
                    className="text-muted-foreground hover:text-primary transition-colors text-sm"
                  >
                    +91 94420 85847
                  </a>
                  <a
                    href="tel:04636250411"
                    className="text-muted-foreground hover:text-primary transition-colors text-sm"
                  >
                    04636 250411
                  </a>
                </div>
              </li>
              <li className="flex items-center gap-3">
                <Mail className="w-5 h-5 text-primary flex-shrink-0" />
                <a
                  href="mailto:devasindainfoods@gmail.com"
                  className="text-muted-foreground hover:text-primary transition-colors text-sm"
                >
                  devasindainfoods@gmail.com
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-border text-center">
          <p className="text-muted-foreground text-sm">© {new Date().getFullYear()} Josmee. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
